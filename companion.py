#!/usr/bin/env python3
"""
Documenter MCP Local Companion Script
=====================================

Lightweight companion for hybrid cloud-local project analysis.
This script runs locally to analyze user's project files and 
communicate securely with the cloud MCP server.

Version: 1.0.0
Size: < 50KB (optimized for quick download)
Security: Read-only, user-controlled, transparent
"""

import os
import sys
import json
import hashlib
import mimetypes
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
import tempfile
import argparse
import logging

# Version and metadata
COMPANION_VERSION = "1.0.0"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB limit per file
SUPPORTED_TEXT_EXTENSIONS = {
    '.py', '.js', '.ts', '.jsx', '.tsx', '.html', '.css', '.scss', '.sass',
    '.json', '.xml', '.yaml', '.yml', '.md', '.txt', '.env', '.gitignore',
    '.dockerfile', '.sql', '.sh', '.bat', '.ps1', '.php', '.rb', '.go',
    '.rs', '.java', '.cs', '.cpp', '.c', '.h', '.hpp', '.swift', '.kt',
    '.dart', '.vue', '.svelte', '.config', '.conf', '.ini', '.toml'
}

class CompanionLogger:
    """Simple logging for companion operations"""
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        
    def info(self, message: str):
        if self.verbose:
            print(f"[INFO] {message}")
            
    def warning(self, message: str):
        print(f"[WARNING] {message}")
        
    def error(self, message: str):
        print(f"[ERROR] {message}")

