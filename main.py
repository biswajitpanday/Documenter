from mcp.server.fastmcp import FastMCP
import os
import json
import re
import sys
import platform
import subprocess
from pathlib import Path
from typing import List, Dict, Optional, Tuple

# Initialize MCP server with clear description
mcp = FastMCP(
    "Universal Project Documenter",
    description="Intelligent documentation generator for any project type. Automatically detects project structure, analyzes dependencies, and generates comprehensive documentation."
)

# Enhanced project type detection with more comprehensive patterns
PROJECT_CONFIGS = {
    "nextjs": {
        "indicators": ["next.config.js", "next.config.ts", "next.config.mjs", "package.json"],
        "check_content": {"package.json": ["next", "@next/"]},
        "important_dirs": ["app", "pages", "components", "src", "public", "styles"],
        "important_files": ["package.json", "README.md", "tsconfig.json", "tailwind.config.js", "next.config.*"],
        "confidence_boost": 3
    },
    "react": {
        "indicators": ["package.json"],
        "check_content": {"package.json": ["react", "react-dom", "react-scripts", "@types/react"]},
        "important_dirs": ["src", "components", "public", "build"],
        "important_files": ["package.json", "README.md", "tsconfig.json", "src/App.*"],
        "confidence_boost": 2
    },
    "angular": {
        "indicators": ["angular.json", "package.json"],
        "check_content": {"package.json": ["@angular/", "angular"], "angular.json": ["@angular"]},
        "important_dirs": ["src", "app", "components", "services", "modules"],
        "important_files": ["angular.json", "package.json", "tsconfig.json", "karma.conf.js"],
        "confidence_boost": 3
    },
    "vue": {
        "indicators": ["vue.config.js", "vite.config.js", "package.json"],
        "check_content": {"package.json": ["vue", "@vue/", "nuxt"]},
        "important_dirs": ["src", "components", "views", "router", "store"],
        "important_files": ["package.json", "vue.config.js", "vite.config.js", "README.md"],
        "confidence_boost": 2
    },
    "svelte": {
        "indicators": ["svelte.config.js", "package.json"],
        "check_content": {"package.json": ["svelte", "@sveltejs/"]},
        "important_dirs": ["src", "static", "build"],
        "important_files": ["svelte.config.js", "package.json", "README.md"],
        "confidence_boost": 2
    },
    "nodejs": {
        "indicators": ["package.json", "server.js", "app.js", "index.js"],
        "check_content": {"package.json": ["express", "node", "fastify", "koa"]},
        "important_dirs": ["src", "lib", "routes", "controllers", "middleware"],
        "important_files": ["package.json", "README.md", "index.js", "server.js"],
        "confidence_boost": 1
    },
    "dotnet": {
        "indicators": [".csproj", ".sln", ".vbproj", ".fsproj", "global.json", "Directory.Build.props"],
        "check_content": {},
        "important_dirs": ["Controllers", "Views", "Models", "Services", "Data", "wwwroot"],
        "important_files": [".csproj", ".sln", "appsettings.json", "Program.cs", "Startup.cs"],
        "confidence_boost": 3
    },
    "java": {
        "indicators": ["pom.xml", "build.gradle", "gradlew", "build.xml", "settings.gradle"],
        "check_content": {"pom.xml": ["java", "maven"], "build.gradle": ["java", "kotlin"]},
        "important_dirs": ["src/main/java", "src/test/java", "src/main/resources", "target", "build"],
        "important_files": ["pom.xml", "build.gradle", "README.md", "application.properties"],
        "confidence_boost": 2
    },
    "kotlin": {
        "indicators": ["build.gradle.kts", "settings.gradle.kts", "gradle.properties"],
        "check_content": {"build.gradle.kts": ["kotlin", "org.jetbrains.kotlin"]},
        "important_dirs": ["src/main/kotlin", "src/test/kotlin", "src/main/resources"],
        "important_files": ["build.gradle.kts", "settings.gradle.kts", "README.md"],
        "confidence_boost": 2
    },
    "go": {
        "indicators": ["go.mod", "go.sum", "main.go", "Makefile"],
        "check_content": {"go.mod": ["module ", "go "]},
        "important_dirs": ["cmd", "pkg", "internal", "api", "web", "docs"],
        "important_files": ["go.mod", "go.sum", "main.go", "README.md", "Makefile"],
        "confidence_boost": 2
    },
    "rust": {
        "indicators": ["Cargo.toml", "Cargo.lock", "src/main.rs", "src/lib.rs"],
        "check_content": {"Cargo.toml": ["[package]", "edition = "]},
        "important_dirs": ["src", "tests", "examples", "benches", "target"],
        "important_files": ["Cargo.toml", "Cargo.lock", "README.md", "main.rs", "lib.rs"],
        "confidence_boost": 3
    },
    "php": {
        "indicators": ["composer.json", "composer.lock", "index.php", "artisan"],
        "check_content": {"composer.json": ["php", "laravel", "symfony"]},
        "important_dirs": ["src", "app", "public", "vendor", "tests"],
        "important_files": ["composer.json", "index.php", "README.md", ".htaccess"],
        "confidence_boost": 1
    },
    "laravel": {
        "indicators": ["artisan", "composer.json", "config/app.php"],
        "check_content": {"composer.json": ["laravel/framework", "laravel"]},
        "important_dirs": ["app", "config", "database", "resources", "routes", "storage"],
        "important_files": ["artisan", "composer.json", ".env.example", "webpack.mix.js"],
        "confidence_boost": 3
    },
    "symfony": {
        "indicators": ["symfony.lock", "composer.json", "bin/console"],
        "check_content": {"composer.json": ["symfony/"]},
        "important_dirs": ["src", "config", "templates", "public", "var"],
        "important_files": ["composer.json", "symfony.lock", "README.md"],
        "confidence_boost": 3
    },
    "flutter": {
        "indicators": ["pubspec.yaml", "pubspec.lock", "android/", "ios/"],
        "check_content": {"pubspec.yaml": ["flutter:", "sdk: flutter"]},
        "important_dirs": ["lib", "test", "android", "ios", "web", "assets"],
        "important_files": ["pubspec.yaml", "README.md", "analysis_options.yaml"],
        "confidence_boost": 3
    },
    "swift": {
        "indicators": ["Package.swift", "*.xcodeproj", "*.xcworkspace", "Podfile"],
        "check_content": {"Package.swift": ["swift-tools-version"]},
        "important_dirs": ["Sources", "Tests", "Package.swift"],
        "important_files": ["Package.swift", "README.md", "*.swift"],
        "confidence_boost": 2
    },
    "ruby": {
        "indicators": ["Gemfile", "Gemfile.lock", "Rakefile", ".ruby-version"],
        "check_content": {"Gemfile": ["ruby ", "gem "]},
        "important_dirs": ["app", "config", "db", "lib", "test", "spec"],
        "important_files": ["Gemfile", "Rakefile", "README.md", "config.ru"],
        "confidence_boost": 1
    },
    "rails": {
        "indicators": ["Gemfile", "config/application.rb", "bin/rails"],
        "check_content": {"Gemfile": ["rails", "gem 'rails'"]},
        "important_dirs": ["app", "config", "db", "lib", "test", "spec"],
        "important_files": ["Gemfile", "Rakefile", "config/routes.rb", "config/application.rb"],
        "confidence_boost": 3
    },
    "python": {
        "indicators": ["requirements.txt", "pyproject.toml", "setup.py", "poetry.lock", "Pipfile"],
        "check_content": {"pyproject.toml": ["[tool.poetry]", "[build-system]"]},
        "important_dirs": ["src", "lib", "tests", "docs", "__pycache__"],
        "important_files": ["requirements.txt", "README.md", "setup.py", "pyproject.toml"],
        "confidence_boost": 1
    },
    "django": {
        "indicators": ["manage.py", "requirements.txt", "settings.py"],
        "check_content": {"requirements.txt": ["django", "Django"], "manage.py": ["django"]},
        "important_dirs": ["apps", "static", "templates", "media", "migrations"],
        "important_files": ["manage.py", "settings.py", "urls.py", "wsgi.py"],
        "confidence_boost": 3
    },
    "fastapi": {
        "indicators": ["main.py", "requirements.txt", "app.py"],
        "check_content": {"requirements.txt": ["fastapi", "uvicorn"], "main.py": ["FastAPI", "from fastapi"]},
        "important_dirs": ["app", "models", "routes", "schemas", "tests"],
        "important_files": ["main.py", "requirements.txt", "README.md"],
        "confidence_boost": 3
    },
    "flask": {
        "indicators": ["app.py", "requirements.txt", "wsgi.py"],
        "check_content": {"requirements.txt": ["flask", "Flask"], "app.py": ["Flask", "from flask"]},
        "important_dirs": ["templates", "static", "blueprints"],
        "important_files": ["app.py", "requirements.txt", "README.md"],
        "confidence_boost": 2
    },
    "gradle": {
        "indicators": ["build.gradle", "gradlew", "settings.gradle"],
        "check_content": {},
        "important_dirs": ["src", "build", "gradle"],
        "important_files": ["build.gradle", "settings.gradle", "gradle.properties"],
        "confidence_boost": 1
    },
    "maven": {
        "indicators": ["pom.xml"],
        "check_content": {"pom.xml": ["<groupId>", "<artifactId>"]},
        "important_dirs": ["src/main", "src/test", "target"],
        "important_files": ["pom.xml", "README.md"],
        "confidence_boost": 2
    },
    "docker": {
        "indicators": ["Dockerfile", "docker-compose.yml", "docker-compose.yaml", ".dockerignore"],
        "check_content": {"Dockerfile": ["FROM ", "RUN ", "COPY "]},
        "important_dirs": ["docker", "scripts"],
        "important_files": ["Dockerfile", "docker-compose.yml", "README.md"],
        "confidence_boost": 1
    },
    "terraform": {
        "indicators": ["main.tf", "variables.tf", "outputs.tf", "terraform.tfvars"],
        "check_content": {},
        "important_dirs": ["modules", "environments"],
        "important_files": ["main.tf", "variables.tf", "outputs.tf", "README.md"],
        "confidence_boost": 2
    },
    "generic": {
        "indicators": [],
        "check_content": {},
        "important_dirs": ["src", "lib", "docs"],
        "important_files": ["README.md"],
        "confidence_boost": 0
    }
}

