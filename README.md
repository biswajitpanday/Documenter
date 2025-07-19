# Documenter MCP Server

🚀 **Intelligent documentation generator for any project type** - Automatically detects project structure, analyzes dependencies, and generates comprehensive documentation.

## ✨ **Features**

- **🎯 Multi-Platform Support**: Works with 25+ project types (React, Next.js, Angular, Vue, Python, .NET, Java, etc.)
- **🔍 Automatic Detection**: Enhanced project type detection with confidence scoring
- **📊 Comprehensive Analysis**: Project structure, dependencies, code metrics, and more
- **📝 Documentation Generation**: Automatic README generation and component documentation
- **🔧 MCP Protocol**: Full Model Context Protocol support for AI assistants

## 🌐 **Live Service**

**URL**: `https://documenter-mcp.onrender.com`

**Status**: ✅ Running and fully functional

## 🚀 **Quick Start**

### **Remote Usage (Recommended)**
Simply add this to your IDE's MCP configuration:

#### **Cursor IDE:**
```json
{
  "mcpServers": {
    "documenter": {
      "url": "https://documenter-mcp.onrender.com"
    }
  }
}
```

#### **VS Code:**
```json
{
  "mcp.servers": {
    "documenter": {
      "url": "https://documenter-mcp.onrender.com"
    }
  }
}
```

### **Local Development**
```bash
# Clone the repository
git clone <repository-url>
cd Documenter

# Run the server locally
python server.py
```

## 🛠️ **Available Tools (16 Total)**

| **Core Tools** | **Analysis Tools** | **Documentation Tools** |
|----------------|-------------------|------------------------|
| 🔍 `detect_project_type` | 📊 `analyze_project_structure` | 📝 `generate_project_readme` |
| 📄 `read_file` | 📦 `analyze_package_json` | 📚 `document_project_comprehensive` |
| 📂 `read_filenames_in_directory` | 📈 `analyze_code_metrics` | 🔍 `find_files_by_pattern` |
| ✏️ `write_file` | 🐛 `scan_for_todos_and_fixmes` | |

## 🎯 **Supported Project Types**

| **Frontend** | **Backend** | **Mobile** | **Languages** | **Infrastructure** |
|--------------|-------------|------------|---------------|-------------------|
| React ⚛️ | Node.js 🟢 | Flutter 📱 | Python 🐍 | Docker 🐳 |
| Next.js ▲ | Express 🌐 | | Java ☕ | Terraform 🏗️ |
| Angular 🅰️ | FastAPI ⚡ | | Go 🐹 | |
| Vue.js 🖖 | Django 🎸 | | Rust 🦀 | |
| Svelte ⚡ | Flask 🌶️ | | PHP 🐘 | |

## 📖 **Usage Examples**

### **One-Command Documentation**
```
"Document my entire project comprehensively"
```
**Result**: Complete analysis with README generation

### **Project Type Detection**
```
"What type of project is this and analyze its structure"
```
**Result**: 
```
Detected project type: NEXTJS
Confidence Score: 12 (Very High)
Indicators found: next.config.js, package.json (contains next, @next/)
```

### **Technology Analysis**
```
"Analyze the code metrics and technology distribution"
```
**Result**: File counts, lines of code, technology percentages

## 🏗️ **Architecture**

- **Lightweight**: Uses only Python standard library
- **Fast**: No heavy dependencies to load
- **Reliable**: Proper error handling and logging
- **Scalable**: Deployed on Railway with automatic scaling

## 📁 **Project Structure**

```
Documenter/
├── server.py              # Main MCP server (Railway deployment)
├── main.py               # Local MCP server (development)
├── railway.json          # Railway configuration
├── requirements.txt      # Dependencies (minimal)
├── README.md            # This file
├── LICENSE              # MIT License
└── .gitignore           # Git ignore file
```

## 🔧 **Technical Details**

- **Framework**: Pure Python with HTTP server
- **Protocol**: Model Context Protocol (MCP) 2024-11-05
- **Deployment**: Railway (serverless)
- **Dependencies**: None (uses only standard library)
- **Performance**: Fast startup, low memory footprint

## 🎉 **Benefits**

✅ **No Local Setup**: Just add the URL to your IDE  
✅ **Always Available**: 24/7 service on Railway  
✅ **Cross-Platform**: Works on any device with internet  
✅ **Professional**: Similar to Context7 and other MCP services  
✅ **Lightweight**: Fast and reliable  

## 📄 **License**

MIT License - see [LICENSE](LICENSE) file for details.

---

⭐ **Star this repository if it helps your documentation workflow!**

