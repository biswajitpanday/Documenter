# 📖 Documenter MCP Server Usage Guide

## 🎯 **Quick Start**

Your Documenter MCP Server is now connected and working! However, to get the best results, you need to specify which project you want to analyze.

## ⚠️ **Important: Specify Your Project Path**

The MCP server runs on the cloud and doesn't automatically know which project you want to analyze. You need to tell it explicitly.

## 🚀 **How to Use**

### **Method 1: Specify Project Path in Your Request**

Instead of:
```
"create me a comprehensive documentation for this project"
```

Use:
```
"create me a comprehensive documentation for the project at /path/to/my/nextjs-project"
```

### **Method 2: Use Descriptive Commands**

- `"Analyze the project at /Users/me/projects/my-react-app"`
- `"Document the project in C:\Users\me\projects\my-nextjs-app"`
- `"Generate README for the project at /home/user/my-vue-project"`

### **Method 3: Use Relative Paths (if supported)**

- `"Analyze the current project directory"`
- `"Document this project"`

## 📁 **Finding Your Project Path**

### **On Windows:**
1. Open File Explorer
2. Navigate to your project folder
3. Click in the address bar
4. Copy the full path (e.g., `C:\Users\YourName\projects\my-app`)

### **On Mac/Linux:**
1. Open Terminal
2. Navigate to your project: `cd /path/to/your/project`
3. Run: `pwd` to get the full path

## 🧪 **Test Your Setup**

Try this command in Cursor IDE:

```
"Detect the project type for the project at /path/to/your/actual/project"
```

**Expected Result:**
- Should detect your project type correctly (Next.js, React, etc.)
- Should NOT show "PYTHON" for a Next.js project
- Should show the correct path you specified

## 🔧 **Troubleshooting**

### **Issue: Still shows wrong project type**
**Solution:** Make sure you're specifying the correct path to your project directory (the folder containing package.json, etc.)

### **Issue: "Path does not exist" error**
**Solution:** 
1. Verify the path is correct
2. Make sure the project directory exists
3. Use forward slashes (/) even on Windows

### **Issue: Still analyzing server directory**
**Solution:** You need to explicitly specify your project path in the command

## 📝 **Example Commands**

### **For Next.js Projects:**
```
"Analyze the Next.js project at /Users/me/projects/my-nextjs-app"
"Generate documentation for the project at C:\Users\me\projects\my-app"
"Detect project type for /home/user/my-nextjs-project"
```

### **For React Projects:**
```
"Analyze the React project at /Users/me/projects/my-react-app"
"Document the project at C:\Users\me\projects\react-app"
```

### **For Python Projects:**
```
"Analyze the Python project at /Users/me/projects/my-python-app"
"Generate README for the project at C:\Users\me\projects\python-app"
```

## 🎯 **Available Tools**

Once you specify the correct project path, you can use:

1. **`detect_project_type`** - Auto-detect project type
2. **`read_file`** - Read project files
3. **`analyze_project_structure`** - Analyze project structure
4. **`analyze_package_json`** - Analyze package.json
5. **`generate_project_readme`** - Generate README
6. **`document_project_comprehensive`** - Complete documentation
7. **`find_files_by_pattern`** - Find files by pattern
8. **`analyze_code_metrics`** - Analyze code metrics
9. **`scan_for_todos_and_fixmes`** - Scan for TODOs

## 💡 **Pro Tips**

1. **Always specify the full path** to your project directory
2. **Use forward slashes** (/) even on Windows
3. **Make sure the path exists** and contains your project files
4. **Test with a simple command first** before running comprehensive analysis

## 🔮 **Future Improvements**

We're working on:
- Automatic project path detection
- Cursor IDE integration for seamless usage
- Smart project context awareness
- Better error messages and guidance

## 📞 **Need Help?**

If you're still having issues:
1. Check that your project path is correct
2. Make sure the project directory exists
3. Try the test commands above
4. Check the error messages for guidance 