def _get_enhanced_project_detection() -> Tuple[str, str]:
    """Enhanced project detection using multiple strategies"""
    try:
        # Try to get the actual working directory from various sources
        detected_path = None
        detection_method = "unknown"
        
        # Strategy 1: Environment variables (IDE-specific)
        env_vars = [
            'CURSOR_CWD', 'VSCODE_CWD', 'WINDSURF_CWD', 'CLAUDE_CWD',
            'PWD', 'CD', 'INIT_CWD', 'PROJECT_ROOT', 'WORKSPACE_FOLDER',
            'npm_config_prefix', 'CARGO_MANIFEST_DIR'
        ]
        
        for env_var in env_vars:
            env_path = os.environ.get(env_var, '')
            if env_path and Path(env_path).exists():
                test_path = Path(env_path).resolve()
                path_str = str(test_path).lower()
                
                # Enhanced exclusion logic
                excluded_patterns = [
                    'documenter', 'mcps', 'mcp-server', 'system32', 'program files',
                    'windows/system', '/usr/bin', '/usr/local/bin', 'node_modules',
                    '.npm', '.yarn', '.pnpm', 'python/site-packages'
                ]
                
                if not any(pattern in path_str for pattern in excluded_patterns):
                    detected_path = str(test_path)
                    detection_method = f"environment variable '{env_var}'"
                    break
        
        # Strategy 2: Process tree analysis
        if not detected_path:
            try:
                import psutil
                current_process = psutil.Process()
                
                # Check parent processes for IDE patterns
                parent = current_process.parent()
                while parent and parent.pid != 1:
                    try:
                        name = parent.name().lower()
                        if any(ide in name for ide in ['cursor', 'code', 'windsurf', 'claude', 'vscode']):
                            cwd = parent.cwd()
                            if cwd and Path(cwd).exists():
                                detected_path = cwd
                                detection_method = f"parent process ({parent.name()}) working directory"
                                break
                        parent = parent.parent()
                    except:
                        break
            except ImportError:
                pass
        
        # Strategy 3: Git repository detection
        if not detected_path:
            current_dir = Path.cwd().resolve()
            for parent in [current_dir] + list(current_dir.parents)[:5]:
                if (parent / '.git').exists():
                    parent_str = str(parent).lower()
                    if not any(pattern in parent_str for pattern in ['documenter', 'mcps']):
                        detected_path = str(parent)
                        detection_method = "git repository root"
                        break
        
        # Strategy 4: Project indicators search
        if not detected_path:
            current_dir = Path.cwd().resolve()
            for parent in [current_dir] + list(current_dir.parents)[:3]:
                indicators_found = 0
                for project_type, config in PROJECT_CONFIGS.items():
                    if project_type == "generic":
                        continue
                    
                    for indicator in config["indicators"]:
                        if "*" in indicator:
                            if list(parent.glob(indicator)):
                                indicators_found += 1
                        elif (parent / indicator).exists():
                            indicators_found += 1
                
                if indicators_found >= 2:  # Need at least 2 indicators for confidence
                    parent_str = str(parent).lower()
                    if not any(pattern in parent_str for pattern in ['documenter', 'mcps']):
                        detected_path = str(parent)
                        detection_method = "project indicators"
                        break
        
        # Strategy 5: Fallback with validation
        if not detected_path:
            cwd = Path.cwd().resolve()
            cwd_str = str(cwd).lower()
            if not any(pattern in cwd_str for pattern in ['documenter', 'mcps']):
                detected_path = str(cwd)
                detection_method = "current working directory"
            else:
                # Try parent directory as last resort
                parent = cwd.parent
                detected_path = str(parent)
                detection_method = "parent directory fallback"
        
        return detected_path or str(Path.cwd()), detection_method
        
    except Exception as e:
        return str(Path.cwd()), f"error fallback: {e}"

@mcp.tool()
def detect_project_type(base_path: str = ".") -> str:
    """
    Automatically detect the type of project with enhanced accuracy
    Supports 25+ project types including React, Next.js, Angular, Vue, Python, .NET, Java, etc.
    """
    try:
        # Use enhanced path detection if no specific path provided
        if base_path == ".":
            base_path, detection_method = _get_enhanced_project_detection()
        else:
            detection_method = "specified path"
        
        base_path_obj = Path(base_path).resolve()
        detected_types = []
        
        if not base_path_obj.exists():
            return f"❌ Path does not exist: {base_path_obj}"
        
        for project_type, config in PROJECT_CONFIGS.items():
            if project_type == "generic":
                continue
                
            score = 0
            found_indicators = []
            
            # Check for indicator files with enhanced matching
            for indicator in config["indicators"]:
                if "*" in indicator:  # Handle wildcards
                    matches = list(base_path_obj.glob(indicator))
                    if matches:
                        found_indicators.append(f"{indicator} ({len(matches)} files)")
                        score += 2
                elif (base_path_obj / indicator).exists():
                    found_indicators.append(indicator)
                    score += 2
            
            # Check file contents for specific keywords with enhanced logic
            for file_to_check, content_keys in config["check_content"].items():
                file_path = base_path_obj / file_to_check
                if file_path.exists() and file_path.is_file():
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read().lower()
                            
                        if isinstance(content_keys, list):
                            matched_keys = [key for key in content_keys if key.lower() in content]
                            if matched_keys:
                                score += len(matched_keys) * 2  # More matches = higher score
                                found_indicators.append(f"{file_to_check} (contains {', '.join(matched_keys)})")
                        elif isinstance(content_keys, str) and content_keys.lower() in content:
                            score += 3
                            found_indicators.append(f"{file_to_check} (contains '{content_keys}')")
                    except Exception:
                        pass  # Skip files that can't be read
            
            # Check for important directories
            dir_score = 0
            found_dirs = []
            for important_dir in config["important_dirs"]:
                if (base_path_obj / important_dir).exists():
                    found_dirs.append(important_dir)
                    dir_score += 1
            
            if dir_score > 0:
                score += min(dir_score, 4)  # Cap directory score at 4
            
            # Apply confidence boost
            score += config.get("confidence_boost", 0)
            
            # Only consider if we found some indicators
            if score > 0:
                detected_types.append({
                    'type': project_type,
                    'score': score,
                    'indicators': found_indicators,
                    'directories': found_dirs,
                    'confidence': _calculate_confidence(score, len(found_indicators), len(found_dirs))
                })
        
        # Sort by score (highest first)
        detected_types.sort(key=lambda x: x['score'], reverse=True)
        
        if not detected_types:
            return f"Detected project type: GENERIC\nPath analyzed: {base_path}\nDetection method: {detection_method}\nNo specific framework detected"
        
        # Build enhanced result
        result = []
        primary_type = detected_types[0]
        
        result.append(f"Detected project type: {primary_type['type'].upper()}")
        result.append(f"Confidence Score: {primary_type['score']} ({primary_type['confidence']})")
        result.append(f"Path analyzed: {base_path_obj}")
        result.append(f"Detection method: {detection_method}")
        
        if primary_type['indicators']:
            result.append(f"Indicators found: {', '.join(primary_type['indicators'])}")
        
        if primary_type['directories']:
            result.append(f"Relevant directories: {', '.join(primary_type['directories'])}")
        
        # Show other possible types if score is competitive
        strong_alternatives = [t for t in detected_types[1:] if t['score'] >= primary_type['score'] * 0.6]
        if strong_alternatives:
            result.append("\nOther possible types:")
            for alt_type in strong_alternatives[:3]:  # Show up to 3 alternatives
                result.append(f"- {alt_type['type'].upper()} (score: {alt_type['score']}, {alt_type['confidence']})")
        
        # Add helpful context
        result.append(f"\nFramework ecosystem: {_get_ecosystem_info(primary_type['type'])}")
        
        return '\n'.join(result)
    except Exception as e:
        return f"Error detecting project type: {e}\nPath: {base_path}\nDetection method: {detection_method if 'detection_method' in locals() else 'unknown'}"

