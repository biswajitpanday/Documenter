# 📚 Universal Project Documenter - Usage Guide

## 🎯 **Automatic Project Detection** 

The Universal Project Documenter **automatically detects your project directory** wherever Cursor IDE is running. No hardcoded paths, no manual configuration - it just works!

## 🔧 **How Auto-Detection Works**

The MCP server uses multiple intelligent methods to find your actual project:

### 🔍 **Detection Methods (in order of priority):**
1. **IDE Environment Variables** - Checks `CURSOR_CWD`, `VSCODE_CWD`, etc.
2. **Parent Process Detection** - Identifies Cursor/VS Code working directory
3. **Current Working Directory** - Where the IDE opened the project
4. **Project Indicator Search** - Looks for `package.json`, `.git`, etc. in parent directories
5. **Graceful Fallback** - Uses current directory as last resort

### ✅ **Smart Exclusions:**
- ❌ Skips MCP server's own directory
- ❌ Avoids system directories (`Program Files`, `System32`)
- ❌ Excludes non-project locations
- ✅ Finds YOUR actual project every time

## 🚀 **Recommended Usage**

### **🎯 Perfect Prompts** (Auto-Detection)

These prompts trigger the **comprehensive workflow** that automatically finds and documents your project:

```
"I need comprehensive documentation for this codebase including project type detection and README generation"

"Document my entire project comprehensively"

"Create complete project documentation with analysis and README"

"Generate comprehensive documentation for this project"
```

### **📍 Explicit Path Prompts** (Backup Option)

Only needed if auto-detection fails:

```
"Document the project at /absolute/path/to/your/project comprehensively"

"Analyze project structure for the codebase at C:\path\to\project"

"Generate README for project located at /Users/username/myproject"
```

## 🛠️ **Available Tools & When They're Used**

### 🚀 **Primary Tools** (Most Useful)

| Tool | Purpose | Triggered By |
|------|---------|--------------|
| `document_project_comprehensive` | **Complete workflow** - auto-detects project, analyzes everything, generates docs | "comprehensive documentation", "document my project" |
| `auto_detect_user_project` | Smart project detection and validation | "detect my project", "find project directory" |
| `detect_project_type` | Framework identification | "what type of project", "identify framework" |
| `generate_project_readme` | README creation | "create README", "generate README" |

### 📊 **Analysis Tools**

| Tool | Purpose | Triggered By |
|------|---------|--------------|
| `analyze_project_structure` | Directory tree & architecture | "analyze structure", "project architecture" |
| `analyze_code_metrics` | Statistics & technology breakdown | "code metrics", "technology distribution" |
| `scan_for_todos_and_fixmes` | Find code annotations | "find TODOs", "scan for FIXME" |
| `analyze_package_json` | Node.js dependency analysis | "analyze package.json", "dependency insights" |
| `analyze_project_config` | Config file analysis (pom.xml, Cargo.toml, etc.) | "analyze [config-file]" |

### 📁 **File Operations**

| Tool | Purpose | Triggered By |
|------|---------|--------------|
| `read_file` | Read specific files | "read [filename]", "show file contents" |
| `find_files_by_pattern` | Search files by pattern | "find *.js files", "locate all Python files" |
| `batch_read_files` | Read multiple files | "read package.json and README.md" |
| `generate_component_documentation` | Document React/Vue components | "document this component", "analyze [component].tsx" |

## 🎪 **Demo Scenarios**

### **Scenario 1: Any Developer, Any Project**
```
User (in their React project): "I need comprehensive documentation for this codebase"

MCP Response:
✅ Auto-detects: /Users/developer/my-react-app
✅ Identifies: React/TypeScript project
✅ Analyzes: package.json, components, src structure
✅ Generates: Comprehensive README.md
✅ Saves to: /Users/developer/my-react-app/README_GENERATED.md
```

