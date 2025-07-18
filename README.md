# 🚀 Universal Project Documenter - MCP Server

**Intelligent documentation generator for any project type. Automatically detects project structure, analyzes dependencies, and generates comprehensive documentation.**

[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-blue)](https://modelcontextprotocol.io)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-green)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![UV](https://img.shields.io/badge/UV-Package%20Manager-orange)](https://github.com/astral-sh/uv)

## ✨ **What Makes This Universal**

🌍 **Works with ANY project type**: React, Next.js, Angular, Vue, Python, .NET, Java, Kotlin, Go, Rust, PHP, Flutter, Swift, Ruby, and more  
🎯 **Smart Auto-Detection**: Automatically finds your actual project directory (not the MCP server's directory)  
🔧 **IDE Integration**: Compatible with Cursor, VS Code, Windsurf, Claude Desktop, and other MCP-enabled editors  
⚡ **Zero Configuration**: No hardcoded paths - works universally for any developer  
📚 **Comprehensive Analysis**: From project structure to README generation in one command  

## 🎪 **Perfect Universal Prompts**

```
✅ "Document my entire project comprehensively"
✅ "I need comprehensive documentation for this codebase"
✅ "Create complete project documentation with analysis and README"
✅ "Generate comprehensive documentation for this project"
```

## 🛠️ **Supported Project Types (25+)**

| Frontend | Backend | Mobile | Languages | Infrastructure |
|----------|---------|--------|-----------|----------------|
| React ⚛️ | Node.js 🟢 | Flutter 📱 | Python 🐍 | Docker 🐳 |
| Next.js ▲ | Express 🌐 | Swift 🍎 | Java ☕ | Terraform 🏗️ |
| Angular 🅰️ | FastAPI ⚡ | React Native ⚛️📱 | Kotlin 📱 | Kubernetes ☸️ |
| Vue.js 🖖 | Django 🎸 | | Go 🐹 | |
| Svelte ⚡ | Flask 🌶️ | | Rust 🦀 | |
| | Laravel 🎭 | | PHP 🐘 | |
| | Ruby on Rails 💎 | | C# .NET 🔷 | |

## 🚀 **Quick Start**

### **1. Installation**

```bash
# Clone and setup
git clone https://github.com/your-username/universal-project-documenter.git
cd universal-project-documenter
uv sync  # or pip install -e .

# Test installation
uv run python test_documenter.py
# Expected: ✅ Passed: 16/16 🎉 All tests passed!
```

### **2. IDE Configuration**

#### **🎯 Cursor IDE** (Recommended)

1. Open **Settings** → **Features** → **Model Context Protocol**
2. Add this configuration:

```json
{
  "mcpServers": {
    "documenter": {
      "command": "uv",
      "args": ["run", "python", "main.py"],
      "cwd": "/absolute/path/to/universal-project-documenter"
    }
  }
}
```

#### **🔷 VS Code**

1. Install MCP Extension
2. Add to settings:

```json
{
  "mcp.servers": {
    "documenter": {
      "command": "uv",
      "args": ["run", "python", "main.py"],
      "cwd": "/absolute/path/to/universal-project-documenter"
    }
  }
}
```

#### **🌊 Windsurf / 🤖 Claude Desktop**

```json
{
  "mcpServers": {
    "documenter": {
      "command": "uv",
      "args": ["run", "python", "main.py"],
      "cwd": "/absolute/path/to/universal-project-documenter"
    }
  }
}
```

**For Claude Desktop**, place config in:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

### **3. Usage**

1. **Open your project** in your IDE
2. **Ask for documentation**: `"I need comprehensive documentation for this codebase"`
3. **Watch the magic happen** ✨

## 🎯 **16 Powerful Tools**

| **🔥 Essential** | **🔧 Analysis** | **📝 Generation** | **🔍 Utilities** |
|------------------|-----------------|-------------------|------------------|
| **📊 document_project_comprehensive** | 🔍 detect_project_type | 📄 generate_project_readme | 📂 read_file |
| **🎯 auto_detect_user_project** | 📋 analyze_project_structure | 📚 generate_component_documentation | ✏️ write_file |
| **📁 get_cursor_working_directory** | ⚙️ analyze_package_json | | 📝 read_filenames_in_directory |
| | 🔧 analyze_project_config | | 🔍 find_files_by_pattern |
| | 📊 analyze_code_metrics | | 📚 batch_read_files |
| | 🔍 scan_for_todos_and_fixmes | | |

### **🌟 Key Tool Highlights**

- **📊 document_project_comprehensive**: Complete workflow - detects project, analyzes structure, generates README
- **🎯 auto_detect_user_project**: Smart detection of your actual project directory (not MCP server directory)
- **🔍 detect_project_type**: Enhanced with 25+ project types and confidence scoring
- **🔧 analyze_project_config**: Universal config analysis (package.json, pom.xml, Cargo.toml, composer.json, etc.)
- **📊 analyze_code_metrics**: Technology distribution and code statistics
- **🔍 scan_for_todos_and_fixmes**: Find TODO, FIXME, HACK comments across codebase

## 📖 **Usage Examples**

### **🎯 One-Command Documentation**
```
"Document my entire project comprehensively"
```
**Result**: Complete analysis with README_GENERATED.md in your project directory

### **🔍 Project Type Detection**
```
"What type of project is this and analyze its structure"
```
**Result**: 
```
Detected project type: NEXTJS
Confidence Score: 12 (Very High)
Indicators found: next.config.js, package.json (contains next, @next/)
Framework ecosystem: React-based full-stack framework with SSR/SSG
```

### **📊 Technology Analysis**
```
"Analyze the code metrics and technology distribution"
```
**Result**: File counts, lines of code, technology percentages, largest files

### **🔧 Configuration Analysis**
```
"Analyze all configuration files in this project"
```
**Result**: Detailed analysis of package.json, pom.xml, Cargo.toml, etc.

## 🌟 **Advanced Features**

### **🎯 Universal Auto-Detection**
- **5-tier detection system**: Environment variables → Process tree → Git root → Project indicators → Fallback
- **Smart exclusions**: Avoids MCP server directory, system folders
- **IDE-aware**: Detects Cursor, VS Code, Windsurf working directories
- **Cross-platform**: Windows, macOS, Linux support

### **🧠 Intelligent Project Analysis**
- **Enhanced scoring**: Confidence levels from "Very Low" to "Very High"
- **Multi-factor detection**: File indicators + content analysis + directory structure
- **Framework ecosystem info**: Detailed context for each project type
- **Alternative suggestions**: Shows other possible project types

### **📚 Comprehensive Documentation Generation**
- **Complete workflow**: Detection → Analysis → Structure → Config → Metrics → README
- **Smart truncation**: Handles large files gracefully
- **Error resilience**: Continues analysis even if some steps fail
- **Professional output**: Structured, readable, actionable documentation

## 🔧 **Platform-Specific Setup**

### **🪟 Windows**

```powershell
# Install UV
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Setup project
git clone https://github.com/your-username/universal-project-documenter.git
cd universal-project-documenter
uv sync
```

**Cursor Configuration (Windows):**
```json
{
  "mcpServers": {
    "documenter": {
      "command": "C:\\Users\\YourName\\.cargo\\bin\\uv.exe",
      "args": ["run", "python", "main.py"],
      "cwd": "C:\\path\\to\\universal-project-documenter"
    }
  }
}
```

### **🍎 macOS / 🐧 Linux**

```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Setup project
git clone https://github.com/your-username/universal-project-documenter.git
cd universal-project-documenter
uv sync

# Make scripts executable (Linux)
chmod +x run_mcp.sh
```

## ✅ **Verification & Testing**

### **Basic Test**
```bash
cd universal-project-documenter
uv run python test_documenter.py
```
**Expected Output**: `✅ Passed: 16/16 🎉 All tests passed!`

### **Auto-Detection Test**
```bash
uv run python test_portfolio.py
```

### **In IDE Test**
1. Restart your IDE after configuration
2. Try: `"I need comprehensive documentation for this codebase"`
3. Should see comprehensive project analysis with README generation

## 🔧 **Troubleshooting**

### **❌ Common Issues & Solutions**

#### **"No MCP servers found"**
- ✅ Check absolute paths in configuration
- ✅ Verify script execution permissions
- ✅ Restart IDE after configuration changes

#### **"Python/UV not found"**
- ✅ Install UV: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- ✅ Check PATH: Ensure UV/Python are in system PATH
- ✅ Use absolute paths in configuration

#### **"Wrong project detected"**
- ✅ Ensure IDE is opened in your project root directory
- ✅ Use explicit path: `"Document the project at /path comprehensively"`

#### **Module/Permission Errors**
- ✅ Run `uv sync` to install dependencies
- ✅ Check file permissions: `chmod +x run_mcp.sh` (Unix)
- ✅ Use absolute paths in MCP configuration

### **🐛 Debug Mode**

```bash
# Enable debug logging
DEBUG=1 uv run python main.py

# Test specific project
uv run python -c "
from main import detect_project_type
print(detect_project_type('/path/to/your/project'))
"
```

## 🎉 **Success Indicators**

When properly configured, you'll see:

✅ **IDE Status**: Green MCP server indicator  
✅ **Tool Count**: "16 tools enabled" in IDE status  
✅ **Auto-Detection**: Correctly identifies your project directory  
✅ **Project Type**: Accurate framework/language detection with confidence score  
✅ **Documentation**: README_GENERATED.md created in your project  

## 🌟 **Real-World Examples**

### **React Project**
```
Input: "Document this React application comprehensively"
Output: 
- Detects React with high confidence
- Analyzes package.json dependencies  
- Documents component structure
- Generates comprehensive README
```

### **Python/Django Project**
```
Input: "I need comprehensive documentation for this codebase"
Output:
- Detects Django framework
- Analyzes requirements.txt/pyproject.toml
- Documents models, views, settings
- Creates installation and usage guide
```

### **Java/Spring Boot Project**
```
Input: "Create complete project documentation"
Output:
- Detects Java with Maven/Gradle
- Analyzes pom.xml/build.gradle
- Documents controllers, services, entities
- Generates API documentation structure
```

## 🤝 **Contributing**

We welcome contributions! This project follows Context7-inspired patterns:

1. **Universal compatibility** - works across all IDEs and platforms
2. **Smart defaults** - minimal configuration required
3. **Comprehensive error handling** - graceful failure modes
4. **Clear documentation** - examples for every use case

## 📄 **License**

MIT License - see [LICENSE](LICENSE) file for details.

## 🚀 **Advanced Configuration**

### **Environment Variables**
```bash
export CURSOR_CWD="/path/to/project"        # Set project detection preference
export DOCUMENTER_DEBUG=1                   # Enable debug logging
export DOCUMENTER_MAX_FILE_SIZE=5000000     # Set max file size limit
```

### **Custom Configuration**
Create `config.json` in the project directory:
```json
{
  "max_file_size": 5000000,
  "excluded_patterns": ["node_modules", ".git", "__pycache__"],
  "supported_extensions": [".py", ".js", ".ts", ".java", ".rs"],
  "detection_strategies": ["env_vars", "process_tree", "git_root", "indicators"]
}
```

---

💡 **Tip**: Works best when your IDE is opened directly in your project root directory!

⭐ **Star this repository if it helps your documentation workflow!**