def _calculate_confidence(score: int, indicators: int, directories: int) -> str:
    """Calculate confidence level based on detection metrics"""
    if score >= 10 and indicators >= 3:
        return "Very High"
    elif score >= 7 and indicators >= 2:
        return "High"
    elif score >= 4 and indicators >= 1:
        return "Medium"
    elif score >= 2:
        return "Low"
    else:
        return "Very Low"

def _get_ecosystem_info(project_type: str) -> str:
    """Get ecosystem information for the detected project type"""
    ecosystems = {
        "nextjs": "React-based full-stack framework with SSR/SSG",
        "react": "Frontend library for building user interfaces",
        "angular": "Full-featured frontend framework by Google",
        "vue": "Progressive frontend framework",
        "svelte": "Compile-time frontend framework",
        "nodejs": "JavaScript runtime for server-side development",
        "dotnet": "Microsoft's cross-platform development framework",
        "java": "Enterprise-grade object-oriented programming",
        "kotlin": "Modern JVM language, Android development",
        "go": "Google's systems programming language",
        "rust": "Systems programming with memory safety",
        "php": "Server-side scripting language",
        "laravel": "PHP web application framework",
        "symfony": "PHP framework for enterprise applications",
        "flutter": "Google's UI toolkit for mobile/web/desktop",
        "swift": "Apple's programming language for iOS/macOS",
        "ruby": "Dynamic object-oriented programming language",
        "rails": "Ruby web application framework",
        "python": "General-purpose programming language",
        "django": "Python web framework for rapid development",
        "fastapi": "Modern Python API framework",
        "flask": "Lightweight Python web framework",
        "docker": "Containerization platform",
        "terraform": "Infrastructure as Code tool"
    }
    return ecosystems.get(project_type.lower(), "General development project")

@mcp.tool()
def read_file(file_path: str) -> str:
    """
    Read a file - works with both absolute and relative paths from current working directory
    """
    try:
        # Convert to Path object for better path handling
        path = Path(file_path)
        if not path.is_absolute():
            path = Path.cwd() / path
            
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        return content
    except Exception as e:
        return f"Error reading file '{file_path}': {e}"

@mcp.tool()
def read_filenames_in_directory(directory: str = ".") -> str:
    """
    Read filenames in a directory - works from current working directory
    """
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

@mcp.tool()
def write_file(file_path: str, content: str) -> str:
    """
    Write to a file - creates directories if needed
    """
    try:
        path = Path(file_path)
        if not path.is_absolute():
            path = Path.cwd() / path
            
        # Create parent directories if they don't exist
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"✅ File written successfully: {path}"
    except Exception as e:
        return f"Error writing to file '{file_path}': {e}"

@mcp.tool()
def analyze_project_structure(base_path: str = ".") -> str:
    """
    Analyze and document the complete project structure with intelligent categorization
    """
    try:
        base_path = Path(base_path).resolve()
        
        # Detect project type first
        project_info = detect_project_type(str(base_path))
        
        structure = []
        structure.append("# 📊 Project Structure Analysis")
        structure.append("")
        structure.append(project_info)
        structure.append("")
        structure.append("## 📁 Directory Tree")
        structure.append("```")
        
        # Generate tree structure
        def generate_tree(path: Path, prefix: str = "", max_depth: int = 3, current_depth: int = 0):
            if current_depth >= max_depth:
                return
                
            items = []
            try:
                # Get directories and files, skip hidden and build folders
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

@mcp.tool()
def analyze_package_json(file_path: str = "package.json") -> str:
    """
    Comprehensive analysis of package.json with insights and recommendations
    """
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
        
        # Basic info
        analysis.append("## ℹ️ Project Information")
        analysis.append(f"**Name:** {package_data.get('name', 'Unknown')}")
        analysis.append(f"**Version:** {package_data.get('version', 'Unknown')}")
        analysis.append(f"**Description:** {package_data.get('description', 'No description provided')}")
        analysis.append(f"**Author:** {package_data.get('author', 'Not specified')}")
        analysis.append(f"**License:** {package_data.get('license', 'Not specified')}")
        analysis.append("")
        
        # Scripts analysis
        if 'scripts' in package_data:
            analysis.append("## 🔧 Available Scripts")
            scripts = package_data['scripts']
            for script, command in scripts.items():
                analysis.append(f"- **`npm run {script}`**: `{command}`")
            analysis.append("")
        
        # Dependencies analysis
        if 'dependencies' in package_data:
            deps = package_data['dependencies']
            analysis.append(f"## 📚 Dependencies ({len(deps)} total)")
            
            # Categorize dependencies
            frameworks = []
            ui_libs = []
            utilities = []
            others = []
            
            for dep in deps.keys():
                if any(framework in dep.lower() for framework in ['react', 'next', 'vue', 'angular', 'svelte']):
                    frameworks.append(dep)
                elif any(ui in dep.lower() for ui in ['ui', 'component', 'styled', 'emotion', 'material', 'antd', 'chakra']):
                    ui_libs.append(dep)
                elif any(util in dep.lower() for util in ['util', 'lodash', 'moment', 'axios', 'fetch']):
                    utilities.append(dep)
                else:
                    others.append(dep)
            
            if frameworks:
                analysis.append("### 🏗️ Frameworks")
                for dep in frameworks:
                    analysis.append(f"- `{dep}`: {deps[dep]}")
            
            if ui_libs:
                analysis.append("### 🎨 UI Libraries")
                for dep in ui_libs:
                    analysis.append(f"- `{dep}`: {deps[dep]}")
            
            if utilities:
                analysis.append("### 🛠️ Utilities")
                for dep in utilities:
                    analysis.append(f"- `{dep}`: {deps[dep]}")
            
            if others:
                analysis.append("### 📦 Other Dependencies")
                for dep in sorted(others):
                    analysis.append(f"- `{dep}`: {deps[dep]}")
            
            analysis.append("")
        
        # Dev dependencies
        if 'devDependencies' in package_data:
            dev_deps = package_data['devDependencies']
            analysis.append(f"## 🔧 Development Dependencies ({len(dev_deps)} total)")
            for dep in sorted(dev_deps.keys()):
                analysis.append(f"- `{dep}`: {dev_deps[dep]}")
            analysis.append("")
        
        return '\n'.join(analysis)
    except Exception as e:
        return f"Error analyzing package.json: {e}"

