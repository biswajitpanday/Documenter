#!/usr/bin/env python3
"""
Documenter MCP Server - Local Version
A local MCP server for project documentation that runs on user's machine
"""

from mcp.server.fastmcp import FastMCP
import os
import json
import re
import sys
import platform
from pathlib import Path
from typing import List, Dict, Optional, Tuple

# Initialize MCP server with clear description
mcp = FastMCP(
    "Documenter",
    description="Local project documentation server - analyzes and documents projects on your machine"
)

# Enhanced project type detection with comprehensive patterns
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
    "nodejs": {
        "indicators": ["package.json", "server.js", "app.js", "index.js"],
        "check_content": {"package.json": ["express", "node", "fastify", "koa"]},
        "important_dirs": ["src", "lib", "routes", "controllers", "middleware"],
        "important_files": ["package.json", "README.md", "index.js", "server.js"],
        "confidence_boost": 1
    },
    "java": {
        "indicators": ["pom.xml", "build.gradle", "gradlew", "build.xml"],
        "check_content": {"pom.xml": ["java", "maven"]},
        "important_dirs": ["src/main/java", "src/test/java", "src/main/resources"],
        "important_files": ["pom.xml", "build.gradle", "README.md", "application.properties"],
        "confidence_boost": 2
    },
    "go": {
        "indicators": ["go.mod", "go.sum", "main.go", "Makefile"],
        "check_content": {"go.mod": ["module ", "go "]},
        "important_dirs": ["cmd", "pkg", "internal", "api", "web"],
        "important_files": ["go.mod", "go.sum", "main.go", "README.md", "Makefile"],
        "confidence_boost": 2
    },
    "rust": {
        "indicators": ["Cargo.toml", "Cargo.lock", "src/main.rs", "src/lib.rs"],
        "check_content": {"Cargo.toml": ["[package]", "edition = "]},
        "important_dirs": ["src", "tests", "examples", "benches"],
        "important_files": ["Cargo.toml", "Cargo.lock", "README.md", "main.rs", "lib.rs"],
        "confidence_boost": 3
    },
    "docker": {
        "indicators": ["Dockerfile", "docker-compose.yml", "docker-compose.yaml"],
        "check_content": {"Dockerfile": ["FROM ", "RUN ", "COPY "]},
        "important_dirs": ["docker", "scripts"],
        "important_files": ["Dockerfile", "docker-compose.yml", "README.md"],
        "confidence_boost": 1
    }
}

@mcp.tool()
def detect_project_type(base_path: str = ".") -> str:
    """
    Automatically detect the type of project with enhanced accuracy.
    Works with local project files - no path specification needed.
    """
    try:
        # Use current working directory by default
        project_path = Path(base_path).resolve()
        
        if not project_path.exists():
            return f"❌ Project path does not exist: {project_path}\n💡 Make sure you're in the correct project directory."
        
        detected_types = []
        
        for project_type, config in PROJECT_CONFIGS.items():
            score = 0
            found_indicators = []
            
            # Check for indicator files
            for indicator in config["indicators"]:
                if "*" in indicator:
                    matches = list(project_path.glob(indicator))
                    if matches:
                        found_indicators.append(f"{indicator} ({len(matches)} files)")
                        score += 2
                elif (project_path / indicator).exists():
                    found_indicators.append(indicator)
                    score += 2
            
            # Check file contents
            for file_to_check, content_keys in config["check_content"].items():
                file_path = project_path / file_to_check
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
                if (project_path / important_dir).exists():
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
        
        if not detected_types:
            return f"Detected project type: GENERIC\nPath analyzed: {project_path}\nNo specific framework detected"
        
        primary_type = detected_types[0]
        result = []
        result.append(f"Detected project type: {primary_type['type'].upper()}")
        result.append(f"Confidence Score: {primary_type['score']}")
        result.append(f"Path analyzed: {project_path}")
        
        if primary_type['indicators']:
            result.append(f"Indicators found: {', '.join(primary_type['indicators'])}")
        
        if primary_type['directories']:
            result.append(f"Relevant directories: {', '.join(primary_type['directories'])}")
        
        return '\n'.join(result)
    except Exception as e:
        return f"Error detecting project type: {e}"

