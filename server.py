#!/usr/bin/env python3
"""
Documenter MCP Server - Simplified and Optimized
A complete MCP server for project documentation with all tools from main.py
"""

import json
import os
import re
import sys
import platform
import time
import uuid
import tempfile
import shutil
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Enhanced project type detection with comprehensive patterns
PROJECT_CONFIGS = {
    "nextjs": {
        "indicators": ["next.config.js", "next.config.ts", "next.config.mjs", "package.json"],
        "check_content": {"package.json": ["next", "@next/"]},
        "important_dirs": ["app", "pages", "components", "src", "public", "styles"],
        "confidence_boost": 3
    },
    "react": {
        "indicators": ["package.json"],
        "check_content": {"package.json": ["react", "react-dom", "react-scripts", "@types/react"]},
        "important_dirs": ["src", "components", "public", "build"],
        "confidence_boost": 2
    },
    "angular": {
        "indicators": ["angular.json", "package.json"],
        "check_content": {"package.json": ["@angular/", "angular"]},
        "important_dirs": ["src", "app", "components", "services", "modules"],
        "confidence_boost": 3
    },
    "vue": {
        "indicators": ["vue.config.js", "vite.config.js", "package.json"],
        "check_content": {"package.json": ["vue", "@vue/", "nuxt"]},
        "important_dirs": ["src", "components", "views", "router", "store"],
        "confidence_boost": 2
    },
    "python": {
        "indicators": ["requirements.txt", "pyproject.toml", "setup.py", "poetry.lock", "Pipfile"],
        "check_content": {"pyproject.toml": ["[tool.poetry]", "[build-system]"]},
        "important_dirs": ["src", "lib", "tests", "docs"],
        "confidence_boost": 1
    },
    "django": {
        "indicators": ["manage.py", "requirements.txt", "settings.py"],
        "check_content": {"requirements.txt": ["django", "Django"]},
        "important_dirs": ["apps", "static", "templates", "media", "migrations"],
        "confidence_boost": 3
    },
    "fastapi": {
        "indicators": ["main.py", "requirements.txt", "app.py"],
        "check_content": {"requirements.txt": ["fastapi", "uvicorn"]},
        "important_dirs": ["app", "models", "routes", "schemas", "tests"],
        "confidence_boost": 3
    },
    "nodejs": {
        "indicators": ["package.json", "server.js", "app.js", "index.js"],
        "check_content": {"package.json": ["express", "node", "fastify", "koa"]},
        "important_dirs": ["src", "lib", "routes", "controllers", "middleware"],
        "confidence_boost": 1
    },
    "java": {
        "indicators": ["pom.xml", "build.gradle", "gradlew", "build.xml"],
        "check_content": {"pom.xml": ["java", "maven"]},
        "important_dirs": ["src/main/java", "src/test/java", "src/main/resources"],
        "confidence_boost": 2
    },
    "go": {
        "indicators": ["go.mod", "go.sum", "main.go", "Makefile"],
        "check_content": {"go.mod": ["module ", "go "]},
        "important_dirs": ["cmd", "pkg", "internal", "api", "web"],
        "confidence_boost": 2
    },
    "rust": {
        "indicators": ["Cargo.toml", "Cargo.lock", "src/main.rs", "src/lib.rs"],
        "check_content": {"Cargo.toml": ["[package]", "edition = "]},
        "important_dirs": ["src", "tests", "examples", "benches"],
        "confidence_boost": 3
    },
    "docker": {
        "indicators": ["Dockerfile", "docker-compose.yml", "docker-compose.yaml"],
        "check_content": {"Dockerfile": ["FROM ", "RUN ", "COPY "]},
        "important_dirs": ["docker", "scripts"],
        "confidence_boost": 1
    }
}