@mcp.tool()
def analyze_project_config(file_path: str) -> str:
    """
    Analyze project configuration files (pom.xml, Cargo.toml, composer.json, etc.)
    """
    try:
        path = Path(file_path)
        if not path.is_absolute():
            path = Path.cwd() / path
            
        if not path.exists():
            return f"❌ Configuration file not found at: {path}"
        
        file_name = path.name.lower()
        analysis = []
        
        # Determine file type and analyze accordingly
        if file_name in ["pom.xml"]:
            return _analyze_maven_pom(path)
        elif file_name in ["cargo.toml"]:
            return _analyze_cargo_toml(path)
        elif file_name in ["composer.json"]:
            return _analyze_composer_json(path)
        elif file_name.endswith(".csproj") or file_name.endswith(".sln"):
            return _analyze_dotnet_project(path)
        elif file_name in ["go.mod"]:
            return _analyze_go_mod(path)
        elif file_name in ["pubspec.yaml"]:
            return _analyze_flutter_pubspec(path)
        elif file_name in ["gemfile"]:
            return _analyze_ruby_gemfile(path)
        elif file_name in ["build.gradle", "build.gradle.kts"]:
            return _analyze_gradle_build(path)
        else:
            # Generic file analysis
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            analysis.append(f"# 📄 File Analysis: {path.name}")
            analysis.append("")
            analysis.append(f"**File Type:** {path.suffix}")
            analysis.append(f"**Size:** {len(content)} characters")
            analysis.append(f"**Lines:** {content.count(chr(10)) + 1}")
            
            return '\n'.join(analysis)
    except Exception as e:
        return f"Error analyzing configuration file: {e}"

def _analyze_maven_pom(path: Path) -> str:
    """Analyze Maven pom.xml file"""
    try:
        import xml.etree.ElementTree as ET
        tree = ET.parse(path)
        root = tree.getroot()
        
        analysis = []
        analysis.append("# 📦 Maven POM Analysis")
        analysis.append("")
        
        # Extract namespace if present
        ns = {'maven': 'http://maven.apache.org/POM/4.0.0'} if 'http://maven.apache.org/POM/4.0.0' in root.tag else {}
        
        # Project info
        group_id = root.find('.//groupId', ns)
        artifact_id = root.find('.//artifactId', ns)
        version = root.find('.//version', ns)
        
        analysis.append("## ℹ️ Project Information")
        analysis.append(f"**Group ID:** {group_id.text if group_id is not None else 'Not specified'}")
        analysis.append(f"**Artifact ID:** {artifact_id.text if artifact_id is not None else 'Not specified'}")
        analysis.append(f"**Version:** {version.text if version is not None else 'Not specified'}")
        analysis.append("")
        
        # Dependencies
        dependencies = root.findall('.//dependency', ns)
        if dependencies:
            analysis.append(f"## 📚 Dependencies ({len(dependencies)} total)")
            for dep in dependencies[:10]:  # Show first 10
                dep_group = dep.find('groupId', ns)
                dep_artifact = dep.find('artifactId', ns)
                dep_version = dep.find('version', ns)
                analysis.append(f"- `{dep_group.text if dep_group is not None else '?'}:{dep_artifact.text if dep_artifact is not None else '?'}:{dep_version.text if dep_version is not None else '?'}`")
            if len(dependencies) > 10:
                analysis.append(f"- ... and {len(dependencies) - 10} more dependencies")
        
        return '\n'.join(analysis)
    except Exception as e:
        return f"Error analyzing pom.xml: {e}"

def _analyze_cargo_toml(path: Path) -> str:
    """Analyze Rust Cargo.toml file"""
    try:
        import tomllib
        with open(path, 'rb') as f:
            cargo_data = tomllib.load(f)
        
        analysis = []
        analysis.append("# 🦀 Cargo.toml Analysis")
        analysis.append("")
        
        # Package info
        if 'package' in cargo_data:
            pkg = cargo_data['package']
            analysis.append("## ℹ️ Package Information")
            analysis.append(f"**Name:** {pkg.get('name', 'Unknown')}")
            analysis.append(f"**Version:** {pkg.get('version', 'Unknown')}")
            analysis.append(f"**Edition:** {pkg.get('edition', 'Unknown')}")
            analysis.append(f"**Description:** {pkg.get('description', 'No description')}")
            analysis.append("")
        
        # Dependencies
        if 'dependencies' in cargo_data:
            deps = cargo_data['dependencies']
            analysis.append(f"## 📚 Dependencies ({len(deps)} total)")
            for dep, version in deps.items():
                if isinstance(version, str):
                    analysis.append(f"- `{dep}`: {version}")
                else:
                    analysis.append(f"- `{dep}`: {version.get('version', 'latest')}")
            analysis.append("")
        
        return '\n'.join(analysis)
    except Exception as e:
        return f"Error analyzing Cargo.toml: {e}"

def _analyze_composer_json(path: Path) -> str:
    """Analyze PHP composer.json file"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            composer_data = json.load(f)
        
        analysis = []
        analysis.append("# 🐘 Composer.json Analysis")
        analysis.append("")
        
        # Basic info
        analysis.append("## ℹ️ Project Information")
        analysis.append(f"**Name:** {composer_data.get('name', 'Unknown')}")
        analysis.append(f"**Description:** {composer_data.get('description', 'No description')}")
        analysis.append(f"**Type:** {composer_data.get('type', 'project')}")
        analysis.append("")
        
        # Dependencies
        if 'require' in composer_data:
            deps = composer_data['require']
            analysis.append(f"## 📚 Dependencies ({len(deps)} total)")
            for dep, version in deps.items():
                analysis.append(f"- `{dep}`: {version}")
            analysis.append("")
        
        return '\n'.join(analysis)
    except Exception as e:
        return f"Error analyzing composer.json: {e}"

def _analyze_dotnet_project(path: Path) -> str:
    """Analyze .NET project files"""
    try:
        import xml.etree.ElementTree as ET
        tree = ET.parse(path)
        root = tree.getroot()
        
        analysis = []
        analysis.append("# 🔷 .NET Project Analysis")
        analysis.append("")
        
        # Project properties
        target_framework = root.find('.//TargetFramework')
        output_type = root.find('.//OutputType')
        
        analysis.append("## ℹ️ Project Information")
        analysis.append(f"**Target Framework:** {target_framework.text if target_framework is not None else 'Not specified'}")
        analysis.append(f"**Output Type:** {output_type.text if output_type is not None else 'Not specified'}")
        analysis.append("")
        
        # Package references
        package_refs = root.findall('.//PackageReference')
        if package_refs:
            analysis.append(f"## 📦 Package References ({len(package_refs)} total)")
            for pkg in package_refs:
                name = pkg.get('Include')
                version = pkg.get('Version')
                analysis.append(f"- `{name}`: {version}")
            analysis.append("")
        
        return '\n'.join(analysis)
    except Exception as e:
        return f"Error analyzing .NET project: {e}"

def _analyze_go_mod(path: Path) -> str:
    """Analyze Go go.mod file"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.strip().split('\n')
        analysis = []
        analysis.append("# 🐹 Go Module Analysis")
        analysis.append("")
        
        # Module name and Go version
        for line in lines:
            if line.startswith('module '):
                analysis.append(f"**Module:** {line.replace('module ', '')}")
            elif line.startswith('go '):
                analysis.append(f"**Go Version:** {line.replace('go ', '')}")
        
        # Dependencies
        in_require = False
        deps = []
        for line in lines:
            if line.strip() == 'require (':
                in_require = True
                continue
            elif line.strip() == ')' and in_require:
                in_require = False
                continue
            elif in_require or line.startswith('require '):
                dep_line = line.strip()
                if dep_line and not dep_line.startswith('//'):
                    deps.append(dep_line)
        
        if deps:
            analysis.append("")
            analysis.append(f"## 📚 Dependencies ({len(deps)} total)")
            for dep in deps:
                analysis.append(f"- `{dep}`")
        
        return '\n'.join(analysis)
    except Exception as e:
        return f"Error analyzing go.mod: {e}"

def _analyze_flutter_pubspec(path: Path) -> str:
    """Analyze Flutter pubspec.yaml file"""
    try:
        import yaml
        with open(path, 'r', encoding='utf-8') as f:
            pubspec_data = yaml.safe_load(f)
        
        analysis = []
        analysis.append("# 🐦 Flutter Pubspec Analysis")
        analysis.append("")
        
        # Basic info
        analysis.append("## ℹ️ Project Information")
        analysis.append(f"**Name:** {pubspec_data.get('name', 'Unknown')}")
        analysis.append(f"**Description:** {pubspec_data.get('description', 'No description')}")
        analysis.append(f"**Version:** {pubspec_data.get('version', 'Unknown')}")
        
        # Flutter and Dart version
        if 'environment' in pubspec_data:
            env = pubspec_data['environment']
            analysis.append(f"**Dart SDK:** {env.get('sdk', 'Not specified')}")
            analysis.append(f"**Flutter:** {env.get('flutter', 'Not specified')}")
        analysis.append("")
        
        # Dependencies
        if 'dependencies' in pubspec_data:
            deps = pubspec_data['dependencies']
            analysis.append(f"## 📚 Dependencies ({len(deps)} total)")
            for dep, version in deps.items():
                if isinstance(version, str):
                    analysis.append(f"- `{dep}`: {version}")
                else:
                    analysis.append(f"- `{dep}`: {version}")
            analysis.append("")
        
        return '\n'.join(analysis)
    except Exception as e:
        return f"Error analyzing pubspec.yaml: {e}"

