# 🌐 Cloud-Based Natural Language Documentation Guide

## 🎯 **Overview**

This guide shows you how to use the Documenter MCP Server with natural language commands through the cloud deployment at `https://documenter-mcp.onrender.com/`. No local setup required!

## ✅ **Benefits of Cloud Version**

- ✅ **No Installation**: Just add the URL to your IDE
- ✅ **Always Available**: 24/7 service on Render
- ✅ **Cross-Platform**: Works on any device with internet
- ✅ **Professional**: Similar to Context7 and other MCP services
- ✅ **Lightweight**: Fast and reliable (0.54s response time)

## 🚀 **Quick Setup**

### **Step 1: Add to Cursor IDE**

Open your Cursor IDE settings and add this configuration:

```json
{
  "mcpServers": {
    "documenter": {
      "url": "https://documenter-mcp.onrender.com/mcp/request"
    }
  }
}
```

### **Step 2: Restart Cursor IDE**

After adding the configuration, restart Cursor IDE to load the MCP server.

### **Step 3: Test the Connection**

Try a simple command to test the connection:
```
"Detect the project type"
```

## 📝 **Natural Language Commands That Work**

### **Project Detection**
- ✅ `"Detect the project type"`
- ✅ `"What type of project is this?"`
- ✅ `"Analyze this project type"`
- ✅ `"Tell me what kind of project this is"`

### **Project Documentation**
- ✅ `"Document this project"`
- ✅ `"Create comprehensive documentation for this project"`
- ✅ `"Generate project documentation"`
- ✅ `"Analyze the project and create a readme"`
- ✅ `"Document my entire project comprehensively"`

### **Project Analysis**
- ✅ `"Analyze this project structure"`
- ✅ `"Show me the project structure"`
- ✅ `"What's the structure of this project?"`
- ✅ `"Analyze the code metrics and technology distribution"`

### **README Generation**
- ✅ `"Generate README for this project"`
- ✅ `"Create a README for this project"`
- ✅ `"Make a README file for this project"`

## 🎯 **How It Works**

### **Smart Context Detection**

The cloud server uses intelligent defaults and context detection:

1. **MCP Context**: Extracts project context from the MCP request
2. **Request Headers**: Checks for project path in headers
3. **Environment Variables**: Uses IDE environment variables
4. **Smart Fallbacks**: Provides helpful guidance when context is unclear

### **Natural Language Processing**

The server understands various ways to express the same intent:

| **Intent** | **Example Commands** |
|------------|---------------------|
| **Project Detection** | "Detect type", "What type", "Analyze type" |
| **Documentation** | "Document", "Create docs", "Generate docs" |
| **Structure Analysis** | "Analyze structure", "Show structure" |
| **README Generation** | "Generate README", "Create README" |

## 📊 **Example Usage Scenarios**

### **Scenario 1: New Project Analysis**
```
User: "What type of project is this and analyze its structure?"
Result: 
- Detects project type (e.g., Next.js, React, Python)
- Shows confidence score
- Lists project indicators found
- Displays directory structure
```

### **Scenario 2: Complete Documentation**
```
User: "Document this project comprehensively"
Result:
- Project type detection
- Structure analysis
- Package.json analysis (if applicable)
- README generation
- Technology distribution
- Code metrics
```

### **Scenario 3: Quick Analysis**
```
User: "Analyze this project"
Result:
- Quick project overview
- Key files and directories
- Technology stack identification
- Basic metrics
```

## 🔧 **Advanced Usage**

### **With Specific Paths**
If you need to analyze a specific project:

```
"Analyze the project at /path/to/my/nextjs-project"
"Document the project in /Users/me/projects/my-app"
"Generate README for the project at C:\Users\me\projects\my-app"
```

### **Batch Operations**
```
"Analyze multiple projects: /path/to/project1, /path/to/project2"
"Compare these projects: /path/to/react-app, /path/to/vue-app"
```

## 🎯 **Supported Project Types**

The server automatically detects 25+ project types:

