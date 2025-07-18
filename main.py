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
    "nodejs": {
        "indicators": ["package.json"],
        "check_content": {"package.json": "node"},
        "important_dirs": ["src", "lib", "routes", "controllers"],
        "important_files": ["package.json", "README.md", "index.js", "server.js"]
    },
    "python": {
        "indicators": ["requirements.txt", "pyproject.toml", "setup.py"],
        "check_content": {},
        "important_dirs": ["src", "lib", "tests"],
        "important_files": ["requirements.txt", "README.md", "setup.py", "pyproject.toml"]
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
        
        for project_type, config in PROJECT_CONFIGS.items():
            if project_type == "generic":
                continue
                
            # Check for indicator files
            indicators_found = []
            for indicator in config["indicators"]:
                if (base_path / indicator).exists():
                    indicators_found.append(indicator)
            
            # Check file contents
            content_matches = 0
            for file_to_check, content_key in config["check_content"].items():
                file_path = base_path / file_to_check
                if file_path.exists():
                    try:
                        if file_to_check.endswith(".json"):
                            with open(file_path, 'r', encoding='utf-8') as f:
                                data = json.load(f)
                                if content_key in str(data).lower():
                                    content_matches += 1
                    except:
                        pass
            
            # Determine if this project type matches
            if indicators_found and (not config["check_content"] or content_matches > 0):
                return f"Detected project type: {project_type.upper()}\nIndicators found: {', '.join(indicators_found)}"
        
        return "Detected project type: GENERIC\nNo specific framework detected"
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
def get_current_working_directory() -> str:
    """
    Get the current working directory where the MCP server is running
    """
    try:
        cwd = Path.cwd().resolve()
        return f"📍 Current working directory: {cwd}"
    except Exception as e:
        return f"Error getting current directory: {e}"

if __name__ == "__main__":
    import sys
    # Log to stderr instead of stdout to avoid interfering with MCP protocol
    cwd = os.getcwd()
    print(f"🚀 Universal Project Documenter starting from: {cwd}", file=sys.stderr)
    print("🔧 Ready to document any project!", file=sys.stderr)
    print("📝 Supports: Next.js, React, Node.js, Python, and generic projects", file=sys.stderr)
    mcp.run(transport='stdio')