def _analyze_ruby_gemfile(path: Path) -> str:
    """Analyze Ruby Gemfile"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        analysis = []
        analysis.append("# 💎 Ruby Gemfile Analysis")
        analysis.append("")
        
        # Extract gems
        gem_lines = [line.strip() for line in content.split('\n') if line.strip().startswith('gem ')]
        
        if gem_lines:
            analysis.append(f"## 💎 Gems ({len(gem_lines)} total)")
            for gem_line in gem_lines:
                analysis.append(f"- `{gem_line}`")
            analysis.append("")
        
        # Ruby version
        ruby_version = None
        for line in content.split('\n'):
            if line.strip().startswith('ruby '):
                ruby_version = line.strip()
                break
        
        if ruby_version:
            analysis.append(f"**Ruby Version:** {ruby_version}")
            analysis.append("")
        
        return '\n'.join(analysis)
    except Exception as e:
        return f"Error analyzing Gemfile: {e}"

def _analyze_gradle_build(path: Path) -> str:
    """Analyze Gradle build file"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        analysis = []
        analysis.append("# 🐘 Gradle Build Analysis")
        analysis.append("")
        
        # Extract plugins
        plugin_lines = []
        for line in content.split('\n'):
            if 'plugin' in line and ('id' in line or 'apply' in line):
                plugin_lines.append(line.strip())
        
        if plugin_lines:
            analysis.append(f"## 🔌 Plugins ({len(plugin_lines)} total)")
            for plugin in plugin_lines:
                analysis.append(f"- `{plugin}`")
            analysis.append("")
        
        # Extract dependencies
        in_dependencies = False
        deps = []
        for line in content.split('\n'):
            if 'dependencies {' in line:
                in_dependencies = True
                continue
            elif in_dependencies and line.strip() == '}':
                in_dependencies = False
                continue
            elif in_dependencies and line.strip():
                deps.append(line.strip())
        
        if deps:
            analysis.append(f"## 📚 Dependencies ({len(deps)} total)")
            for dep in deps[:15]:  # Show first 15
                analysis.append(f"- `{dep}`")
            if len(deps) > 15:
                analysis.append(f"- ... and {len(deps) - 15} more dependencies")
        
        return '\n'.join(analysis)
    except Exception as e:
        return f"Error analyzing Gradle build file: {e}"

@mcp.tool()
def generate_component_documentation(component_path: str) -> str:
    """
    Generate comprehensive documentation for React/Vue/TypeScript components
    """
    try:
        path = Path(component_path)
        if not path.is_absolute():
            path = Path.cwd() / path
            
        if not path.exists():
            return f"❌ Component file not found: {path}"
            
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        
        component_name = path.stem
        file_extension = path.suffix
        
        docs = []
        docs.append(f"# {component_name} Component")
        docs.append("")
        docs.append(f"**File:** `{path.name}`")
        docs.append(f"**Type:** {file_extension.upper()} Component")
        docs.append("")
        
        # Extract imports
        imports = re.findall(r'^import\s+.*?from\s+[\'"].*?[\'"];?$', content, re.MULTILINE)
        if imports:
            docs.append("## 📦 Imports")
            docs.append("```typescript")
            for imp in imports[:10]:  # Show first 10 imports
                docs.append(imp)
            if len(imports) > 10:
                docs.append(f"// ... and {len(imports) - 10} more imports")
            docs.append("```")
            docs.append("")
        
        # Extract interfaces
        interfaces = re.findall(r'interface\s+(\w+)\s*{([^}]+)}', content, re.MULTILINE | re.DOTALL)
        if interfaces:
            docs.append("## 🔧 Interfaces")
            for interface_name, interface_body in interfaces:
                docs.append(f"### {interface_name}")
                docs.append("```typescript")
                docs.append(f"interface {interface_name} {{")
                docs.append(interface_body.strip())
                docs.append("}")
                docs.append("```")
                docs.append("")
        
        # Extract props interface
        props_match = re.search(r'interface\s+(\w*Props|\w*Properties)\s*{([^}]+)}', content, re.MULTILINE | re.DOTALL)
        if props_match:
            docs.append("## ⚙️ Props")
            docs.append("```typescript")
            docs.append(props_match.group(0))
            docs.append("```")
            docs.append("")
        
        # Extract component function/class
        component_patterns = [
            rf'const\s+{component_name}\s*[=:]\s*\([^)]*\)\s*=>\s*{{',
            rf'function\s+{component_name}\s*\([^)]*\)\s*{{',
            rf'class\s+{component_name}\s+extends\s+.*\s*{{',
            rf'export\s+default\s+function\s+{component_name}\s*\([^)]*\)\s*{{'
        ]
        
        for pattern in component_patterns:
            component_match = re.search(pattern, content, re.MULTILINE)
            if component_match:
                docs.append("## 🏗️ Component Definition")
                docs.append("```typescript")
                docs.append(component_match.group(0))
                docs.append("// ... component implementation")
                docs.append("```")
                docs.append("")
                break
        
        # Extract exported functions/constants
        exports = re.findall(r'^export\s+(?:const|function|class)\s+(\w+)', content, re.MULTILINE)
        if exports:
            docs.append("## 📤 Exports")
            for export in exports:
                docs.append(f"- `{export}`")
            docs.append("")
        
        # File stats
        lines = content.count('\n') + 1
        chars = len(content)
        docs.append("## 📊 File Statistics")
        docs.append(f"- **Lines of code:** {lines}")
        docs.append(f"- **Characters:** {chars:,}")
        docs.append(f"- **File size:** {len(content.encode('utf-8'))} bytes")
        
        return '\n'.join(docs)
    except Exception as e:
        return f"Error generating component documentation: {e}"

@mcp.tool()
def generate_project_readme(base_path: str = ".") -> str:
    """
    Generate a comprehensive README.md for any project based on its structure and files
    """
    try:
        base_path = Path(base_path).resolve()
        
        # Detect project type and get package info
        project_type = detect_project_type(str(base_path))
        
        readme = []
        
        # Try to get project name from package.json or directory name
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
        
        # Generate README content
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
        if package_json_path.exists():
            readme.append("```bash")
            readme.append("# Clone the repository")
            readme.append(f"git clone <repository-url>")
            readme.append(f"cd {project_name}")
            readme.append("")
            readme.append("# Install dependencies")
            readme.append("npm install")
            readme.append("```")
        else:
            readme.append("```bash")
            readme.append("# Clone the repository")
            readme.append(f"git clone <repository-url>")
            readme.append(f"cd {project_name}")
            readme.append("```")
        readme.append("")
        
        # Available scripts
        if package_json_path.exists():
            try:
                with open(package_json_path, 'r', encoding='utf-8') as f:
                    package_data = json.load(f)
                    if 'scripts' in package_data:
                        readme.append("## 🔧 Available Scripts")
                        readme.append("")
                        for script, command in package_data['scripts'].items():
                            readme.append(f"```bash")
                            readme.append(f"npm run {script}")
                            readme.append(f"```")
                            readme.append(f"{command}")
                            readme.append("")
            except:
                pass
        
        # Project structure
        readme.append("## 📁 Project Structure")
        readme.append("")
        readme.append("```")
        
        def add_structure(path: Path, prefix: str = "", max_depth: int = 2, current_depth: int = 0):
            if current_depth >= max_depth:
                return
                
            items = []
            try:
                for item in path.iterdir():
                    if item.name.startswith('.') or item.name in ['node_modules', '__pycache__', '.next', 'out']:
                        continue
                    items.append(item)
                
                items.sort(key=lambda x: (x.is_file(), x.name.lower()))
                
                for i, item in enumerate(items[:8]):  # Limit items shown
                    is_last = i == len(items) - 1
                    current_prefix = "└── " if is_last else "├── "
                    readme.append(f"{prefix}{current_prefix}{item.name}")
                    
                    if item.is_dir() and current_depth < max_depth - 1:
                        next_prefix = prefix + ("    " if is_last else "│   ")
                        add_structure(item, next_prefix, max_depth, current_depth + 1)
            except:
                pass
        
        readme.append(f"{project_name}/")
        add_structure(base_path, "", max_depth=3)
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