### **Scenario 2: Different Developer, Different Project**
```
User (in their Python project): "Document my entire project comprehensively"

MCP Response:
✅ Auto-detects: /home/dev/my-python-api
✅ Identifies: Python/FastAPI project
✅ Analyzes: pyproject.toml, requirements.txt, src structure
✅ Generates: Comprehensive README.md
✅ Saves to: /home/dev/my-python-api/README_GENERATED.md
```

### **Scenario 3: Corporate Enterprise Project**
```
User (in their .NET solution): "Generate comprehensive documentation for this project"

MCP Response:
✅ Auto-detects: C:\Projects\EnterpriseSolution
✅ Identifies: .NET/C# solution
✅ Analyzes: .sln, .csproj files, project structure
✅ Generates: Comprehensive README.md
✅ Saves to: C:\Projects\EnterpriseSolution\README_GENERATED.md
```

## 🔄 **Universal Compatibility**

### **Works With Any:**
- 🖥️ **Operating System**: Windows, macOS, Linux
- 🏗️ **Project Type**: React, Vue, Python, .NET, Java, Go, Rust, PHP, etc.
- 📁 **Directory Structure**: Any valid project layout
- 🛠️ **IDE**: Cursor, VS Code, or any editor that sets working directory

### **Automatically Detects:**
- 📦 **Package Managers**: npm, pip, cargo, maven, gradle, composer, etc.
- ⚙️ **Config Files**: package.json, pyproject.toml, pom.xml, Cargo.toml, etc.
- 🏗️ **Frameworks**: Next.js, React, Django, FastAPI, Spring Boot, etc.
- 📂 **Project Structure**: src/, app/, components/, tests/, docs/, etc.

## 🎯 **Best Practices**

### ✅ **Recommended Approach**
```
✅ "Document my entire project comprehensively"
✅ "I need comprehensive documentation for this codebase"
✅ "Create complete project documentation with analysis"
✅ "Generate comprehensive docs for this project"
```

### ⚠️ **Fallback Options**
```
🔧 "Document the project at [specific-path] comprehensively"
🔧 "Analyze project structure for the codebase at [path]"
```

### ❌ **Avoid These**
```
❌ "Help me understand this code"
❌ "What does this function do?"
❌ "How do I install dependencies?"
❌ "Debug this error"
```

## 🚀 **Universal Examples**

### **For Any Portfolio Project**
```
"I need comprehensive documentation for my portfolio project including structure analysis and README generation"
```

### **For Any Open Source Project**
```
"Document this open source project comprehensively - detect type, analyze dependencies, and create documentation"
```

### **For Any Corporate Project**
```
"Generate complete project documentation including code metrics, configuration analysis, and README for this application"
```

## 🔧 **Troubleshooting**

### **Issue: Auto-detection picks wrong directory**
**Solution**: Use explicit path
```
"Document the project at /your/actual/project/path comprehensively"
```

### **Issue: No project indicators found**
**Response**: You'll see a helpful warning with suggestions
```
⚠️ Warning: This doesn't appear to be a project directory.
💡 Try specifying the project path explicitly in your prompt
```

### **Issue: README saved to wrong location**
**How it works**: README_GENERATED.md is always saved to the detected project directory

## 📈 **Pro Tips**

1. **Trust the auto-detection** → It's designed to find your actual project
2. **Use "comprehensive" keyword** → Triggers the full workflow  
3. **Open your project in Cursor first** → Ensures correct working directory
4. **Check the detection output** → Shows which directory was analyzed
5. **Specify path if needed** → Fallback option always available

## 🎉 **Success Indicators**

When working correctly, you should see:
- ✅ **Project path**: Shows YOUR actual project directory
- ✅ **Project type**: Matches your actual framework (React, Python, etc.)
- ✅ **Config files**: Finds your package.json, pyproject.toml, etc.
- ✅ **README location**: Saved to YOUR project folder
- ✅ **Technology stack**: Reflects your actual dependencies

## 🌍 **Universal Compatibility Promise**

This documenter works for **any developer, any project, anywhere** - no configuration needed! 🚀 