@mcp.tool()
def read_file(file_path: str) -> str:
    """
    Read a file from the current project directory.
    Works with local project files.
    """
    try:
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
    Read filenames in a directory from the current project.
    Works with local project files.
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
def analyze_project_structure(base_path: str = ".") -> str:
    """
    Analyze and document the complete project structure.
    Works with local project files.
    """
    try:
        project_path = Path(base_path).resolve()
        project_info = detect_project_type(str(project_path))
        
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
        
        structure.append(project_path.name + "/")
        generate_tree(project_path, "", max_depth=4)
        structure.append("```")
        
        return '\n'.join(structure)
    except Exception as e:
        return f"Error analyzing project structure: {e}"

@mcp.tool()
def analyze_package_json(file_path: str = "package.json") -> str:
    """
    Comprehensive analysis of package.json.
    Works with local project files.
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
        
        return '\n'.join(analysis)
    except Exception as e:
        return f"Error analyzing package.json: {e}"

@mcp.tool()
def generate_project_readme(base_path: str = ".") -> str:
    """
    Generate a comprehensive README.md for the current project.
    Works with local project files.
    """
    try:
        project_path = Path(base_path).resolve()
        
        # Detect project type and get package info
        project_type = detect_project_type(str(project_path))
        
        readme = []
        
        # Try to get project name from package.json or directory name
        project_name = project_path.name
        description = "A software project"
        
        package_json_path = project_path / "package.json"
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
        add_structure(project_path, "", max_depth=3)
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
def document_project_comprehensive(project_path: str = ".") -> str:
    """
    Complete project documentation workflow.
    Works with local project files - no path specification needed.
    """
    try:
        project_path = Path(project_path).resolve()
        
        results = []
        results.append("# 🚀 Universal Project Documentation")
        results.append("=" * 70)
        results.append(f"📁 Project Location: {project_path}")
        results.append(f"🖥️  Platform: {platform.system()} {platform.release()}")
        results.append(f"🐍 Python: {sys.version.split()[0]}")
        results.append("")
        
        if not project_path.exists():
            return f"❌ Project path does not exist: {project_path}"
        
        # Step 1: Project type detection
        results.append("## 🔍 Step 1: Project Type Detection")
        results.append("-" * 50)
        try:
            project_type_result = detect_project_type(str(project_path))
            results.append(project_type_result)
        except Exception as e:
            results.append(f"❌ Error in project type detection: {e}")
        results.append("")
        
        # Step 2: Project structure analysis
        results.append("## 📊 Step 2: Project Structure Analysis")
        results.append("-" * 50)
        try:
            structure_result = analyze_project_structure(str(project_path))
            results.append(structure_result)
        except Exception as e:
            results.append(f"❌ Error in structure analysis: {e}")
        results.append("")
        
        # Step 3: Package.json analysis (if exists)
        package_json_path = project_path / "package.json"
        if package_json_path.exists():
            results.append("## ⚙️ Step 3: Package.json Analysis")
            results.append("-" * 50)
            try:
                package_result = analyze_package_json(str(package_json_path))
                results.append(package_result)
            except Exception as e:
                results.append(f"❌ Error analyzing package.json: {e}")
            results.append("")
        
        # Step 4: README generation
        results.append("## 📝 Step 4: README Generation")
        results.append("-" * 50)
        try:
            readme_result = generate_project_readme(str(project_path))
            
            # Save the README file
            readme_path = project_path / "README_GENERATED.md"
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
        
        # Step 5: Summary
        results.append("## ✅ Documentation Summary")
        results.append("-" * 50)
        results.append(f"📁 **Project Analyzed**: {project_path}")
        results.append(f"📄 **Documentation Generated**: README_GENERATED.md")
        results.append("")
        
        results.append("🎉 **Project documentation completed successfully!**")
        results.append("")
        results.append("💡 **Tip**: You can now use the generated README_GENERATED.md as a starting point")
        results.append("for your project documentation.")
        
        return '\n'.join(results)
        
    except Exception as e:
        return f"❌ Critical error in comprehensive documentation: {e}"

if __name__ == "__main__":
    print("🚀 Documenter MCP Server (Local) starting...", file=sys.stderr)
    print("📁 Working directory:", Path.cwd(), file=sys.stderr)
    print("🔧 Ready to analyze local projects!", file=sys.stderr)
    mcp.run(transport='stdio') 