@mcp.tool()
def batch_read_files(file_paths: List[str]) -> str:
    """
    Read multiple files at once and return their contents with clear separation
    """
    try:
        results = []
        for file_path in file_paths:
            path = Path(file_path)
            if not path.is_absolute():
                path = Path.cwd() / path
            
            results.append(f"## 📄 File: {path}")
            results.append("")
            
            if not path.exists():
                results.append("❌ File not found")
            else:
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    results.append(f"```{path.suffix[1:] if path.suffix else 'text'}")
                    results.append(content[:2000])  # Limit to first 2000 characters
                    if len(content) > 2000:
                        results.append(f"\n... (truncated, total length: {len(content)} characters)")
                    results.append("```")
                except Exception as e:
                    results.append(f"❌ Error reading file: {e}")
            
            results.append("")
            results.append("---")
            results.append("")
        
        return '\n'.join(results)
    except Exception as e:
        return f"Error in batch file reading: {e}"

@mcp.tool()
def find_files_by_pattern(pattern: str, base_path: str = ".") -> str:
    """
    Find files matching a pattern (supports wildcards like *.py, **/*.js, etc.)
    """
    try:
        base_path = Path(base_path).resolve()
        
        # Use glob to find matching files
        matching_files = list(base_path.glob(pattern))
        
        # Filter out hidden files and common build directories
        filtered_files = []
        for file_path in matching_files:
            relative_path = file_path.relative_to(base_path)
            path_parts = relative_path.parts
            
            # Skip hidden files and directories
            if any(part.startswith('.') for part in path_parts):
                continue
            
            # Skip common build/dependency directories
            skip_dirs = {'node_modules', '__pycache__', '.next', 'out', 'dist', 'build', 'target', 'vendor'}
            if any(part in skip_dirs for part in path_parts):
                continue
            
            filtered_files.append(file_path)
        
        if not filtered_files:
            return f"No files found matching pattern: {pattern}"
        
        # Sort files by extension and name
        filtered_files.sort(key=lambda x: (x.suffix, x.name))
        
        results = []
        results.append(f"# 🔍 Files matching pattern: `{pattern}`")
        results.append("")
        results.append(f"Found {len(filtered_files)} files:")
        results.append("")
        
        # Group by extension
        by_extension = {}
        for file_path in filtered_files:
            ext = file_path.suffix or 'no-extension'
            if ext not in by_extension:
                by_extension[ext] = []
            by_extension[ext].append(file_path.relative_to(base_path))
        
        for ext, files in sorted(by_extension.items()):
            results.append(f"## {ext} files ({len(files)})")
            for file_path in files:
                results.append(f"- `{file_path}`")
            results.append("")
        
        return '\n'.join(results)
    except Exception as e:
        return f"Error finding files: {e}"

@mcp.tool()
def analyze_code_metrics(base_path: str = ".") -> str:
    """
    Analyze code metrics like file count, lines of code, and technology distribution
    """
    try:
        base_path = Path(base_path).resolve()
        
        # File extensions to analyze
        code_extensions = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.ts': 'TypeScript', 
            '.jsx': 'React JSX',
            '.tsx': 'React TSX',
            '.java': 'Java',
            '.kt': 'Kotlin',
            '.go': 'Go',
            '.rs': 'Rust',
            '.php': 'PHP',
            '.rb': 'Ruby',
            '.cs': 'C#',
            '.cpp': 'C++',
            '.c': 'C',
            '.swift': 'Swift',
            '.dart': 'Dart',
            '.html': 'HTML',
            '.css': 'CSS',
            '.scss': 'SCSS',
            '.vue': 'Vue',
            '.xml': 'XML',
            '.json': 'JSON',
            '.yaml': 'YAML',
            '.yml': 'YAML',
            '.toml': 'TOML',
            '.md': 'Markdown',
        }
        
        metrics = {
            'total_files': 0,
            'total_lines': 0,
            'by_language': {},
            'largest_files': [],
            'file_sizes': [],
        }
        
        # Analyze all files
        for file_path in base_path.rglob('*'):
            if not file_path.is_file():
                continue
            
            # Skip hidden files and common build directories
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
                    size = len(content)
                    
                    metrics['total_lines'] += lines
                    metrics['file_sizes'].append(size)
                    
                    if language not in metrics['by_language']:
                        metrics['by_language'][language] = {'files': 0, 'lines': 0}
                    
                    metrics['by_language'][language]['files'] += 1
                    metrics['by_language'][language]['lines'] += lines
                    
                    # Track largest files
                    metrics['largest_files'].append({
                        'path': relative_path,
                        'lines': lines,
                        'size': size,
                        'language': language
                    })
            except:
                # Skip binary files or files with encoding issues
                pass
        
        # Sort largest files
        metrics['largest_files'].sort(key=lambda x: x['lines'], reverse=True)
        metrics['largest_files'] = metrics['largest_files'][:10]  # Top 10
        
        # Generate report
        results = []
        results.append("# 📊 Code Metrics Analysis")
        results.append("")
        results.append(f"**Total Files:** {metrics['total_files']:,}")
        results.append(f"**Total Lines of Code:** {metrics['total_lines']:,}")
        results.append(f"**Average File Size:** {sum(metrics['file_sizes']) // len(metrics['file_sizes']) if metrics['file_sizes'] else 0:,} characters")
        results.append("")
        
        # Language breakdown
        if metrics['by_language']:
            results.append("## 🔧 Technology Distribution")
            sorted_languages = sorted(metrics['by_language'].items(), key=lambda x: x[1]['lines'], reverse=True)
            
            total_lines = metrics['total_lines']
            for language, stats in sorted_languages:
                percentage = (stats['lines'] / total_lines * 100) if total_lines > 0 else 0
                results.append(f"- **{language}**: {stats['files']} files, {stats['lines']:,} lines ({percentage:.1f}%)")
            results.append("")
        
        # Largest files
        if metrics['largest_files']:
            results.append("## 📄 Largest Files")
            for file_info in metrics['largest_files']:
                results.append(f"- `{file_info['path']}` ({file_info['language']}) - {file_info['lines']:,} lines")
            results.append("")
        
        return '\n'.join(results)
    except Exception as e:
        return f"Error analyzing code metrics: {e}"

@mcp.tool()
def scan_for_todos_and_fixmes(base_path: str = ".") -> str:
    """
    Scan project for TODO, FIXME, HACK, and other code comments that need attention
    """
    try:
        base_path = Path(base_path).resolve()
        
        # Patterns to search for
        patterns = {
            'TODO': r'(?i)(?://|#|\*|<!--)?\s*TODO\s*:?\s*(.*)',
            'FIXME': r'(?i)(?://|#|\*|<!--)?\s*FIXME\s*:?\s*(.*)',
            'HACK': r'(?i)(?://|#|\*|<!--)?\s*HACK\s*:?\s*(.*)',
            'NOTE': r'(?i)(?://|#|\*|<!--)?\s*NOTE\s*:?\s*(.*)',
            'WARNING': r'(?i)(?://|#|\*|<!--)?\s*WARNING\s*:?\s*(.*)',
        }
        
        findings = {pattern: [] for pattern in patterns.keys()}
        
        # Code file extensions to search
        code_extensions = {'.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.kt', '.go', '.rs', '.php', '.rb', '.cs', '.cpp', '.c', '.swift', '.dart'}
        
        for file_path in base_path.rglob('*'):
            if not file_path.is_file() or file_path.suffix not in code_extensions:
                continue
            
            # Skip hidden files and build directories
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
                # Skip files with encoding issues
                pass
        
        # Generate report
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
                'HACK': '⚠️',
                'NOTE': '💡',
                'WARNING': '⚠️'
            }
            
            results.append(f"## {emoji_map.get(pattern_name, '📌')} {pattern_name} ({len(items)} items)")
            results.append("")
            
            for item in items:
                results.append(f"- **`{item['file']}:{item['line']}`** - {item['comment']}")
            results.append("")
        
        return '\n'.join(results)
    except Exception as e:
        return f"Error scanning for annotations: {e}"

