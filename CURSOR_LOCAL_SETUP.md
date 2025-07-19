# 🔧 Local MCP Server Setup for Cursor IDE

## 🎯 **Overview**

This guide shows you how to set up the Documenter MCP Server to run locally on your machine, giving you direct access to your project files without needing to specify paths.

## ✅ **Benefits of Local Setup**

- ✅ **Simple Commands**: "Document this project" works naturally
- ✅ **No Path Specification**: Automatic project detection
- ✅ **Privacy**: Files stay on your machine
- ✅ **Performance**: Fast file access
- ✅ **Offline**: Works without internet

## 🚀 **Installation Steps**

### **Step 1: Download the Local Server**

1. **Clone or download** the Documenter repository
2. **Navigate** to the project directory
3. **Verify** you have `local_server.py` file

### **Step 2: Install Dependencies**

```bash
# Install the MCP FastMCP library
pip install mcp

# Or if you have a requirements.txt
pip install -r requirements.txt
```

### **Step 3: Update Cursor IDE Configuration**

Open your Cursor IDE settings and update the MCP configuration:

**Replace this (cloud version):**
```json
{
  "mcpServers": {
    "documenter": {
      "url": "https://documenter-mcp.onrender.com/mcp/request"
    }
  }
}
```

**With this (local version):**
```json
{
  "mcpServers": {
    "documenter": {
      "command": "python",
      "args": ["/full/path/to/local_server.py"],
      "env": {}
    }
  }
}
```

**Important**: Replace `/full/path/to/local_server.py` with the actual path to your `local_server.py` file.

### **Step 4: Find Your local_server.py Path**

**On Windows:**
```bash
# In Command Prompt or PowerShell
cd C:\path\to\Documenter
echo %cd%\local_server.py
```

**On Mac/Linux:**
```bash
# In Terminal
cd /path/to/Documenter
pwd
echo "$(pwd)/local_server.py"
```

### **Step 5: Test the Setup**

1. **Restart Cursor IDE**
2. **Open a project** you want to document
3. **Try a simple command**: "Detect the project type"
4. **Expected result**: Should detect your project type correctly

## 🧪 **Testing Your Setup**

### **Test 1: Project Type Detection**
```
"Detect the project type"
```
**Expected**: Should show your project type (Next.js, React, Python, etc.)

### **Test 2: Project Documentation**
```
"Create comprehensive documentation for this project"
```
**Expected**: Should analyze your project and generate documentation

### **Test 3: Project Analysis**
```
"Analyze this project structure"
```
**Expected**: Should show your project's directory structure

## 🔧 **Troubleshooting**

### **Issue: "Command not found"**
**Solution**: Make sure the path to `local_server.py` is correct and absolute.

### **Issue: "Module not found"**
**Solution**: Install the required dependencies:
```bash
pip install mcp
```

### **Issue: "Permission denied"**
**Solution**: Make sure the `local_server.py` file is executable:
```bash
chmod +x local_server.py
```

### **Issue: Still not working**
**Solution**: Check the Cursor IDE logs for error messages.

## 📝 **Example Commands That Work**

With the local setup, these commands work naturally:

- ✅ `"Detect the project type"`
- ✅ `"Create comprehensive documentation for this project"`
- ✅ `"Analyze this project structure"`
- ✅ `"Generate README for this project"`
- ✅ `"Document this project"`
- ✅ `"Analyze the project and create a readme"`

## 🎯 **Configuration Examples**

### **Windows Example:**
```json
{
  "mcpServers": {
    "documenter": {
      "command": "python",
      "args": ["C:\\Users\\YourName\\Documents\\Documenter\\local_server.py"],
      "env": {}
    }
  }
}
```

### **Mac/Linux Example:**
```json
{
  "mcpServers": {
    "documenter": {
      "command": "python",
      "args": ["/Users/YourName/Documents/Documenter/local_server.py"],
      "env": {}
    }
  }
}
```

## 🔮 **Advanced Configuration**

### **Using Virtual Environment:**
```json
{
  "mcpServers": {
    "documenter": {
      "command": "/path/to/venv/bin/python",
      "args": ["/path/to/local_server.py"],
      "env": {}
    }
  }
}
```

### **Using Python Module:**
```json
{
  "mcpServers": {
    "documenter": {
      "command": "python",
      "args": ["-m", "documenter.local_server"],
      "env": {}
    }
  }
}
```

## 📊 **Performance Comparison**

| Feature | Cloud Version | Local Version |
|---------|---------------|---------------|
| **Setup Complexity** | Simple | Medium |
| **File Access** | Limited | Full |
| **Privacy** | Files sent to cloud | Files stay local |
| **Performance** | Network dependent | Fast |
| **Offline Support** | No | Yes |
| **Path Specification** | Required | Not needed |

## 🎉 **Success Criteria**

You know it's working when:

- ✅ **Simple commands work**: "Document this project" works
- ✅ **Correct project detection**: Next.js project detected as Next.js
- ✅ **No path specification needed**: Works with current directory
- ✅ **Fast response**: Quick analysis and documentation
- ✅ **Privacy maintained**: Files stay on your machine

## 📞 **Need Help?**

If you're having issues:

1. **Check the path**: Make sure the path to `local_server.py` is correct
2. **Install dependencies**: Make sure `mcp` is installed
3. **Restart Cursor**: Restart Cursor IDE after configuration changes
4. **Check logs**: Look at Cursor IDE logs for error messages
5. **Test manually**: Try running `python local_server.py` directly

## 🔄 **Migration from Cloud Version**

If you're currently using the cloud version:

1. **Backup your current configuration**
2. **Follow the installation steps above**
3. **Update your Cursor configuration**
4. **Test with simple commands**
5. **Remove the old cloud configuration**

The local version provides a much better user experience with natural language commands and direct file access! 