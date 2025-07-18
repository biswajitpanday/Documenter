from mcp.server.fastmcp import FastMCP
import os
import json
import re
from pathlib import Path
from typing import List, Dict, Optional

mcp = FastMCP("Universal Project Documenter")

# Configuration for different project types
PROJECT_CONFIGS = {
    "nextjs": {
        "indicators": ["next.config.js", "next.config.ts", "package.json"],
        "check_content": {"package.json": "next"},
        "important_dirs": ["app", "pages", "components", "src", "public"],
        "important_files": ["package.json", "README.md", "tsconfig.json", "tailwind.config.js"]
    },
    "react": {
        "indicators": ["package.json"],
        "check_content": {"package.json": "react"},
        "important_dirs": ["src", "components", "public"],
        "important_files": ["package.json", "README.md", "tsconfig.json"]
    },
    "angular": {
        "indicators": ["angular.json", "package.json"],
        "check_content": {"package.json": "@angular"},
        "important_dirs": ["src", "app", "components", "services", "modules"],
        "important_files": ["angular.json", "package.json", "tsconfig.json", "karma.conf.js"]
    },
    "vue": {
        "indicators": ["vue.config.js", "vite.config.js", "package.json"],
        "check_content": {"package.json": "vue"},
        "important_dirs": ["src", "components", "views", "router", "store"],
        "important_files": ["package.json", "vue.config.js", "vite.config.js", "README.md"]
    },
    "nodejs": {
        "indicators": ["package.json"],
        "check_content": {"package.json": "node"},
        "important_dirs": ["src", "lib", "routes", "controllers"],
        "important_files": ["package.json", "README.md", "index.js", "server.js"]
    },
    "dotnet": {
        "indicators": [".csproj", ".sln", ".vbproj", ".fsproj", "global.json"],
        "check_content": {},
        "important_dirs": ["Controllers", "Views", "Models", "Services", "Data"],
        "important_files": [".csproj", ".sln", "appsettings.json", "Program.cs", "Startup.cs"]
    },
    "java": {
        "indicators": ["pom.xml", "build.gradle", "gradlew", "build.xml"],
        "check_content": {},
        "important_dirs": ["src/main/java", "src/test/java", "src/main/resources"],
        "important_files": ["pom.xml", "build.gradle", "README.md", "application.properties"]
    },
    "kotlin": {
        "indicators": ["build.gradle.kts", "settings.gradle.kts", "gradle.properties"],
        "check_content": {"build.gradle.kts": "kotlin"},
        "important_dirs": ["src/main/kotlin", "src/test/kotlin", "src/main/resources"],
        "important_files": ["build.gradle.kts", "settings.gradle.kts", "README.md"]
    },
    "go": {
        "indicators": ["go.mod", "go.sum", "main.go"],
        "check_content": {},
        "important_dirs": ["cmd", "pkg", "internal", "api", "web"],
        "important_files": ["go.mod", "go.sum", "main.go", "README.md", "Makefile"]
    },
    "rust": {
        "indicators": ["Cargo.toml", "Cargo.lock"],
        "check_content": {},
        "important_dirs": ["src", "tests", "examples", "benches"],
        "important_files": ["Cargo.toml", "Cargo.lock", "README.md", "main.rs", "lib.rs"]
    },
    "php": {
        "indicators": ["composer.json", "composer.lock", "index.php"],
        "check_content": {},
        "important_dirs": ["src", "app", "public", "vendor", "tests"],
        "important_files": ["composer.json", "index.php", "README.md", ".htaccess"]
    },
    "laravel": {
        "indicators": ["artisan", "composer.json"],
        "check_content": {"composer.json": "laravel"},
        "important_dirs": ["app", "config", "database", "resources", "routes"],
        "important_files": ["artisan", "composer.json", ".env.example", "webpack.mix.js"]
    },
    "flutter": {
        "indicators": ["pubspec.yaml", "pubspec.lock"],
        "check_content": {"pubspec.yaml": "flutter"},
        "important_dirs": ["lib", "test", "android", "ios", "web"],
        "important_files": ["pubspec.yaml", "README.md", "analysis_options.yaml"]
    },
    "swift": {
        "indicators": ["Package.swift", "*.xcodeproj", "*.xcworkspace"],
        "check_content": {},
        "important_dirs": ["Sources", "Tests", "Package.swift"],
        "important_files": ["Package.swift", "README.md", "*.swift"]
    },
    "ruby": {
        "indicators": ["Gemfile", "Gemfile.lock", "Rakefile"],
        "check_content": {},
        "important_dirs": ["app", "config", "db", "lib", "test", "spec"],
        "important_files": ["Gemfile", "Rakefile", "README.md", "config.ru"]
    },
    "rails": {
        "indicators": ["Gemfile", "config/application.rb"],
        "check_content": {"Gemfile": "rails"},
        "important_dirs": ["app", "config", "db", "lib", "test", "spec"],
        "important_files": ["Gemfile", "Rakefile", "config/routes.rb", "config/application.rb"]
    },
    "python": {
        "indicators": ["requirements.txt", "pyproject.toml", "setup.py", "poetry.lock"],
        "check_content": {},
        "important_dirs": ["src", "lib", "tests", "docs"],
        "important_files": ["requirements.txt", "README.md", "setup.py", "pyproject.toml"]
    },
    "django": {
        "indicators": ["manage.py", "requirements.txt"],
        "check_content": {"requirements.txt": "django"},
        "important_dirs": ["apps", "static", "templates", "media"],
        "important_files": ["manage.py", "settings.py", "urls.py", "wsgi.py"]
    },
    "fastapi": {
        "indicators": ["main.py", "requirements.txt"],
        "check_content": {"requirements.txt": "fastapi"},
        "important_dirs": ["app", "models", "routes", "schemas"],
        "important_files": ["main.py", "requirements.txt", "README.md"]
    },
    "gradle": {
        "indicators": ["build.gradle", "gradlew", "settings.gradle"],
        "check_content": {},
        "important_dirs": ["src", "build", "gradle"],
        "important_files": ["build.gradle", "settings.gradle", "gradle.properties"]
    },
    "maven": {
        "indicators": ["pom.xml"],
        "check_content": {},
        "important_dirs": ["src/main", "src/test", "target"],
        "important_files": ["pom.xml", "README.md"]
    },
    "generic": {
        "indicators": [],
        "check_content": {},
        "important_dirs": ["src", "lib", "docs"],
        "important_files": ["README.md"]
    }
}