| **Frontend** | **Backend** | **Mobile** | **Languages** | **Infrastructure** |
|--------------|-------------|------------|---------------|-------------------|
| React ⚛️ | Node.js 🟢 | Flutter 📱 | Python 🐍 | Docker 🐳 |
| Next.js ▲ | Express 🌐 | | Java ☕ | Terraform 🏗️ |
| Angular 🅰️ | FastAPI ⚡ | | Go 🐹 | |
| Vue.js 🖖 | Django 🎸 | | Rust 🦀 | |
| Svelte ⚡ | Flask 🌶️ | | PHP 🐘 | |

## 📋 **Available Tools**

### **Core Tools**
1. **`detect_project_type`** - Auto-detect project type
2. **`read_file`** - Read project files
3. **`read_filenames_in_directory`** - List directory contents
4. **`write_file`** - Write files to project

### **Analysis Tools**
5. **`analyze_project_structure`** - Complete structure analysis
6. **`analyze_package_json`** - Package.json analysis
7. **`analyze_code_metrics`** - Code statistics and metrics
8. **`scan_for_todos_and_fixmes`** - Find code annotations

### **Documentation Tools**
9. **`generate_project_readme`** - README generation
10. **`document_project_comprehensive`** - Complete documentation
11. **`find_files_by_pattern`** - Pattern-based file search

## 🔧 **Troubleshooting**

### **Issue: "Path does not exist"**
**Solution**: The server needs to know which project to analyze. Try:
- Specify the path: `"Analyze the project at /path/to/your/project"`
- Use relative paths: `"Analyze the current project"`
- Check if the path is correct

### **Issue: "Analyzing server directory"**
**Solution**: The server is analyzing its own directory instead of your project. Try:
- Specify your project path explicitly
- Use clear project context in your command
- Check your IDE's working directory

### **Issue: "Tool not found"**
**Solution**: 
- Restart Cursor IDE after adding the MCP configuration
- Check that the URL is correct: `https://documenter-mcp.onrender.com/mcp/request`
- Verify the server is running (check the health endpoint)

### **Issue: Slow response**
**Solution**:
- The server is hosted on Render's free tier
- First request might be slow due to cold start
- Subsequent requests should be faster

## 📊 **Performance & Reliability**

### **Response Times**
- **First Request**: ~2-5 seconds (cold start)
- **Subsequent Requests**: ~0.5-1 second
- **Large Projects**: ~3-10 seconds (depending on size)

### **Availability**
- **Uptime**: 99.9% (Render free tier)
- **Auto-restart**: Yes (after inactivity)
- **Backup**: Multiple deployment options available

### **Limitations**
- **File Size**: Limited to reasonable project sizes
- **Concurrent Users**: Shared resources on free tier
- **Timeout**: 30-second request timeout

## 🎉 **Success Criteria**

You know it's working when:

- ✅ **Simple commands work**: "Document this project" works
- ✅ **Correct project detection**: Next.js project detected as Next.js
- ✅ **Fast response**: Quick analysis and documentation
- ✅ **No setup required**: Just add the URL to your IDE
- ✅ **Cross-platform**: Works on any device with internet

## 🔮 **Future Enhancements**

We're working on:
- **Better context detection**: Automatic project path detection
- **File upload support**: Upload specific files for analysis
- **Batch processing**: Analyze multiple projects at once
- **Custom templates**: User-defined documentation templates
- **Integration improvements**: Better IDE integration

## 📞 **Need Help?**

If you're having issues:

1. **Check the URL**: Make sure it's `https://documenter-mcp.onrender.com/mcp/request`
2. **Restart IDE**: Restart Cursor IDE after configuration changes
3. **Test connection**: Try the health check endpoint
4. **Check logs**: Look at Cursor IDE logs for error messages
5. **Use specific paths**: Try specifying the project path explicitly

## 🌟 **Pro Tips**

1. **Be specific**: "Document this Next.js project" works better than "Document this"
2. **Use natural language**: "What type of project is this?" works
3. **Combine commands**: "Analyze and document this project" works
4. **Check results**: Always verify the detected project type is correct
5. **Use paths when needed**: Specify paths for complex scenarios

The cloud version provides a seamless, professional experience with natural language commands and no local setup required! 