@mcp.tool()
def get_cursor_working_directory() -> str:
    """
    Get the current working directory where Cursor IDE is running (user's project directory)
    This helps identify which project the user wants to document
    """
    try:
        # Try to get the actual working directory from environment
        import os
        cursor_cwd = os.environ.get('CURSOR_CWD', os.getcwd())
        cwd = Path(cursor_cwd).resolve()
        return f"📍 Cursor working directory: {cwd}\n💡 Use this path as base_path in other tools if needed"
    except Exception as e:
        return f"Error getting Cursor directory: {e}"

@mcp.tool()
def auto_detect_user_project(hint_path: str = "") -> str:
    """
    Automatically detect the user's project directory and provide analysis
    This tool tries to find the actual project the user wants to document
    """
    try:
        # Start with provided hint or try to detect from environment
        if hint_path:
            base_path = Path(hint_path).resolve()
        else:
            # Try multiple methods to detect the user's actual project directory
            detected_path = None
            
            # Method 1: Check environment variables that Cursor/IDEs might set
            env_vars_to_check = [
                'CURSOR_CWD',          # Cursor IDE working directory
                'VSCODE_CWD',          # VS Code working directory  
                'PWD',                 # Current working directory (Unix)
                'CD',                  # Current directory (Windows)
                'INIT_CWD',            # Initial working directory
                'PROJECT_ROOT',        # Some IDEs set this
                'WORKSPACE_FOLDER',    # Workspace folder
            ]
            
            detection_method = "unknown"
            
            for env_var in env_vars_to_check:
                env_path = os.environ.get(env_var, '')
                if env_path and Path(env_path).exists():
                    test_path = Path(env_path).resolve()
                    # Don't use the MCP server's own directory or system directories
                    path_str = str(test_path).lower()
                    if (not path_str.endswith('documenter') and 
                        not path_str.endswith('mcps') and
                        not 'system32' in path_str and
                        not 'program files' in path_str):
                        detected_path = str(test_path)
                        detection_method = f"environment variable '{env_var}'"
                        break
            
            # Method 2: Try to detect from the calling process working directory
            if not detected_path:
                try:
                    import psutil
                    current_process = psutil.Process()
                    parent_process = current_process.parent()
                    if parent_process and parent_process.name().lower() in ['cursor.exe', 'code.exe', 'cursor', 'code']:
                        cwd = parent_process.cwd()
                        if cwd and Path(cwd).exists():
                            detected_path = cwd
                            detection_method = f"parent process ({parent_process.name()}) working directory"
                except:
                    pass  # psutil not available or other error
            
            # Method 3: Check current working directory as fallback
            if not detected_path:
                cwd = Path.cwd().resolve()
                cwd_str = str(cwd).lower()
                if (not cwd_str.endswith('documenter') and 
                    not cwd_str.endswith('mcps')):
                    detected_path = str(cwd)
                    detection_method = "current working directory"
            
            # Method 4: Look for common project indicators in parent directories
            if not detected_path:
                current_dir = Path.cwd().resolve()
                for parent in [current_dir] + list(current_dir.parents)[:3]:  # Check up to 3 levels up
                    if any((parent / indicator).exists() for indicator in [
                        'package.json', 'pyproject.toml', 'requirements.txt', 'pom.xml',
                        'Cargo.toml', 'go.mod', 'composer.json', '.git', '.gitignore'
                    ]):
                        parent_str = str(parent).lower()
                        if (not parent_str.endswith('documenter') and 
                            not parent_str.endswith('mcps')):
                            detected_path = str(parent)
                            detection_method = f"project indicators in parent directory"
                            break
            
            if not detected_path:
                detected_path = str(Path.cwd())
                detection_method = "fallback to current directory"
            
            base_path = Path(detected_path).resolve()
        
        result = []
        result.append(f"🎯 Detected user project directory: {base_path}")
        
        if not hint_path:
            result.append(f"🔍 Detection method: {detection_method}")
        result.append("")
        
        # Quick analysis
        if not base_path.exists():
            result.append("❌ Directory does not exist")
            return '\n'.join(result)
        
        # Count files and detect project type
        files = list(base_path.iterdir()) if base_path.is_dir() else []
        project_files = [f.name for f in files if f.is_file()]
        
        result.append(f"📁 Contains {len(files)} items")
        result.append(f"📄 Key files found: {', '.join(project_files[:10])}")
        
        # Check for project indicators
        project_indicators = []
        common_indicators = [
            ('package.json', 'Node.js/JavaScript project'),
            ('pyproject.toml', 'Python project'),
            ('requirements.txt', 'Python project'),
            ('pom.xml', 'Java/Maven project'),
            ('build.gradle', 'Java/Gradle project'), 
            ('Cargo.toml', 'Rust project'),
            ('go.mod', 'Go project'),
            ('composer.json', 'PHP project'),
            ('.csproj', '.NET project'),
            ('.sln', '.NET solution'),
            ('pubspec.yaml', 'Flutter project'),
            ('Gemfile', 'Ruby project'),
            ('.git', 'Git repository'),
        ]
        
        for indicator, description in common_indicators:
            if any(indicator in f or f.endswith(indicator) for f in project_files):
                project_indicators.append(description)
        
        if project_indicators:
            result.append(f"🔧 Project type indicators: {', '.join(set(project_indicators))}")
        else:
            result.append("❓ No clear project type indicators found")
        
        # Check if this looks like a real project
        has_project_structure = any(
            (base_path / folder).exists() for folder in [
                'src', 'app', 'lib', 'components', 'pages', 'public', 'assets',
                'tests', 'test', 'spec', 'docs', 'config', 'scripts'
            ]
        )
        
        if has_project_structure:
            result.append("✅ Project structure detected")
        elif len(files) < 3:
            result.append("⚠️ Warning: This may not be a project directory")
        
        result.append("")
        result.append("💡 To analyze this project, use:")
        result.append(f"   \"Document my project comprehensively\"")
        result.append("   Or specify the path explicitly:")
        result.append(f"   \"Document the project at {base_path} comprehensively\"")
        
        return '\n'.join(result)
    except Exception as e:
        return f"Error detecting user project: {e}"