@mcp.tool()
def detect_project_type(base_path: str = ".") -> str:
    """
    Automatically detect the type of project (Next.js, React, Node.js, Python, etc.)
    """
    try:
        base_path = Path(base_path).resolve()
        detected_types = []
        
        for project_type, config in PROJECT_CONFIGS.items():
            if project_type == "generic":
                continue
                
            score = 0
            found_indicators = []
            
            # Check for indicator files
            for indicator in config["indicators"]:
                if "*" in indicator:  # Handle wildcards like *.xcodeproj
                    import glob
                    matches = list(base_path.glob(indicator))
                    if matches:
                        found_indicators.append(f"{indicator} ({len(matches)} files)")
                        score += 2
                elif (base_path / indicator).exists():
                    found_indicators.append(indicator)
                    score += 2
            
            # Check file contents for specific keywords
            for file_to_check, content_key in config["check_content"].items():
                file_path = base_path / file_to_check
                if file_path.exists():
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read().lower()
                            if content_key.lower() in content:
                                score += 3
                                found_indicators.append(f"{file_to_check} (contains '{content_key}')")
                    except:
                        pass
            
            # Check for important directories
            dir_score = 0
            found_dirs = []
            for important_dir in config["important_dirs"]:
                if (base_path / important_dir).exists():
                    found_dirs.append(important_dir)
                    dir_score += 1
            
            if dir_score > 0:
                score += min(dir_score, 3)  # Cap directory score at 3
            
            # Only consider if we found some indicators
            if score > 0:
                detected_types.append({
                    'type': project_type,
                    'score': score,
                    'indicators': found_indicators,
                    'directories': found_dirs
                })
        
        # Sort by score (highest first)
        detected_types.sort(key=lambda x: x['score'], reverse=True)
        
        if not detected_types:
            return "Detected project type: GENERIC\nNo specific framework detected"
        
        # Build result
        result = []
        primary_type = detected_types[0]
        result.append(f"Detected project type: {primary_type['type'].upper()}")
        result.append(f"Confidence Score: {primary_type['score']}")
        result.append(f"Indicators found: {', '.join(primary_type['indicators'])}")
        
        if primary_type['directories']:
            result.append(f"Relevant directories: {', '.join(primary_type['directories'])}")
        
        # Show other possible types if score is close
        if len(detected_types) > 1 and detected_types[1]['score'] >= primary_type['score'] * 0.7:
            result.append("\nOther possible types:")
            for other_type in detected_types[1:3]:  # Show up to 2 alternatives
                result.append(f"- {other_type['type'].upper()} (score: {other_type['score']})")
        
        return '\n'.join(result)
    except Exception as e:
        return f"Error detecting project type: {e}"

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
    Complete project documentation workflow - detects project, analyzes structure, and generates documentation
    If project_path is not provided, attempts to auto-detect the user's current project
    """
    try:
        # Step 1: Determine the project path with enhanced detection
        if not project_path:
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
                except:
                    pass  # psutil not available or other error
            
            # Method 3: Check current working directory as fallback
            if not detected_path:
                cwd = Path.cwd().resolve()
                cwd_str = str(cwd).lower()
                if (not cwd_str.endswith('documenter') and 
                    not cwd_str.endswith('mcps')):
                    detected_path = str(cwd)
            
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
                            break
            
            project_path = detected_path or "."
        
        base_path = Path(project_path).resolve()
        
        results = []
        results.append("# 🚀 Comprehensive Project Documentation")
        results.append("=" * 60)
        results.append(f"📁 Analyzing project at: {base_path}")
        
        # Show detection method used
        if not project_path or project_path == ".":
            results.append(f"🔍 Auto-detected project directory")
        else:
            results.append(f"📍 Using specified project path")
        results.append("")
        
        if not base_path.exists():
            return f"❌ Project path does not exist: {base_path}"
        
        # Verify this looks like a real project directory
        project_files = list(base_path.iterdir()) if base_path.is_dir() else []
        has_project_indicators = any(
            (base_path / indicator).exists() for indicator in [
                'package.json', 'pyproject.toml', 'requirements.txt', 'pom.xml',
                'Cargo.toml', 'go.mod', 'composer.json', '.git', '.gitignore',
                'src', 'app', 'lib', 'components', 'pages'
            ]
        )
        
        if not has_project_indicators and len(project_files) < 3:
            results.append("⚠️ Warning: This doesn't appear to be a project directory.")
            results.append("💡 Try specifying the project path explicitly in your prompt:")
            results.append("   'Document the project at /path/to/your/project comprehensively'")
            results.append("")
        
        # Continue with the rest of the analysis...
        # Step 2: Detect project type
        results.append("## 🔍 Step 1: Project Type Detection")
        results.append("-" * 40)
        try:
            project_type_result = detect_project_type(str(base_path))
            results.append(project_type_result)
        except Exception as e:
            results.append(f"❌ Error detecting project type: {e}")
        results.append("")
        
        # Step 3: Analyze project structure  
        results.append("## 📊 Step 2: Project Structure Analysis")
        results.append("-" * 40)
        try:
            structure_result = analyze_project_structure(str(base_path))
            results.append(structure_result)
        except Exception as e:
            results.append(f"❌ Error analyzing structure: {e}")
        results.append("")
        
        # Step 4: Analyze configuration files
        results.append("## ⚙️ Step 3: Configuration Analysis")
        results.append("-" * 40)
        
        config_files = [
            "package.json", "pyproject.toml", "requirements.txt", "pom.xml", 
            "Cargo.toml", "composer.json", "go.mod", "pubspec.yaml", 
            "Gemfile", "build.gradle"
        ]
        
        found_configs = []
        for config_file in config_files:
            config_path = base_path / config_file
            if config_path.exists():
                found_configs.append(config_file)
                try:
                    if config_file == "package.json":
                        config_result = analyze_package_json(str(config_path))
                    else:
                        config_result = analyze_project_config(str(config_path))
                    results.append(f"### {config_file}")
                    results.append(config_result)
                    results.append("")
                except Exception as e:
                    results.append(f"❌ Error analyzing {config_file}: {e}")
        
        if not found_configs:
            results.append("ℹ️ No configuration files found to analyze")
        results.append("")
        
        # Step 5: Code metrics
        results.append("## 📈 Step 4: Code Metrics")
        results.append("-" * 40)
        try:
            metrics_result = analyze_code_metrics(str(base_path))
            results.append(metrics_result)
        except Exception as e:
            results.append(f"❌ Error analyzing code metrics: {e}")
        results.append("")
        
        # Step 6: Generate README
        results.append("## 📝 Step 5: README Generation")
        results.append("-" * 40)
        try:
            readme_result = generate_project_readme(str(base_path))
            
            # Optionally write the README file
            readme_path = base_path / "README_GENERATED.md"
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(readme_result)
            
            results.append(f"✅ README generated and saved to: {readme_path}")
            results.append("")
            results.append("### Generated README Preview:")
            results.append(readme_result[:1000] + "..." if len(readme_result) > 1000 else readme_result)
        except Exception as e:
            results.append(f"❌ Error generating README: {e}")
        results.append("")
        
        # Step 7: Summary
        results.append("## ✅ Documentation Complete!")
        results.append("-" * 40)
        results.append(f"📁 Project analyzed: {base_path}")
        results.append(f"⚙️ Config files found: {len(found_configs)}")
        results.append(f"📄 README generated: README_GENERATED.md")
        results.append("")
        results.append("🎉 Your project documentation is ready!")
        
        return '\n'.join(results)
        
    except Exception as e:
        return f"Error in comprehensive documentation: {e}"

if __name__ == "__main__":
    import sys
    # Log to stderr instead of stdout to avoid interfering with MCP protocol
    cwd = os.getcwd()
    print(f"🚀 Universal Project Documenter starting from: {cwd}", file=sys.stderr)
    print("🔧 Ready to document any project!", file=sys.stderr)
    print("📝 Supports: Next.js, React, Node.js, Python, and generic projects", file=sys.stderr)
    mcp.run(transport='stdio')