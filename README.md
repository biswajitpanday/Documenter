# Universal Project Documenter - MCP Server

A Model Context Protocol (MCP) server that provides intelligent documentation tools for any project type. Automatically detects project structure, analyzes dependencies, and generates comprehensive documentation.

## Features

- **Universal Project Detection**: Automatically identifies Next.js, React, Node.js, Python, and other project types
- **Intelligent Documentation**: Generates comprehensive README files and component documentation
- **Project Structure Analysis**: Creates detailed architecture overviews with file categorization
- **Package Analysis**: Provides insights and recommendations for dependencies
- **File System Operations**: Read, write, and analyze files with directory traversal
- **Component Documentation**: Specialized documentation for React/Vue/TypeScript components

## Tools Available

1. **🚀 document_project_comprehensive** - **NEW!** Complete workflow that auto-detects your project and generates full documentation
2. **🔍 auto_detect_user_project** - **NEW!** Smart detection of your actual project directory (not MCP server directory)
3. **detect_project_type** - Automatically identify project framework and type
4. **read_file** - Read any file with absolute or relative paths
5. **write_file** - Create or update files with automatic directory creation
6. **read_filenames_in_directory** - List directory contents
7. **analyze_project_structure** - Complete project architecture analysis
8. **analyze_package_json** - Comprehensive package.json analysis with recommendations
9. **analyze_project_config** - **NEW!** Analyze any config file (pom.xml, Cargo.toml, composer.json, etc.)
10. **generate_component_documentation** - Detailed component documentation
11. **generate_project_readme** - Auto-generate comprehensive README files
12. **batch_read_files** - **NEW!** Read multiple files at once
13. **find_files_by_pattern** - **NEW!** Search files with wildcards (*.js, **/*.py, etc.)
14. **analyze_code_metrics** - **NEW!** Code statistics and technology distribution analysis
15. **scan_for_todos_and_fixmes** - **NEW!** Find TODO, FIXME, HACK comments in codebase
16. **get_cursor_working_directory** - Get Cursor's current working directory

## Prerequisites

- Python 3.11+
- UV package manager

## Installation

1. **Clone or download this repository**

2. **Install UV (if not already installed)**:
   ```bash
   # Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   
   # macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Navigate to the project directory**:
   ```bash
   cd path/to/Documenter
   ```

4. **Install dependencies**:
   ```bash
   uv sync
   ```

## Setup for Cursor IDE

1. **Open Cursor Settings** (Ctrl/Cmd + ,)

2. **Search for "mcp"** in settings

3. **Edit the MCP configuration file** and add:
   ```json
   {
     "mcpServers": {
       "documenter": {
         "command": "C:\\path\\to\\your\\Documenter\\run_mcp.bat",
         "args": [],
         "cwd": "C:\\path\\to\\your\\Documenter"
       }
     }
   }
   ```

4. **Replace the paths** with your actual Documenter folder location

5. **Restart Cursor** - You should see a green indicator showing "9 tools enabled"

## Usage

Once configured in Cursor, you can use natural language to:

- **"I need comprehensive documentation for this codebase including project type detection and README generation"** - Complete workflow with auto-detection
- **"Document my entire project comprehensively"** - Full analysis and documentation generation
- **"Analyze this project structure"** - Get detailed architecture overview
- **"Generate documentation for this component"** - Create component docs
- **"Create a README for this project"** - Auto-generate comprehensive README
- **"What type of project is this?"** - Identify framework and technologies
- **"Analyze the package.json file"** - Get dependency insights and recommendations
- **"Show me code metrics and technology distribution"** - Get detailed statistics
- **"Find all TODO comments in the codebase"** - Scan for code annotations

## 🎯 **Smart Project Detection**

**NEW!** The documenter now intelligently detects **your** project directory (not the MCP server's directory):

### ✅ **Recommended Usage**
```
"I need comprehensive documentation for this codebase including project type detection and README generation"
```
This triggers the **complete workflow** that:
1. 🔍 Auto-detects your actual project directory
2. 📊 Analyzes project type and structure  
3. ⚙️ Examines configuration files
4. 📈 Generates code metrics
5. 📝 Creates comprehensive README
6. 💾 Saves documentation to your project folder

### 🎯 **For Specific Projects**
```
"Document the project at C:\path\to\your\project comprehensively"
"Analyze project structure for the codebase at /absolute/path"
```

### 📚 **See Also**
- 📖 **[USAGE_GUIDE.md](USAGE_GUIDE.md)** - Comprehensive usage examples and troubleshooting
- 🧪 **[test_portfolio.py](test_portfolio.py)** - Example of documenting a different project

## Example Outputs

### Project Structure Analysis
- **Architecture diagrams** with component relationships
- **File categorization** (components, pages, utilities, etc.)
- **Technology stack** identification
- **Performance insights** and optimization suggestions

### Component Documentation
- **Props interface** documentation
- **Usage examples** with code snippets
- **Dependencies** and import statements
- **Best practices** and recommendations

### README Generation
- **Comprehensive project overview** with features
- **Installation and setup** instructions
- **Usage examples** and API documentation
- **Contributing guidelines** and development workflow

## Publishing Your MCP Server

### Option 1: GitHub Repository

1. **Initialize Git** (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **Create GitHub repository** and push:
   ```bash
   git remote add origin https://github.com/yourusername/universal-project-documenter.git
   git push -u origin main
   ```

3. **Add installation instructions** in your README for others:
   ```bash
   git clone https://github.com/yourusername/universal-project-documenter.git
   cd universal-project-documenter
   uv sync
   ```

### Option 2: PyPI Package

1. **Update pyproject.toml** with your details:
   ```toml
   [project]
   name = "universal-project-documenter"
   version = "1.0.0"
   description = "MCP server for universal project documentation"
   authors = [
       {name = "Your Name", email = "your.email@example.com"}
   ]
   ```

2. **Build and publish**:
   ```bash
   uv build
   uv publish
   ```

### Option 3: Docker Container

1. **Create Dockerfile**:
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY . .
   RUN pip install uv && uv sync
   CMD ["uv", "run", "python", "main.py"]
   ```

2. **Build and push**:
   ```bash
   docker build -t universal-project-documenter .
   docker push yourusername/universal-project-documenter
   ```

## File Structure

```
Documenter/
├── main.py                    # MCP server implementation
├── run_mcp.bat               # Windows batch launcher
├── cursor-mcp-config-batch.json # Cursor configuration example
├── pyproject.toml            # Project dependencies
├── uv.lock                   # Lock file
├── .python-version           # Python version
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

## Troubleshooting

### Red Status in Cursor
- Ensure the batch file path is correct in your MCP config
- Verify UV is installed and accessible
- Check that all dependencies are installed (`uv sync`)
- Restart Cursor after configuration changes

### Permission Issues
- On Windows, ensure the batch file has execution permissions
- On macOS/Linux, make sure the script is executable: `chmod +x run_mcp.sh`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with `uv run python main.py`
5. Submit a pull request

## License

MIT License - feel free to use and modify as needed.

## Support

For issues and questions, please create an issue in the GitHub repository or reach out to the maintainer.