class ProjectAnalyzer:
    """Core project analysis functionality"""
    
    def __init__(self, project_path: str, logger: CompanionLogger):
        self.project_path = Path(project_path).resolve()
        self.logger = logger
        self.excluded_dirs = {
            'node_modules', '.git', '__pycache__', '.pytest_cache',
            'venv', 'env', '.env', 'build', 'dist', 'target',
            '.next', '.nuxt', 'coverage', '.coverage', 'logs'
        }
        self.excluded_files = {
            '.DS_Store', 'Thumbs.db', '*.log', '*.tmp', '*.cache'
        }
        
    def is_text_file(self, file_path: Path) -> bool:
        """Check if file is likely a text file"""
        if file_path.suffix.lower() in SUPPORTED_TEXT_EXTENSIONS:
            return True
            
        # Check MIME type for files without clear extensions
        mime_type, _ = mimetypes.guess_type(str(file_path))
        if mime_type and mime_type.startswith('text/'):
            return True
            
        return False
    
    def should_exclude_path(self, path: Path) -> bool:
        """Check if path should be excluded from analysis"""
        # Check if any parent directory is excluded
        for part in path.parts:
            if part in self.excluded_dirs:
                return True
                
        # Check specific file exclusions
        if path.name in self.excluded_files:
            return True
            
        return False
    
    def get_file_info(self, file_path: Path) -> Dict[str, Any]:
        """Get basic file information"""
        try:
            stat = file_path.stat()
            return {
                'path': str(file_path.relative_to(self.project_path)),
                'size': stat.st_size,
                'modified': stat.st_mtime,
                'is_text': self.is_text_file(file_path),
                'extension': file_path.suffix.lower()
            }
        except Exception as e:
            self.logger.warning(f"Could not get info for {file_path}: {e}")
            return None
    
    def read_text_file(self, file_path: Path, max_size: int = MAX_FILE_SIZE) -> Optional[str]:
        """Safely read text file content"""
        try:
            if file_path.stat().st_size > max_size:
                self.logger.warning(f"File {file_path} too large ({file_path.stat().st_size} bytes)")
                return None
                
            # Try different encodings
            encodings = ['utf-8', 'utf-16', 'latin-1', 'cp1252']
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        content = f.read()
                    return content
                except UnicodeDecodeError:
                    continue
                    
            self.logger.warning(f"Could not decode file {file_path}")
            return None
            
        except Exception as e:
            self.logger.warning(f"Could not read file {file_path}: {e}")
            return None
    
    def analyze_project_structure(self) -> Dict[str, Any]:
        """Analyze complete project structure"""
        self.logger.info(f"Analyzing project structure: {self.project_path}")
        
        structure = {
            'project_path': str(self.project_path),
            'project_name': self.project_path.name,
            'total_files': 0,
            'total_size': 0,
            'directories': [],
            'files': [],
            'file_types': {},
            'errors': []
        }
        
        try:
            for root, dirs, files in os.walk(self.project_path):
                root_path = Path(root)
                
                # Skip excluded directories
                if self.should_exclude_path(root_path):
                    continue
                    
                # Filter out excluded subdirectories
                dirs[:] = [d for d in dirs if not self.should_exclude_path(root_path / d)]
                
                # Add directory info
                rel_path = str(root_path.relative_to(self.project_path))
                if rel_path != '.':
                    structure['directories'].append(rel_path)
                
                # Process files
                for file_name in files:
                    file_path = root_path / file_name
                    
                    if self.should_exclude_path(file_path):
                        continue
                    
                    file_info = self.get_file_info(file_path)
                    if file_info:
                        structure['files'].append(file_info)
                        structure['total_files'] += 1
                        structure['total_size'] += file_info['size']
                        
                        # Count file types
                        ext = file_info['extension']
                        structure['file_types'][ext] = structure['file_types'].get(ext, 0) + 1
                        
        except Exception as e:
            error_msg = f"Error analyzing structure: {e}"
            self.logger.error(error_msg)
            structure['errors'].append(error_msg)
        
        self.logger.info(f"Found {structure['total_files']} files in {len(structure['directories'])} directories")
        return structure
    
    def detect_project_type(self) -> Dict[str, Any]:
        """Detect project type based on files and structure"""
        self.logger.info("Detecting project type...")
        
        indicators = {
            'package.json': 'nodejs',
            'requirements.txt': 'python',
            'Pipfile': 'python', 
            'pyproject.toml': 'python',
            'pom.xml': 'java',
            'build.gradle': 'java',
            'Cargo.toml': 'rust',
            'go.mod': 'go',
            'composer.json': 'php',
            'Gemfile': 'ruby',
            '*.csproj': 'csharp',
            '*.sln': 'csharp',
            'angular.json': 'angular',
            'next.config.js': 'nextjs',
            'nuxt.config.js': 'nuxtjs',
            'vue.config.js': 'vue',
            'svelte.config.js': 'svelte',
            'gatsby-config.js': 'gatsby',
            'Dockerfile': 'docker',
            'docker-compose.yml': 'docker',
            'terraform.tf': 'terraform'
        }
        
        detected_types = {}
        confidence_scores = {}
        
        for file_pattern, project_type in indicators.items():
            if '*' in file_pattern:
                # Handle wildcard patterns
                pattern = file_pattern.replace('*', '')
                matches = list(self.project_path.glob(f"**/*{pattern}"))
            else:
                # Direct file check
                matches = [self.project_path / file_pattern] if (self.project_path / file_pattern).exists() else []
            
            if matches:
                detected_types[project_type] = detected_types.get(project_type, 0) + len(matches)
                confidence_scores[project_type] = confidence_scores.get(project_type, 0) + len(matches)
        
        # Additional heuristics
        if (self.project_path / 'src').exists() and (self.project_path / 'public').exists():
            confidence_scores['react'] = confidence_scores.get('react', 0) + 2
            
        if (self.project_path / 'pages').exists():
            confidence_scores['nextjs'] = confidence_scores.get('nextjs', 0) + 3
        
        # Find best match
        if confidence_scores:
            best_type = max(confidence_scores.items(), key=lambda x: x[1])
            return {
                'detected_type': best_type[0],
                'confidence': best_type[1],
                'all_detected': confidence_scores,
                'indicators_found': detected_types
            }
        else:
            return {
                'detected_type': 'unknown',
                'confidence': 0,
                'all_detected': {},
                'indicators_found': {}
            }
    
    def get_important_files(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get content of important configuration and documentation files"""
        self.logger.info("Reading important project files...")
        
        important_patterns = [
            'README*', 'readme*', 'package.json', 'requirements.txt',
            'Pipfile', 'pyproject.toml', 'setup.py', 'Dockerfile',
            '*.config.js', '*.config.ts', 'tsconfig.json', 
            'angular.json', 'next.config.*', 'nuxt.config.*',
            'vite.config.*', 'webpack.config.*', '.env.example',
            'docker-compose.yml', 'Makefile', 'LICENSE*'
        ]
        
        important_files = []
        file_count = 0
        
        for pattern in important_patterns:
            if file_count >= limit:
                break
                
            matches = list(self.project_path.glob(pattern))
            for file_path in matches:
                if file_count >= limit:
                    break
                    
                if self.should_exclude_path(file_path) or not file_path.is_file():
                    continue
                
                if self.is_text_file(file_path):
                    content = self.read_text_file(file_path)
                    if content:
                        important_files.append({
                            'path': str(file_path.relative_to(self.project_path)),
                            'content': content[:5000],  # Limit content size
                            'size': len(content),
                            'truncated': len(content) > 5000
                        })
                        file_count += 1
        
        self.logger.info(f"Read {len(important_files)} important files")
        return important_files

class SecureCommunicator:
    """Handle secure communication with cloud server"""
    
    def __init__(self, logger: CompanionLogger):
        self.logger = logger
    
    def create_analysis_package(self, project_data: Dict[str, Any], user_preferences: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create secure package for cloud transmission"""
        
        # Apply privacy filters
        if user_preferences and user_preferences.get('exclude_content', False):
            # Remove file contents if user prefers privacy
            if 'important_files' in project_data:
                for file_info in project_data['important_files']:
                    file_info['content'] = '[CONTENT EXCLUDED BY USER PREFERENCE]'
        
        # Create metadata hash for integrity
        package = {
            'companion_version': COMPANION_VERSION,
            'analysis_timestamp': __import__('time').time(),
            'project_data': project_data,
            'user_preferences': user_preferences or {},
            'integrity_hash': None
        }
        
        # Calculate integrity hash
        package_str = json.dumps(package, sort_keys=True, default=str)
        package['integrity_hash'] = hashlib.sha256(package_str.encode()).hexdigest()[:16]
        
        return package

def main():
    """Main companion execution"""
    parser = argparse.ArgumentParser(description='Documenter MCP Local Companion')
    parser.add_argument('--project-path', '-p', default='.', help='Project path to analyze')
    parser.add_argument('--output', '-o', help='Output file for analysis results')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose logging')
    parser.add_argument('--exclude-content', action='store_true', help='Exclude file contents (privacy mode)')
    parser.add_argument('--version', action='store_true', help='Show version')
    
    args = parser.parse_args()
    
    if args.version:
        print(f"Documenter MCP Companion v{COMPANION_VERSION}")
        return
    
    logger = CompanionLogger(verbose=args.verbose)
    logger.info(f"Starting Documenter Companion v{COMPANION_VERSION}")
    
    try:
        # Initialize analyzer
        analyzer = ProjectAnalyzer(args.project_path, logger)
        
        # Perform analysis
        logger.info("Starting project analysis...")
        project_data = {
            'structure': analyzer.analyze_project_structure(),
            'project_type': analyzer.detect_project_type(),
            'important_files': analyzer.get_important_files()
        }
        
        # Create secure package
        communicator = SecureCommunicator(logger)
        user_preferences = {
            'exclude_content': args.exclude_content
        }
        
        package = communicator.create_analysis_package(project_data, user_preferences)
        
        # Output results
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(package, f, indent=2, default=str)
            logger.info(f"Analysis saved to {args.output}")
        else:
            print(json.dumps(package, indent=2, default=str))
        
        logger.info("Analysis completed successfully")
        
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 