@mcp.tool()
def document_project_comprehensive(project_path: str = "") -> str:
    """
    Complete project documentation workflow with enhanced detection and analysis
    Automatically detects any project type and generates comprehensive documentation
    """
    try:
        # Step 1: Enhanced project path detection
        if not project_path:
            detected_path, detection_method = _get_enhanced_project_detection()
            project_path = detected_path
        else:
            detection_method = "explicitly specified"
        
        base_path = Path(project_path).resolve()
        
        results = []
        results.append("# 🚀 Universal Project Documentation")
        results.append("=" * 70)
        results.append(f"📁 Project Location: {base_path}")
        results.append(f"🔍 Detection Method: {detection_method}")
        results.append(f"🖥️  Platform: {platform.system()} {platform.release()}")
        results.append(f"🐍 Python: {sys.version.split()[0]}")
        results.append("")
        
        if not base_path.exists():
            return f"❌ Project path does not exist: {base_path}\nDetection method: {detection_method}"
        
        # Validate this is a real project directory
        project_files = list(base_path.iterdir()) if base_path.is_dir() else []
        project_indicators = [
            'package.json', 'pyproject.toml', 'requirements.txt', 'pom.xml',
            'Cargo.toml', 'go.mod', 'composer.json', '.git', '.gitignore',
            'src', 'app', 'lib', 'components', 'pages', 'Dockerfile'
        ]
        
        has_indicators = any(
            (base_path / indicator).exists() for indicator in project_indicators
        )
        
        if not has_indicators and len(project_files) < 3:
            results.append("⚠️  Warning: This doesn't appear to be a typical project directory.")
            results.append("💡 Suggestion: Ensure you're in the correct project folder, or specify the path explicitly:")
            results.append("   Example: 'Document the project at /path/to/your/project comprehensively'")
            results.append("")
        
        # Step 2: Enhanced project type detection
        results.append("## 🔍 Step 1: Enhanced Project Type Detection")
        results.append("-" * 50)
        try:
            project_type_result = detect_project_type(str(base_path))
            results.append(project_type_result)
        except Exception as e:
            results.append(f"❌ Error in project type detection: {e}")
            results.append("📝 Continuing with generic analysis...")
        results.append("")
        
        # Step 3: Comprehensive project structure analysis
        results.append("## 📊 Step 2: Project Structure Analysis")
        results.append("-" * 50)
        try:
            structure_result = analyze_project_structure(str(base_path))
            results.append(structure_result)
        except Exception as e:
            results.append(f"❌ Error in structure analysis: {e}")
        results.append("")
        
        # Step 4: Multi-format configuration analysis
        results.append("## ⚙️ Step 3: Configuration Files Analysis")
        results.append("-" * 50)
        
        config_patterns = {
            "Node.js/JavaScript": ["package.json", "package-lock.json", "yarn.lock", "pnpm-lock.yaml"],
            "Python": ["pyproject.toml", "requirements.txt", "setup.py", "poetry.lock", "Pipfile"],
            "Java/Kotlin": ["pom.xml", "build.gradle", "build.gradle.kts", "settings.gradle"],
            ".NET": ["*.csproj", "*.sln", "global.json", "Directory.Build.props"],
            "Go": ["go.mod", "go.sum"],
            "Rust": ["Cargo.toml", "Cargo.lock"],
            "PHP": ["composer.json", "composer.lock"],
            "Ruby": ["Gemfile", "Gemfile.lock"],
            "Flutter/Dart": ["pubspec.yaml", "pubspec.lock"],
            "Swift": ["Package.swift"],
            "Docker": ["Dockerfile", "docker-compose.yml", "docker-compose.yaml"],
            "Infrastructure": ["terraform.tf", "main.tf", "variables.tf"]
        }
        
        found_configs = []
        for category, config_files in config_patterns.items():
            category_files = []
            for config_file in config_files:
                if "*" in config_file:
                    matches = list(base_path.glob(config_file))
                    if matches:
                        category_files.extend([m.name for m in matches])
                else:
                    if (base_path / config_file).exists():
                        category_files.append(config_file)
            
            if category_files:
                results.append(f"### {category}")
                for config_file in category_files:
                    config_path = base_path / config_file
                    if config_path.exists():
                        found_configs.append(config_file)
                        try:
                            if config_file == "package.json":
                                config_result = analyze_package_json(str(config_path))
                            else:
                                config_result = analyze_project_config(str(config_path))
                            
                            # Truncate very long results
                            if len(config_result) > 3000:
                                config_result = config_result[:3000] + "\n... (truncated for brevity)"
                            
                            results.append(config_result)
                        except Exception as e:
                            results.append(f"❌ Error analyzing {config_file}: {e}")
                results.append("")
        
        if not found_configs:
            results.append("ℹ️ No standard configuration files found")
            results.append("This might be a generic project or use custom configuration")
        results.append("")
        
        # Step 5: Code metrics and technology analysis
        results.append("## 📈 Step 4: Code Metrics & Technology Analysis")
        results.append("-" * 50)
        try:
            metrics_result = analyze_code_metrics(str(base_path))
            results.append(metrics_result)
        except Exception as e:
            results.append(f"❌ Error analyzing code metrics: {e}")
        results.append("")
        
        # Step 6: Development workflow analysis
        results.append("## 🛠️ Step 5: Development Workflow Analysis")
        results.append("-" * 50)
        try:
            workflow_info = _analyze_development_workflow(base_path)
            results.append(workflow_info)
        except Exception as e:
            results.append(f"❌ Error analyzing workflow: {e}")
        results.append("")
        
        # Step 7: README generation
        results.append("## 📝 Step 6: Comprehensive README Generation")
        results.append("-" * 50)
        try:
            readme_result = generate_project_readme(str(base_path))
            
            # Save the README file
            readme_path = base_path / "README_GENERATED.md"
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(readme_result)
            
            results.append(f"✅ README generated and saved to: {readme_path}")
            results.append("")
            results.append("### 📖 Generated README Preview (first 1000 characters):")
            results.append("```markdown")
            results.append(readme_result[:1000] + "..." if len(readme_result) > 1000 else readme_result)
            results.append("```")
        except Exception as e:
            results.append(f"❌ Error generating README: {e}")
        results.append("")
        
        # Step 8: Summary and recommendations
        results.append("## ✅ Documentation Summary")
        results.append("-" * 50)
        results.append(f"📁 **Project Analyzed**: {base_path}")
        results.append(f"🔍 **Detection Method**: {detection_method}")
        results.append(f"⚙️ **Config Files Found**: {len(found_configs)}")
        results.append(f"📄 **Documentation Generated**: README_GENERATED.md")
        results.append("")
        
        # Provide next steps
        results.append("## 🎯 Next Steps & Recommendations")
        results.append("-" * 50)
        next_steps = _get_project_recommendations(base_path, found_configs)
        results.append(next_steps)
        results.append("")
        
        results.append("🎉 **Universal project documentation completed successfully!**")
        results.append("")
        results.append("💡 **Tip**: You can now use the generated README_GENERATED.md as a starting point")
        results.append("for your project documentation, or ask for specific component analysis.")
        
        return '\n'.join(results)
        
    except Exception as e:
        return f"❌ Critical error in comprehensive documentation: {e}\n\nPlease try specifying the project path explicitly:\n'Document the project at /absolute/path/to/project comprehensively'"

def _analyze_development_workflow(base_path: Path) -> str:
    """Analyze development workflow based on project structure and files"""
    workflow_info = []
    
    # Check for CI/CD
    ci_files = ['.github/workflows', '.gitlab-ci.yml', 'azure-pipelines.yml', 'Jenkinsfile', '.circleci']
    found_ci = [ci for ci in ci_files if (base_path / ci).exists()]
    
    if found_ci:
        workflow_info.append(f"🔄 **CI/CD Detected**: {', '.join(found_ci)}")
    
    # Check for testing
    test_indicators = ['test', 'tests', '__tests__', 'spec', 'specs']
    test_dirs = [td for td in test_indicators if (base_path / td).exists()]
    
    if test_dirs:
        workflow_info.append(f"🧪 **Testing Structure**: {', '.join(test_dirs)}")
    
    # Check for documentation
    doc_indicators = ['docs', 'documentation', 'README.md', 'CONTRIBUTING.md']
    doc_files = [doc for doc in doc_indicators if (base_path / doc).exists()]
    
    if doc_files:
        workflow_info.append(f"📚 **Documentation**: {', '.join(doc_files)}")
    
    # Check for containerization
    container_files = ['Dockerfile', 'docker-compose.yml', '.dockerignore']
    container_found = [cf for cf in container_files if (base_path / cf).exists()]
    
    if container_found:
        workflow_info.append(f"🐳 **Containerization**: {', '.join(container_found)}")
    
    # Check for environment management
    env_files = ['.env.example', '.env.template', '.env.local', 'config']
    env_found = [ef for ef in env_files if (base_path / ef).exists()]
    
    if env_found:
        workflow_info.append(f"🌍 **Environment Config**: {', '.join(env_found)}")
    
    return '\n'.join(workflow_info) if workflow_info else "ℹ️ Standard development workflow detected"

def _get_project_recommendations(base_path: Path, found_configs: List[str]) -> str:
    """Generate recommendations based on project analysis"""
    recommendations = []
    
    # Generic recommendations
    if not (base_path / 'README.md').exists():
        recommendations.append("📝 Consider creating a comprehensive README.md")
    
    if not (base_path / '.gitignore').exists():
        recommendations.append("🚫 Add a .gitignore file for your project type")
    
    if not (base_path / 'LICENSE').exists():
        recommendations.append("⚖️ Consider adding a LICENSE file")
    
    # Technology-specific recommendations
    if any('package.json' in config for config in found_configs):
        if not (base_path / '.nvmrc').exists():
            recommendations.append("🔧 Consider adding .nvmrc for Node.js version management")
        if not (base_path / 'tsconfig.json').exists() and 'typescript' in str(found_configs).lower():
            recommendations.append("📘 Consider adding TypeScript configuration")
    
    if any('requirements.txt' in config or 'pyproject.toml' in config for config in found_configs):
        if not (base_path / '.python-version').exists():
            recommendations.append("🐍 Consider adding .python-version for Python version management")
    
    if any('.csproj' in config or '.sln' in config for config in found_configs):
        if not (base_path / '.editorconfig').exists():
            recommendations.append("📝 Consider adding .editorconfig for consistent coding style")
    
    return '\n'.join(f"• {rec}" for rec in recommendations) if recommendations else "✅ Project structure looks comprehensive!"

if __name__ == "__main__":
    # Log to stderr instead of stdout to avoid interfering with MCP protocol
    cwd = os.getcwd()
    print(f"🚀 Universal Project Documenter starting from: {cwd}", file=sys.stderr)
    print("🔧 Ready to document any project!", file=sys.stderr)
    print("📝 Supports: Next.js, React, Node.js, Python, and generic projects", file=sys.stderr)
    mcp.run(transport='stdio')