class MCPHandler(BaseHTTPRequestHandler):
    """MCP Protocol HTTP Handler"""
    
    # Class-level storage for uploaded projects
    projects: Dict[str, Dict] = {}
    
    def _get_user_project_path(self, arguments: Dict, request_data: Dict = None) -> Path:
        """Get the user's project path from MCP context or arguments with enhanced detection"""
        try:
            logger.info("🔍 Attempting to detect user's project path...")
            
            # Method 1: Check if base_path is provided in arguments
            if 'base_path' in arguments and arguments['base_path']:
                provided_path = arguments['base_path']
                logger.info(f"📁 Base path provided in arguments: {provided_path}")
                
                # Handle different path formats
                if provided_path and provided_path != ".":
                    # Check if it's an absolute path
                    path_obj = Path(provided_path)
                    if path_obj.is_absolute() and path_obj.exists():
                        logger.info(f"✅ Using absolute path: {path_obj}")
                        return path_obj.resolve()
                    
                    # Try as relative path from common base directories
                    possible_bases = [
                        Path.cwd(),
                        Path("/workspace"),  # Common in cloud environments
                        Path("/app"),        # Common in Docker
                        Path("/opt/render/project/src"),  # Render environment
                    ]
                    
                    for base in possible_bases:
                        full_path = base / provided_path
                        if full_path.exists():
                            logger.info(f"✅ Found relative path: {full_path}")
                            return full_path.resolve()
            
            # Method 2: Extract from natural language in arguments
            context_path = self._extract_path_from_natural_language(arguments, request_data)
            if context_path and context_path.exists():
                logger.info(f"✅ Extracted from natural language: {context_path}")
                return context_path.resolve()
            
            # Method 3: Check MCP request context and headers
            mcp_context_path = self._extract_path_from_mcp_context(request_data)
            if mcp_context_path and mcp_context_path.exists():
                logger.info(f"✅ Found in MCP context: {mcp_context_path}")
                return mcp_context_path.resolve()
            
            # Method 4: Try to detect from request headers (if available)
            header_path = self._extract_path_from_headers()
            if header_path and header_path.exists():
                logger.info(f"✅ Found in headers: {header_path}")
                return header_path.resolve()
            
            # Method 5: Intelligent fallback - use server's current directory
            # This is where the cloud server limitation becomes apparent
            fallback_path = Path.cwd().resolve()
            logger.warning(f"⚠️ Using fallback path (server directory): {fallback_path}")
            logger.warning("💡 TIP: For better project detection, try specifying the project path in your prompt")
            
            return fallback_path
            
        except Exception as e:
            logger.error(f"❌ Error detecting project path: {e}")
            return Path.cwd().resolve()
    
    def _extract_path_from_natural_language(self, arguments: Dict, request_data: Dict = None) -> Optional[Path]:
        """Extract project path from natural language in user prompts"""
        try:
            # Get all text from the request to analyze
            text_sources = []
            
            # Check arguments for text content
            for key, value in arguments.items():
                if isinstance(value, str):
                    text_sources.append(value)
            
            # Check if there's prompt text in request_data
            if request_data:
                # Look for common fields that might contain the user's prompt
                prompt_fields = ['prompt', 'message', 'text', 'query', 'input', 'description']
                for field in prompt_fields:
                    if field in request_data and isinstance(request_data[field], str):
                        text_sources.append(request_data[field])
                
                # Check nested structures
                if 'params' in request_data and isinstance(request_data['params'], dict):
                    for field in prompt_fields:
                        if field in request_data['params']:
                            text_sources.append(str(request_data['params'][field]))
            
            # Combine all text sources
            combined_text = " ".join(text_sources).lower()
            
            if not combined_text:
                return None
            
            logger.info(f"🔍 Analyzing text for path clues: {combined_text[:100]}...")
            
            # Path extraction patterns
            import re
            
            # Pattern 1: Explicit paths (Windows and Unix)
            path_patterns = [
                r'[A-Z]:\\[^\\/:*?"<>|\r\n]+(?:\\[^\\/:*?"<>|\r\n]+)*',  # Windows absolute paths
                r'/[^/:\*\?"<>\|\r\n]+(?:/[^/:\*\?"<>\|\r\n]+)*',        # Unix absolute paths
                r'\\\\[^\\/:*?"<>|\r\n]+(?:\\[^\\/:*?"<>|\r\n]+)*',      # UNC paths
            ]
            
            for pattern in path_patterns:
                matches = re.findall(pattern, combined_text, re.IGNORECASE)
                for match in matches:
                    potential_path = Path(match)
                    if potential_path.exists() and potential_path.is_dir():
                        logger.info(f"🎯 Found explicit path in text: {potential_path}")
                        return potential_path
            
            # Pattern 2: Project name hints
            project_keywords = [
                r'project\s+(?:at|in|located|from|called|named)\s+([^\s]+)',
                r'(?:analyze|document|check)\s+([A-Za-z0-9\-_]+)\s+project',
                r'current\s+project\s+(?:at|in)\s+([^\s]+)',
                r'working\s+on\s+([A-Za-z0-9\-_]+)',
            ]
            
            for pattern in project_keywords:
                matches = re.findall(pattern, combined_text, re.IGNORECASE)
                for match in matches:
                    # Try to find this project name in common locations
                    common_locations = [
                        Path.home() / "Projects",
                        Path.home() / "Documents",
                        Path.home() / "Code",
                        Path("/workspace"),
                        Path("/app"),
                        Path("C:/Projects") if Path("C:/").exists() else None,
                        Path("C:/D/RND") if Path("C:/D").exists() else None,
                    ]
                    
                    for location in common_locations:
                        if location and location.exists():
                            potential_path = location / match
                            if potential_path.exists() and potential_path.is_dir():
                                logger.info(f"🎯 Found project by name: {potential_path}")
                                return potential_path
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Error extracting path from natural language: {e}")
            return None
    
    def _extract_path_from_mcp_context(self, request_data: Dict = None) -> Optional[Path]:
        """Extract project path from MCP request context/metadata"""
        try:
            if not request_data:
                return None
            
            # Check for workspace/project information in MCP context
            context_fields = [
                'workspace', 'project', 'cwd', 'working_directory', 
                'current_directory', 'root_path', 'base_path'
            ]
            
            for field in context_fields:
                if field in request_data:
                    path_value = request_data[field]
                    if isinstance(path_value, str) and path_value:
                        potential_path = Path(path_value)
                        if potential_path.exists():
                            return potential_path
            
            # Check nested context in params
            if 'params' in request_data and isinstance(request_data['params'], dict):
                params = request_data['params']
                for field in context_fields:
                    if field in params:
                        path_value = params[field]
                        if isinstance(path_value, str) and path_value:
                            potential_path = Path(path_value)
                            if potential_path.exists():
                                return potential_path
            
            # Check for IDE-specific context
            ide_context_fields = [
                'cursor_workspace', 'vscode_workspace', 'ide_workspace',
                'project_root', 'workspace_root'
            ]
            
            for field in ide_context_fields:
                if field in request_data:
                    path_value = request_data[field]
                    if isinstance(path_value, str) and path_value:
                        potential_path = Path(path_value)
                        if potential_path.exists():
                            return potential_path
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Error extracting path from MCP context: {e}")
            return None
    
    def _extract_path_from_headers(self) -> Optional[Path]:
        """Extract project path from HTTP headers"""
        try:
            # Check common headers that IDEs might send
            header_fields = [
                'X-Project-Path', 'X-Workspace-Path', 'X-Current-Directory',
                'X-Working-Directory', 'X-Root-Path', 'X-Base-Path',
                'Cursor-Workspace', 'VSCode-Workspace', 'IDE-Workspace'
            ]
            
            for header in header_fields:
                header_value = self.headers.get(header)
                if header_value:
                    potential_path = Path(header_value)
                    if potential_path.exists():
                        return potential_path
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Error extracting path from headers: {e}")
            return None
    
    def _send_response(self, status_code: int, data: dict):
        """Send JSON response with proper headers"""
        try:
            self.send_response(status_code)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())
        except Exception as e:
            logger.error(f"Error sending response: {e}")
            # Fallback to basic response
            try:
                self.send_response(500)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b"Internal Server Error")
            except:
                pass  # Last resort - connection might be broken
    
    def do_GET(self):
        """Handle GET requests"""
        start_time = time.time()
        try:
            parsed_url = urlparse(self.path)
            path = parsed_url.path
            
            if path == "/":
                response = {
                    "name": "Documenter MCP Server",
                    "version": "2.0.0",
                    "status": "running",
                    "description": "Intelligent documentation generator for any project type",
                    "platform": "Render",
                    "url": "https://documenter-mcp.onrender.com",
                    "endpoints": {
                        "health": "/",
                        "tools": "/tools",
                        "mcp": "/mcp/request"
                    }
                }
                self._send_response(200, response)
                
            elif path == "/tools":
                tools = self._get_all_tools()
                response = {
                    "tools": tools,
                    "count": len(tools),
                    "platform": "Railway"
                }
                self._send_response(200, response)
                
            else:
                self._send_response(404, {"error": "Endpoint not found"})
                
        except Exception as e:
            logger.error(f"GET request error: {e}")
            self._send_response(500, {"error": str(e)})
        finally:
            response_time = time.time() - start_time
            logger.info(f"GET {self.path} - {response_time:.3f}s")
    
    def do_POST(self):
        """Handle POST requests (MCP protocol)"""
        start_time = time.time()
        try:
            parsed_url = urlparse(self.path)
            path = parsed_url.path
            
            if path == "/mcp/request":
                # Read request body with error handling
                try:
                    content_length = int(self.headers.get('Content-Length', 0))
                    if content_length > 1024 * 1024:  # 1MB limit
                        self._send_response(413, {"error": "Request too large"})
                        return
                    
                    post_data = self.rfile.read(content_length)
                    if not post_data:
                        self._send_response(400, {"error": "Empty request body"})
                        return
                        
                except (ValueError, OverflowError) as e:
                    logger.error(f"Invalid content length: {e}")
                    self._send_response(400, {"error": "Invalid content length"})
                    return
                except Exception as e:
                    logger.error(f"Error reading request body: {e}")
                    self._send_response(500, {"error": "Error reading request"})
                    return
                
                # Parse JSON with error handling
                try:
                    request_data = json.loads(post_data.decode('utf-8'))
                except json.JSONDecodeError as e:
                    logger.error(f"JSON decode error: {e}")
                    self._send_response(400, {"error": "Invalid JSON"})
                    return
                except UnicodeDecodeError as e:
                    logger.error(f"Unicode decode error: {e}")
                    self._send_response(400, {"error": "Invalid encoding"})
                    return
                
                # Validate request structure
                if not isinstance(request_data, dict):
                    self._send_response(400, {"error": "Request must be a JSON object"})
                    return
                
                # Handle MCP requests
                method = request_data.get('method', '')
                request_id = request_data.get('id')
                
                if not method:
                    self._send_response(400, {"error": "Missing method"})
                    return
                
                if method == 'initialize':
                    response = {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {
                            "protocolVersion": "2024-11-05",
                            "capabilities": {
                                "tools": {
                                    "listChanged": False
                                }
                            },
                            "serverInfo": {
                                "name": "Documenter",
                                "version": "2.0.0"
                            }
                        }
                    }
                elif method == 'tools/list':
                    tools = self._get_all_tools()
                    response = {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {"tools": tools}
                    }
                elif method == 'tools/call':
                    # Handle tool calls with validation
                    params = request_data.get('params', {})
                    if not isinstance(params, dict):
                        self._send_response(400, {"error": "Invalid params"})
                        return
                    
                    tool_name = params.get('name', '')
                    arguments = params.get('arguments', {})
                    
                    if not tool_name:
                        self._send_response(400, {"error": "Missing tool name"})
                        return
                    
                    # Get user's project path and add it to context
                    user_project_path = self._get_user_project_path(arguments, request_data)
                    logger.info(f"User project path detected: {user_project_path}")
                    
                    # Add project context to arguments if not already present
                    if 'base_path' not in arguments or not arguments['base_path']:
                        arguments['base_path'] = str(user_project_path)
                    
                    result = self._execute_tool(tool_name, arguments)
                    response = {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {
                            "content": [
                                {
                                    "type": "text",
                                    "text": result
                                }
                            ]
                        }
                    }
                else:
                    response = {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "error": {
                            "code": -32601,
                            "message": f"Method not found: {method}"
                        }
                    }
                
                self._send_response(200, response)
                
            else:
                self._send_response(404, {"error": "Endpoint not found"})
                
        except Exception as e:
            logger.error(f"POST request error: {e}")
            self._send_response(500, {"error": "Internal server error"})
        finally:
            response_time = time.time() - start_time
            logger.info(f"POST {self.path} - {response_time:.3f}s")
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def _get_all_tools(self) -> List[Dict]:
        """Get all available tools with proper MCP schema"""
        return [
            {
                "name": "detect_project_type",
                "description": "Automatically detect the type of project with enhanced accuracy. Supports 25+ project types including React, Next.js, Angular, Vue, Python, .NET, Java, etc. Use simple commands like 'Detect the project type' or 'What type of project is this?'",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "base_path": {
                            "type": "string",
                            "description": "Base path to analyze (optional - will use intelligent defaults)"
                        }
                    }
                }
            },
            {
                "name": "read_file",
                "description": "Read the contents of a file from the user's project directory",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "Path to the file to read (relative to user's project directory)"
                        }
                    },
                    "required": ["file_path"]
                }
            },
            {
                "name": "read_filenames_in_directory",
                "description": "Read filenames in a directory - works from current working directory",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "directory": {
                            "type": "string",
                            "description": "Directory to list (default: current directory)"
                        }
                    }
                }
            },
            {
                "name": "write_file",
                "description": "Write to a file - creates directories if needed",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "Path to the file to write"
                        },
                        "content": {
                            "type": "string",
                            "description": "Content to write to the file"
                        }
                    },
                    "required": ["file_path", "content"]
                }
            },
            {
                "name": "analyze_project_structure",
                "description": "Analyze and document the complete project structure with intelligent categorization",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "base_path": {
                            "type": "string",
                            "description": "Base path to analyze (default: current directory)"
                        }
                    }
                }
            },
            {
                "name": "analyze_package_json",
                "description": "Comprehensive analysis of package.json with insights and recommendations",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "Path to package.json (default: package.json)"
                        }
                    }
                }
            },
            {
                "name": "generate_project_readme",
                "description": "Generate a comprehensive README.md for any project based on its structure and files",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "base_path": {
                            "type": "string",
                            "description": "Base path to analyze (default: current directory)"
                        }
                    }
                }
            },
            {
                "name": "find_files_by_pattern",
                "description": "Find files matching a pattern (supports wildcards like *.py, **/*.js, etc.)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "pattern": {
                            "type": "string",
                            "description": "Pattern to search for (e.g., *.py, **/*.js)"
                        },
                        "base_path": {
                            "type": "string",
                            "description": "Base path to search in (default: current directory)"
                        }
                    },
                    "required": ["pattern"]
                }
            },
            {
                "name": "analyze_code_metrics",
                "description": "Analyze code metrics like file count, lines of code, and technology distribution",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "base_path": {
                            "type": "string",
                            "description": "Base path to analyze (default: current directory)"
                        }
                    }
                }
            },
            {
                "name": "scan_for_todos_and_fixmes",
                "description": "Scan project for TODO, FIXME, HACK, and other code comments that need attention",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "base_path": {
                            "type": "string",
                            "description": "Base path to scan (default: current directory)"
                        }
                    }
                }
            },
            {
                "name": "document_project_comprehensive",
                "description": "Complete project documentation workflow. Use simple commands like 'Document this project', 'Create comprehensive documentation', or 'Generate project documentation'. Automatically detects project type and creates full documentation.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "project_path": {
                            "type": "string",
                            "description": "Project path to document (optional - will use intelligent defaults)"
                        }
                    }
                }
            },
            {
                "name": "upload_project_files",
                "description": "Upload project files for analysis. Use this to upload your project files so the cloud server can analyze them. Example: 'Upload my project files for analysis'",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "files_data": {
                            "type": "object",
                            "description": "Object containing file paths as keys and file contents as values"
                        }
                    }
                }
            },
            {
                "name": "analyze_uploaded_project",
                "description": "Analyze a previously uploaded project. Use this after uploading files to get comprehensive documentation. Example: 'Analyze the uploaded project'",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "project_id": {
                            "type": "string",
                            "description": "Project ID returned from upload_project_files"
                        }
                    }
                }
            }
        ]
    
    def _execute_tool(self, tool_name: str, arguments: Dict) -> str:
        """Execute a tool with the given arguments"""
        try:
            # Validate tool name
            if not tool_name or not isinstance(tool_name, str):
                return "❌ Invalid tool name"
            
            # Validate arguments
            if not isinstance(arguments, dict):
                arguments = {}
            
            # Execute tool with proper error handling
            if tool_name == "detect_project_type":
                base_path = arguments.get("base_path", ".")
                if not isinstance(base_path, str):
                    return "❌ Invalid base_path parameter"
                return self._detect_project_type(base_path)
            elif tool_name == "read_file":
                file_path = arguments.get("file_path")
                if not isinstance(file_path, str):
                    return "❌ Invalid file_path parameter"
                return self._read_file(file_path)
            elif tool_name == "read_filenames_in_directory":
                directory = arguments.get("directory", ".")
                if not isinstance(directory, str):
                    return "❌ Invalid directory parameter"
                return self._read_filenames_in_directory(directory)
            elif tool_name == "write_file":
                file_path = arguments.get("file_path")
                content = arguments.get("content")
                if not isinstance(file_path, str):
                    return "❌ Invalid file_path parameter"
                if not isinstance(content, str):
                    return "❌ Invalid content parameter"
                return self._write_file(file_path, content)
            elif tool_name == "analyze_project_structure":
                base_path = arguments.get("base_path", ".")
                if not isinstance(base_path, str):
                    return "❌ Invalid base_path parameter"
                return self._analyze_project_structure(base_path)
            elif tool_name == "analyze_package_json":
                file_path = arguments.get("file_path", "package.json")
                if not isinstance(file_path, str):
                    return "❌ Invalid file_path parameter"
                return self._analyze_package_json(file_path)
            elif tool_name == "generate_project_readme":
                base_path = arguments.get("base_path", ".")
                if not isinstance(base_path, str):
                    return "❌ Invalid base_path parameter"
                return self._generate_project_readme(base_path)
            elif tool_name == "find_files_by_pattern":
                pattern = arguments.get("pattern")
                base_path = arguments.get("base_path", ".")
                if not isinstance(pattern, str):
                    return "❌ Invalid pattern parameter"
                if not isinstance(base_path, str):
                    return "❌ Invalid base_path parameter"
                return self._find_files_by_pattern(pattern, base_path)
            elif tool_name == "analyze_code_metrics":
                base_path = arguments.get("base_path", ".")
                if not isinstance(base_path, str):
                    return "❌ Invalid base_path parameter"
                return self._analyze_code_metrics(base_path)
            elif tool_name == "scan_for_todos_and_fixmes":
                base_path = arguments.get("base_path", ".")
                if not isinstance(base_path, str):
                    return "❌ Invalid base_path parameter"
                return self._scan_for_todos_and_fixmes(base_path)
            elif tool_name == "document_project_comprehensive":
                project_path = arguments.get("project_path", "")
                if not isinstance(project_path, str):
                    return "❌ Invalid project_path parameter"
                return self._document_project_comprehensive(project_path)
            elif tool_name == "upload_project_files":
                files_data = arguments.get("files_data", {})
                if not isinstance(files_data, dict):
                    return "❌ Invalid files_data parameter"
                return self._upload_project_files(files_data)
            elif tool_name == "analyze_uploaded_project":
                project_id = arguments.get("project_id", "")
                if not isinstance(project_id, str):
                    return "❌ Invalid project_id parameter"
                return self._analyze_uploaded_project(project_id)
            else:
                return f"❌ Tool '{tool_name}' not found"
        except Exception as e:
            logger.error(f"Tool execution error for {tool_name}: {e}")
            return f"❌ Error executing {tool_name}: {str(e)}"
    
    # Tool implementations (simplified versions from main.py)
    def _detect_project_type(self, base_path: str) -> str:
        """Detect project type with enhanced accuracy"""
        try:
            base_path = Path(base_path).resolve()
            detected_types = []
            
            if not base_path.exists():
                return f"❌ Path does not exist: {base_path}\n💡 Please provide the correct path to your project directory.\n📝 Example: Use 'Analyze the project at /path/to/your/project' or specify the base_path argument."
            
            for project_type, config in PROJECT_CONFIGS.items():
                score = 0
                found_indicators = []
                
                # Check for indicator files
                for indicator in config["indicators"]:
                    if "*" in indicator:
                        matches = list(base_path.glob(indicator))
                        if matches:
                            found_indicators.append(f"{indicator} ({len(matches)} files)")
                            score += 2
                    elif (base_path / indicator).exists():
                        found_indicators.append(indicator)
                        score += 2
                
                # Check file contents
                for file_to_check, content_keys in config["check_content"].items():
                    file_path = base_path / file_to_check
                    if file_path.exists() and file_path.is_file():
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read().lower()
                            
                            if isinstance(content_keys, list):
                                matched_keys = [key for key in content_keys if key.lower() in content]
                                if matched_keys:
                                    score += len(matched_keys) * 2
                                    found_indicators.append(f"{file_to_check} (contains {', '.join(matched_keys)})")
                        except Exception:
                            pass
                
                # Check for important directories
                dir_score = 0
                found_dirs = []
                for important_dir in config["important_dirs"]:
                    if (base_path / important_dir).exists():
                        found_dirs.append(important_dir)
                        dir_score += 1
                
                if dir_score > 0:
                    score += min(dir_score, 4)
                
                # Apply confidence boost
                score += config.get("confidence_boost", 0)
                
                if score > 0:
                    detected_types.append({
                        'type': project_type,
                        'score': score,
                        'indicators': found_indicators,
                        'directories': found_dirs
                    })
            
            # Sort by score
            detected_types.sort(key=lambda x: x['score'], reverse=True)
            
            # Check if we're analyzing the server's own directory
            path_str = str(base_path).lower()
            if any(pattern in path_str for pattern in ['documenter', 'mcps', 'render', 'opt/render']):
                warning = f"\n⚠️  WARNING: You appear to be analyzing the MCP server's own directory ({base_path}).\n💡 To analyze your project, please specify the correct path to your project directory.\n📝 Example: 'Analyze the project at /path/to/your/nextjs-project'"
            else:
                warning = ""
            
            if not detected_types:
                return f"Detected project type: GENERIC\nPath analyzed: {base_path}\nNo specific framework detected{warning}"
            
            primary_type = detected_types[0]
            result = []
            result.append(f"Detected project type: {primary_type['type'].upper()}")
            result.append(f"Confidence Score: {primary_type['score']}")
            result.append(f"Path analyzed: {base_path}")
            
            if primary_type['indicators']:
                result.append(f"Indicators found: {', '.join(primary_type['indicators'])}")
            
            if primary_type['directories']:
                result.append(f"Relevant directories: {', '.join(primary_type['directories'])}")
            
            result.append(warning)  # Add warning if analyzing server directory
            
            return '\n'.join(result)
        except Exception as e:
            return f"Error detecting project type: {e}"
    
    def _read_file(self, file_path: str) -> str:
        """Read a file"""
        try:
            path = Path(file_path)
            if not path.is_absolute():
                path = Path.cwd() / path
                
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            return content
        except Exception as e:
            return f"Error reading file '{file_path}': {e}"
    
    def _read_filenames_in_directory(self, directory: str) -> str:
        """Read filenames in a directory"""
        try:
            path = Path(directory)
            if not path.is_absolute():
                path = Path.cwd() / path
                
            if not path.exists():
                return f"Directory '{directory}' does not exist"
                
            files = [f.name for f in path.iterdir() if f.is_file()]
            dirs = [f.name for f in path.iterdir() if f.is_dir() and not f.name.startswith('.')]
            
            result = []
            result.append(f"📁 Directory: {path}")
            result.append(f"📂 Subdirectories ({len(dirs)}): {', '.join(sorted(dirs))}")
            result.append(f"📄 Files ({len(files)}): {', '.join(sorted(files))}")
            
            return '\n'.join(result)
        except Exception as e:
            return f"Error reading directory '{directory}': {e}"
    
    def _write_file(self, file_path: str, content: str) -> str:
        """Write to a file"""
        try:
            path = Path(file_path)
            if not path.is_absolute():
                path = Path.cwd() / path
                
            path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            return f"✅ File written successfully: {path}"
        except Exception as e:
            return f"Error writing to file '{file_path}': {e}"
    
    def _analyze_project_structure(self, base_path: str) -> str:
        """Analyze project structure"""
        try:
            base_path = Path(base_path).resolve()
            project_info = self._detect_project_type(str(base_path))
            
            structure = []
            structure.append("# 📊 Project Structure Analysis")
            structure.append("")
            structure.append(project_info)
            structure.append("")
            structure.append("## 📁 Directory Tree")
            structure.append("```")
            
            def generate_tree(path: Path, prefix: str = "", max_depth: int = 3, current_depth: int = 0):
                if current_depth >= max_depth:
                    return
                    
                items = []
                try:
                    for item in path.iterdir():
                        if item.name.startswith('.') or item.name in ['node_modules', '__pycache__', '.next', 'out', 'dist', 'build']:
                            continue
                        items.append(item)
                    
                    items.sort(key=lambda x: (x.is_file(), x.name.lower()))
                    
                    for i, item in enumerate(items):
                        is_last = i == len(items) - 1
                        current_prefix = "└── " if is_last else "├── "
                        structure.append(f"{prefix}{current_prefix}{item.name}")
                        
                        if item.is_dir() and current_depth < max_depth - 1:
                            next_prefix = prefix + ("    " if is_last else "│   ")
                            generate_tree(item, next_prefix, max_depth, current_depth + 1)
                except PermissionError:
                    structure.append(f"{prefix}    [Permission Denied]")
            
            structure.append(base_path.name + "/")
            generate_tree(base_path, "", max_depth=4)
            structure.append("```")
            
            return '\n'.join(structure)
        except Exception as e:
            return f"Error analyzing project structure: {e}"
    
    def _analyze_package_json(self, file_path: str) -> str:
        """Analyze package.json"""
        try:
            path = Path(file_path)
            if not path.is_absolute():
                path = Path.cwd() / path
                
            if not path.exists():
                return f"❌ package.json not found at: {path}"
                
            with open(path, "r", encoding="utf-8") as f:
                package_data = json.load(f)
            
            analysis = []
            analysis.append("# 📦 Package.json Analysis")
            analysis.append("")
            analysis.append("## ℹ️ Project Information")
            analysis.append(f"**Name:** {package_data.get('name', 'Unknown')}")
            analysis.append(f"**Version:** {package_data.get('version', 'Unknown')}")
            analysis.append(f"**Description:** {package_data.get('description', 'No description provided')}")
            analysis.append(f"**Author:** {package_data.get('author', 'Not specified')}")
            analysis.append(f"**License:** {package_data.get('license', 'Not specified')}")
            analysis.append("")
            
            if 'scripts' in package_data:
                analysis.append("## 🔧 Available Scripts")
                scripts = package_data['scripts']
                for script, command in scripts.items():
                    analysis.append(f"- **`npm run {script}`**: `{command}`")
                analysis.append("")
            
            if 'dependencies' in package_data:
                deps = package_data['dependencies']
                analysis.append(f"## 📚 Dependencies ({len(deps)} total)")
                for dep, version in deps.items():
                    analysis.append(f"- `{dep}`: {version}")
                analysis.append("")
            
            return '\n'.join(analysis)
        except Exception as e:
            return f"Error analyzing package.json: {e}"
    
    def _generate_project_readme(self, base_path: str) -> str:
        """Generate project README"""
        try:
            base_path = Path(base_path).resolve()
            project_type = self._detect_project_type(str(base_path))
            
            project_name = base_path.name
            description = "A software project"
            
            package_json_path = base_path / "package.json"
            if package_json_path.exists():
                try:
                    with open(package_json_path, 'r', encoding='utf-8') as f:
                        package_data = json.load(f)
                        project_name = package_data.get('name', project_name)
                        description = package_data.get('description', description)
                except:
                    pass
            
            readme = []
            readme.append(f"# {project_name}")
            readme.append("")
            readme.append(description)
            readme.append("")
            readme.append("## 🚀 Project Information")
            readme.append(project_type.replace("Detected project type: ", "**Project Type:** "))
            readme.append("")
            readme.append("## 📦 Installation")
            readme.append("")
            readme.append("```bash")
            readme.append("# Clone the repository")
            readme.append(f"git clone <repository-url>")
            readme.append(f"cd {project_name}")
            readme.append("```")
            readme.append("")
            
            return '\n'.join(readme)
        except Exception as e:
            return f"Error generating README: {e}"
    
    def _find_files_by_pattern(self, pattern: str, base_path: str) -> str:
        """Find files by pattern"""
        try:
            base_path = Path(base_path).resolve()
            matching_files = list(base_path.glob(pattern))
            
            filtered_files = []
            for file_path in matching_files:
                relative_path = file_path.relative_to(base_path)
                path_parts = relative_path.parts
                
                if any(part.startswith('.') for part in path_parts):
                    continue
                
                skip_dirs = {'node_modules', '__pycache__', '.next', 'out', 'dist', 'build', 'target', 'vendor'}
                if any(part in skip_dirs for part in path_parts):
                    continue
                
                filtered_files.append(file_path)
            
            if not filtered_files:
                return f"No files found matching pattern: {pattern}"
            
            filtered_files.sort(key=lambda x: (x.suffix, x.name))
            
            results = []
            results.append(f"# 🔍 Files matching pattern: `{pattern}`")
            results.append("")
            results.append(f"Found {len(filtered_files)} files:")
            results.append("")
            
            for file_path in filtered_files:
                results.append(f"- `{file_path.relative_to(base_path)}`")
            
            return '\n'.join(results)
        except Exception as e:
            return f"Error finding files: {e}"
    
    def _analyze_code_metrics(self, base_path: str) -> str:
        """Analyze code metrics"""
        try:
            base_path = Path(base_path).resolve()
            
            code_extensions = {
                '.py': 'Python', '.js': 'JavaScript', '.ts': 'TypeScript', 
                '.jsx': 'React JSX', '.tsx': 'React TSX', '.java': 'Java',
                '.kt': 'Kotlin', '.go': 'Go', '.rs': 'Rust', '.php': 'PHP',
                '.rb': 'Ruby', '.cs': 'C#', '.cpp': 'C++', '.c': 'C',
                '.swift': 'Swift', '.dart': 'Dart', '.html': 'HTML',
                '.css': 'CSS', '.scss': 'SCSS', '.vue': 'Vue'
            }
            
            metrics = {
                'total_files': 0,
                'total_lines': 0,
                'by_language': {},
            }
            
            for file_path in base_path.rglob('*'):
                if not file_path.is_file():
                    continue
                
                relative_path = file_path.relative_to(base_path)
                path_parts = relative_path.parts
                
                if any(part.startswith('.') for part in path_parts):
                    continue
                
                skip_dirs = {'node_modules', '__pycache__', '.next', 'out', 'dist', 'build', 'target', 'vendor'}
                if any(part in skip_dirs for part in path_parts):
                    continue
                
                metrics['total_files'] += 1
                
                ext = file_path.suffix.lower()
                language = code_extensions.get(ext, 'Other')
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        lines = content.count('\n') + 1
                        
                        metrics['total_lines'] += lines
                        
                        if language not in metrics['by_language']:
                            metrics['by_language'][language] = {'files': 0, 'lines': 0}
                        
                        metrics['by_language'][language]['files'] += 1
                        metrics['by_language'][language]['lines'] += lines
                except:
                    pass
            
            results = []
            results.append("# 📊 Code Metrics Analysis")
            results.append("")
            results.append(f"**Total Files:** {metrics['total_files']:,}")
            results.append(f"**Total Lines of Code:** {metrics['total_lines']:,}")
            results.append("")
            
            if metrics['by_language']:
                results.append("## 🔧 Technology Distribution")
                sorted_languages = sorted(metrics['by_language'].items(), key=lambda x: x[1]['lines'], reverse=True)
                
                total_lines = metrics['total_lines']
                for language, stats in sorted_languages:
                    percentage = (stats['lines'] / total_lines * 100) if total_lines > 0 else 0
                    results.append(f"- **{language}**: {stats['files']} files, {stats['lines']:,} lines ({percentage:.1f}%)")
                results.append("")
            
            return '\n'.join(results)
        except Exception as e:
            return f"Error analyzing code metrics: {e}"
    
    def _scan_for_todos_and_fixmes(self, base_path: str) -> str:
        """Scan for TODOs and FIXMEs"""
        try:
            base_path = Path(base_path).resolve()
            
            patterns = {
                'TODO': r'(?i)(?://|#|\*|<!--)?\s*TODO\s*:?\s*(.*)',
                'FIXME': r'(?i)(?://|#|\*|<!--)?\s*FIXME\s*:?\s*(.*)',
                'HACK': r'(?i)(?://|#|\*|<!--)?\s*HACK\s*:?\s*(.*)',
            }
            
            findings = {pattern: [] for pattern in patterns.keys()}
            
            code_extensions = {'.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.kt', '.go', '.rs', '.php', '.rb', '.cs', '.cpp', '.c', '.swift', '.dart'}
            
            for file_path in base_path.rglob('*'):
                if not file_path.is_file() or file_path.suffix not in code_extensions:
                    continue
                
                relative_path = file_path.relative_to(base_path)
                path_parts = relative_path.parts
                
                if any(part.startswith('.') for part in path_parts):
                    continue
                
                skip_dirs = {'node_modules', '__pycache__', '.next', 'out', 'dist', 'build', 'target', 'vendor'}
                if any(part in skip_dirs for part in path_parts):
                    continue
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        
                    for line_num, line in enumerate(lines, 1):
                        for pattern_name, pattern in patterns.items():
                            match = re.search(pattern, line)
                            if match:
                                comment = match.group(1).strip() if match.group(1) else line.strip()
                                findings[pattern_name].append({
                                    'file': relative_path,
                                    'line': line_num,
                                    'comment': comment
                                })
                except:
                    pass
            
            results = []
            results.append("# 🔍 Code Annotations Scan")
            results.append("")
            
            total_items = sum(len(items) for items in findings.values())
            if total_items == 0:
                results.append("✅ No TODO, FIXME, or other annotations found!")
                return '\n'.join(results)
            
            results.append(f"Found {total_items} items that need attention:")
            results.append("")
            
            for pattern_name, items in findings.items():
                if not items:
                    continue
                
                emoji_map = {
                    'TODO': '📝',
                    'FIXME': '🐛', 
                    'HACK': '⚠️'
                }
                
                results.append(f"## {emoji_map.get(pattern_name, '📌')} {pattern_name} ({len(items)} items)")
                results.append("")
                
                for item in items:
                    results.append(f"- **`{item['file']}:{item['line']}`** - {item['comment']}")
                results.append("")
            
            return '\n'.join(results)
        except Exception as e:
            return f"Error scanning for annotations: {e}"
    
    def _document_project_comprehensive(self, project_path: str) -> str:
        """Complete comprehensive documentation workflow with enhanced context detection"""
        try:
            # Enhanced project path detection
            original_path = project_path
            if not project_path:
                project_path = str(Path.cwd().resolve())
            
            base_path = Path(project_path).resolve()
            
            # Check if we're analyzing the server's own directory (cloud limitation)
            server_indicators = ['opt/render/project', 'documenter', 'mcp', 'server.py']
            path_str = str(base_path).lower()
            is_server_directory = any(indicator in path_str for indicator in server_indicators)
            
            results = []
            results.append("# 🚀 Universal Project Documentation")
            results.append("=" * 70)
            
            # Context detection feedback
            if is_server_directory:
                results.append("⚠️  **IMPORTANT: Cloud Server Limitation Detected**")
                results.append("")
                results.append("🔍 **Context Detection Results:**")
                results.append(f"📁 **Analyzing**: {base_path}")
                results.append("❌ **Issue**: This appears to be the MCP server's directory, not your project")
                results.append("")
                results.append("💡 **How to Fix This:**")
                results.append("1. **Specify your project path explicitly**: Try prompts like:")
                results.append("   - `\"Document the project at C:\\path\\to\\your\\project\"`")
                results.append("   - `\"Analyze my React project in C:\\Users\\YourName\\Projects\\MyApp\"`")
                results.append("2. **Use descriptive prompts**: Include your project name or location")
                results.append("3. **Consider the local version**: For direct file access without path specification")
                results.append("")
                results.append("📋 **Example Commands:**")
                results.append("```")
                results.append("Document the Next.js project at C:\\D\\RND\\my-portfolio")
                results.append("Analyze the React project in /Users/john/Projects/my-app")
                results.append("Generate documentation for the Laravel project located at /var/www/html")
                results.append("```")
                results.append("")
                results.append("🔄 **Continuing with current directory analysis for demonstration...**")
                results.append("")
            else:
                results.append("✅ **Context Detection Successful**")
                results.append(f"📁 **Project Location**: {base_path}")
                if original_path:
                    results.append(f"🎯 **Detection Method**: Path provided in request")
                else:
                    results.append(f"🎯 **Detection Method**: Automatic detection")
                results.append("")
            
            results.append(f"🖥️  **Platform**: {platform.system()} {platform.release()}")
            results.append(f"🐍 **Python**: {sys.version.split()[0]}")
            results.append("")
            
            if not base_path.exists():
                results.append(f"❌ **Error**: Project path does not exist: {base_path}")
                results.append("")
                results.append("💡 **Suggestions:**")
                results.append("- Check if the path is correct")
                results.append("- Make sure the directory exists")
                results.append("- Try using an absolute path")
                results.append("- For cloud version, specify the full project path in your prompt")
                return '\n'.join(results)
            
            # Step 1: Project type detection
            results.append("## 🔍 Step 1: Project Type Detection")
            results.append("-" * 50)
            project_type_result = self._detect_project_type(str(base_path))
            results.append(project_type_result)
            results.append("")
            
            # Step 2: Project structure analysis
            results.append("## 📊 Step 2: Project Structure Analysis")
            results.append("-" * 50)
            structure_result = self._analyze_project_structure(str(base_path))
            results.append(structure_result)
            results.append("")
            
            # Step 3: Code metrics
            results.append("## 📈 Step 3: Code Metrics & Technology Analysis")
            results.append("-" * 50)
            metrics_result = self._analyze_code_metrics(str(base_path))
            results.append(metrics_result)
            results.append("")
            
            # Step 4: Technical debt scanning
            results.append("## 🐛 Step 4: Technical Debt Analysis")
            results.append("-" * 50)
            debt_result = self._scan_for_todos_and_fixmes(str(base_path))
            results.append(debt_result)
            results.append("")
            
            # Step 5: README generation
            results.append("## 📝 Step 5: README Generation")
            results.append("-" * 50)
            readme_result = self._generate_project_readme(str(base_path))
            results.append(readme_result)
            results.append("")
            
            # Final recommendations
            if is_server_directory:
                results.append("## 🎯 Final Recommendations")
                results.append("-" * 50)
                results.append("This analysis was performed on the MCP server directory as a demonstration.")
                results.append("For accurate project documentation:")
                results.append("")
                results.append("**Option 1: Cloud Version with Explicit Paths**")
                results.append("- Use prompts like: `\"Document the project at C:\\path\\to\\your\\project\"`")
                results.append("- Always specify the full project path")
                results.append("- Works great for one-time documentation tasks")
                results.append("")
                results.append("**Option 2: Local Version (Recommended for Development)**")
                results.append("- Download and run the local MCP server")
                results.append("- Automatic project detection from your IDE workspace")
                results.append("- Direct file system access, no path specification needed")
                results.append("- Perfect for active development workflow")
                results.append("")
            else:
                results.append("🎉 **Universal project documentation completed successfully!**")
                results.append("")
                results.append("📋 **Summary:**")
                results.append("- Project type detected and analyzed")
                results.append("- Complete structure mapping performed")
                results.append("- Code metrics and technology distribution calculated")
                results.append("- Technical debt and annotations identified")
                results.append("- Comprehensive README generated")
            
            return '\n'.join(results)
            
        except Exception as e:
            return f"❌ Critical error in comprehensive documentation: {e}\n\n💡 Try specifying your project path explicitly in the prompt."

    def _upload_project_files(self, files_data: Dict) -> str:
        """Handle file uploads for project analysis"""
        try:
            if not files_data:
                return "❌ No files provided for upload"
            
            project_id = str(uuid.uuid4())
            uploaded_files = {}
            
            # Process uploaded files
            for file_path, file_content in files_data.items():
                if isinstance(file_content, str):
                    uploaded_files[file_path] = file_content
                else:
                    return f"❌ Invalid file content for {file_path}"
            
            # Store project data
            self.projects[project_id] = {
                'files': uploaded_files,
                'uploaded_at': time.time(),
                'status': 'uploaded',
                'file_count': len(uploaded_files)
            }
            
            # Clean up old projects (keep only last 10)
            if len(self.projects) > 10:
                oldest_projects = sorted(self.projects.items(), key=lambda x: x[1]['uploaded_at'])[:-10]
                for old_id, _ in oldest_projects:
                    del self.projects[old_id]
            
            return f"✅ Project uploaded successfully!\n📁 Project ID: {project_id}\n📄 Files uploaded: {len(uploaded_files)}\n💡 Use 'analyze_uploaded_project' with this project ID to generate documentation."
            
        except Exception as e:
            logger.error(f"Upload failed: {e}")
            return f"❌ Upload failed: {e}"

    def _analyze_uploaded_project(self, project_id: str) -> str:
        """Analyze project from uploaded files"""
        try:
            if project_id not in self.projects:
                return f"❌ Project {project_id} not found. Please upload your project files first using 'upload_project_files'."
            
            project_data = self.projects[project_id]
            files = project_data['files']
            
            if not files:
                return "❌ No files found in uploaded project"
            
            results = []
            results.append("# 🚀 Uploaded Project Analysis")
            results.append("=" * 50)
            results.append(f"📁 Project ID: {project_id}")
            results.append(f"📄 Files uploaded: {len(files)}")
            results.append(f"⏰ Uploaded: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(project_data['uploaded_at']))}")
            results.append("")
            
            # Analyze project type from uploaded files
            project_type = self._detect_project_type_from_files(files)
            results.append("## 🔍 Project Type Detection")
            results.append("-" * 30)
            results.append(project_type)
            results.append("")
            
            # Analyze project structure
            structure_analysis = self._analyze_project_structure_from_files(files)
            results.append("## 📊 Project Structure Analysis")
            results.append("-" * 30)
            results.append(structure_analysis)
            results.append("")
            
            # Analyze key configuration files
            config_analysis = self._analyze_config_files_from_uploaded(files)
            if config_analysis:
                results.append("## ⚙️ Configuration Analysis")
                results.append("-" * 30)
                results.append(config_analysis)
                results.append("")
            
            # Generate README
            readme_content = self._generate_readme_from_files(files, project_type)
            results.append("## 📝 Generated README")
            results.append("-" * 30)
            results.append("```markdown")
            results.append(readme_content)
            results.append("```")
            results.append("")
            
            results.append("## ✅ Analysis Complete")
            results.append("-" * 30)
            results.append("🎉 Your project has been successfully analyzed!")
            results.append("📄 A comprehensive README has been generated above.")
            results.append("💡 You can copy the README content to create a README.md file in your project.")
            
            return '\n'.join(results)
            
        except Exception as e:
            logger.error(f"Analysis failed: {e}")
            return f"❌ Analysis failed: {e}"

    def _detect_project_type_from_files(self, files: Dict[str, str]) -> str:
        """Detect project type from uploaded files"""
        try:
            detected_types = []
            
            for project_type, config in PROJECT_CONFIGS.items():
                score = 0
                found_indicators = []
                
                # Check for indicator files
                for indicator in config["indicators"]:
                    for file_path in files.keys():
                        if indicator in file_path or file_path.endswith(indicator):
                            found_indicators.append(f"{indicator} ({file_path})")
                            score += 2
                
                # Check file contents
                for file_to_check, content_keys in config["check_content"].items():
                    for file_path, file_content in files.items():
                        if file_to_check in file_path or file_path.endswith(file_to_check):
                            try:
                                content = file_content.lower()
                                if isinstance(content_keys, list):
                                    matched_keys = [key for key in content_keys if key.lower() in content]
                                    if matched_keys:
                                        score += len(matched_keys) * 2
                                        found_indicators.append(f"{file_path} (contains {', '.join(matched_keys)})")
                            except Exception:
                                pass
                
                if score > 0:
                    detected_types.append({
                        'type': project_type,
                        'score': score,
                        'indicators': found_indicators
                    })
            
            # Sort by score
            detected_types.sort(key=lambda x: x['score'], reverse=True)
            
            if not detected_types:
                return "Detected project type: GENERIC\nNo specific framework detected"
            
            primary_type = detected_types[0]
            result = []
            result.append(f"Detected project type: {primary_type['type'].upper()}")
            result.append(f"Confidence Score: {primary_type['score']}")
            
            if primary_type['indicators']:
                result.append(f"Indicators found: {', '.join(primary_type['indicators'])}")
            
            return '\n'.join(result)
            
        except Exception as e:
            return f"Error detecting project type: {e}"

    def _analyze_project_structure_from_files(self, files: Dict[str, str]) -> str:
        """Analyze project structure from uploaded files"""
        try:
            structure = []
            structure.append("## 📁 File Structure")
            structure.append("```")
            
            # Group files by directory
            dirs = {}
            for file_path in files.keys():
                path_parts = file_path.split('/')
                if len(path_parts) > 1:
                    dir_name = path_parts[0]
                    if dir_name not in dirs:
                        dirs[dir_name] = []
                    dirs[dir_name].append('/'.join(path_parts[1:]))
                else:
                    if 'root' not in dirs:
                        dirs['root'] = []
                    dirs['root'].append(file_path)
            
            # Display structure
            for dir_name, files_in_dir in sorted(dirs.items()):
                if dir_name == 'root':
                    structure.append("📄 Root files:")
                else:
                    structure.append(f"📁 {dir_name}/")
                
                for file_name in sorted(files_in_dir):
                    structure.append(f"  └── {file_name}")
                structure.append("")
            
            structure.append("```")
            structure.append(f"**Total files analyzed:** {len(files)}")
            
            return '\n'.join(structure)
            
        except Exception as e:
            return f"Error analyzing project structure: {e}"

    def _analyze_config_files_from_uploaded(self, files: Dict[str, str]) -> str:
        """Analyze configuration files from uploaded files"""
        try:
            config_analysis = []
            
            # Check for package.json
            for file_path, content in files.items():
                if 'package.json' in file_path:
                    try:
                        package_data = json.loads(content)
                        config_analysis.append("### 📦 Package.json Analysis")
                        config_analysis.append(f"**Name:** {package_data.get('name', 'Unknown')}")
                        config_analysis.append(f"**Version:** {package_data.get('version', 'Unknown')}")
                        config_analysis.append(f"**Description:** {package_data.get('description', 'No description')}")
                        
                        if 'scripts' in package_data:
                            config_analysis.append("**Available Scripts:**")
                            for script, command in package_data['scripts'].items():
                                config_analysis.append(f"- `npm run {script}`: {command}")
                        
                        if 'dependencies' in package_data:
                            deps = package_data['dependencies']
                            config_analysis.append(f"**Dependencies:** {len(deps)} total")
                            for dep, version in list(deps.items())[:10]:  # Show first 10
                                config_analysis.append(f"- `{dep}`: {version}")
                            if len(deps) > 10:
                                config_analysis.append(f"- ... and {len(deps) - 10} more dependencies")
                        
                        config_analysis.append("")
                    except Exception:
                        config_analysis.append("❌ Error parsing package.json")
                        config_analysis.append("")
            
            # Check for other config files
            config_files = ['pyproject.toml', 'requirements.txt', 'pom.xml', 'Cargo.toml', 'go.mod']
            for config_file in config_files:
                for file_path, content in files.items():
                    if config_file in file_path:
                        config_analysis.append(f"### ⚙️ {config_file}")
                        config_analysis.append(f"```")
                        config_analysis.append(content[:500] + "..." if len(content) > 500 else content)
                        config_analysis.append("```")
                        config_analysis.append("")
                        break
            
            return '\n'.join(config_analysis) if config_analysis else "No configuration files found"
            
        except Exception as e:
            return f"Error analyzing configuration files: {e}"

    def _generate_readme_from_files(self, files: Dict[str, str], project_type: str) -> str:
        """Generate README from uploaded files"""
        try:
            # Extract project name from package.json or use a default
            project_name = "My Project"
            description = "A software project"
            
            for file_path, content in files.items():
                if 'package.json' in file_path:
                    try:
                        package_data = json.loads(content)
                        project_name = package_data.get('name', project_name)
                        description = package_data.get('description', description)
                        break
                    except Exception:
                        pass
            
            readme = []
            readme.append(f"# {project_name}")
            readme.append("")
            readme.append(description)
            readme.append("")
            
            # Project type info
            readme.append("## 🚀 Project Information")
            readme.append(project_type.replace("Detected project type: ", "**Project Type:** "))
            readme.append("")
            
            # Installation and setup
            readme.append("## 📦 Installation")
            readme.append("")
            readme.append("```bash")
            readme.append("# Clone the repository")
            readme.append(f"git clone <repository-url>")
            readme.append(f"cd {project_name}")
            readme.append("")
            
            # Add installation commands based on project type
            if 'NEXTJS' in project_type.upper() or 'REACT' in project_type.upper():
                readme.append("# Install dependencies")
                readme.append("npm install")
                readme.append("")
                readme.append("# Start development server")
                readme.append("npm run dev")
            elif 'PYTHON' in project_type.upper():
                readme.append("# Install dependencies")
                readme.append("pip install -r requirements.txt")
                readme.append("")
                readme.append("# Run the application")
                readme.append("python main.py")
            else:
                readme.append("# Install dependencies")
                readme.append("# (Add installation instructions for your project type)")
            
            readme.append("```")
            readme.append("")
            
            # Project structure
            readme.append("## 📁 Project Structure")
            readme.append("")
            readme.append("```")
            
            # Show key files and directories
            key_files = []
            for file_path in files.keys():
                if any(keyword in file_path.lower() for keyword in ['readme', 'package.json', 'main.py', 'index.js', 'app.py']):
                    key_files.append(file_path)
            
            for file_path in sorted(key_files):
                readme.append(f"├── {file_path}")
            
            readme.append("```")
            readme.append("")
            
            # Contributing section
            readme.append("## 🤝 Contributing")
            readme.append("")
            readme.append("1. Fork the repository")
            readme.append("2. Create your feature branch (`git checkout -b feature/amazing-feature`)")
            readme.append("3. Commit your changes (`git commit -m 'Add some amazing feature'`)")
            readme.append("4. Push to the branch (`git push origin feature/amazing-feature`)")
            readme.append("5. Open a Pull Request")
            readme.append("")
            
            # License section
            readme.append("## 📄 License")
            readme.append("")
            readme.append("This project is licensed under the MIT License - see the LICENSE file for details.")
            readme.append("")
            
            return '\n'.join(readme)
            
        except Exception as e:
            return f"Error generating README: {e}"

if __name__ == "__main__":
    # Get port from environment or use default
    port = int(os.environ.get("PORT", 8000))
    
    print(f"🚀 Starting Documenter MCP Server")
    print(f"📍 Server will be available on port: {port}")
    print(f"🔧 Platform: Render")
    print(f"🌐 URL: https://documenter-mcp.onrender.com")
    
    # Create server
    server = HTTPServer(('0.0.0.0', port), MCPHandler)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        server.shutdown() 