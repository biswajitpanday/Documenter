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

1. **detect_project_type** - Automatically identify project framework and type
2. **read_file** - Read any file with absolute or relative paths
3. **write_file** - Create or update files with automatic directory creation
4. **read_filenames_in_directory** - List directory contents
5. **analyze_project_structure** - Complete project architecture analysis
6. **analyze_package_json** - Comprehensive package.json analysis with recommendations
7. **generate_component_documentation** - Detailed component documentation
8. **generate_project_readme** - Auto-generate comprehensive README files
9. **get_current_working_directory** - Get server's current working directory

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

- **"Analyze this project structure"** - Get detailed architecture overview
- **"Generate documentation for this component"** - Create component docs
- **"Create a README for this project"** - Auto-generate comprehensive README
- **"What type of project is this?"** - Identify framework and technologies
- **"Analyze the package.json file"** - Get dependency insights and recommendations

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

