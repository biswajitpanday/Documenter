# 🔧 Cursor IDE Setup Guide

## 🎯 **Problem Diagnosis**

The MCP server is working perfectly (as confirmed by our tests), but Cursor IDE is having trouble connecting. This is likely due to:

1. **Configuration format** - Cursor expects specific MCP protocol format
2. **Protocol version** - Need to ensure compatibility
3. **Connection timing** - Cursor might need time to establish connection

## ✅ **Working Configuration**

### **Option 1: Standard MCP Configuration**
```json
{
  "mcpServers": {
    "documenter": {
      "url": "https://documenter-mcp.onrender.com/mcp/request"
    }
  }
}
```

### **Option 2: Full MCP Configuration**
```json
{
  "mcpServers": {
    "documenter": {
      "url": "https://documenter-mcp.onrender.com/mcp/request",
      "protocol": "mcp",
      "version": "2024-11-05"
    }
  }
}
```

### **Option 3: Alternative Configuration**
```json
{
  "mcpServers": {
    "documenter": {
      "url": "https://documenter-mcp.onrender.com",
      "endpoint": "/mcp/request"
    }
  }
}
```

## 🔧 **Setup Steps**

### **Step 1: Update Cursor Configuration**
1. Open Cursor IDE
2. Go to **Settings** (Ctrl/Cmd + ,)
3. Search for **"MCP"** or **"Model Context Protocol"**
4. Add the configuration above to your settings

### **Step 2: Restart Cursor IDE**
1. Close Cursor completely
2. Reopen Cursor IDE
3. Wait for the MCP connection to establish

### **Step 3: Verify Connection**
1. Open the **Command Palette** (Ctrl/Cmd + Shift + P)
2. Type **"MCP"** or **"Model Context Protocol"**
3. Look for Documenter tools in the list

## 🧪 **Testing the Connection**

### **Test 1: Health Check**
Visit: https://documenter-mcp.onrender.com/
Expected: JSON response with server info

### **Test 2: Tools Endpoint**
Visit: https://documenter-mcp.onrender.com/tools
Expected: List of 11 available tools

### **Test 3: MCP Protocol**
Run our test script:
```bash
python test_mcp_protocol.py
```

## 🔍 **Troubleshooting**

### **Issue: "Loading tools" with yellow status**
**Solution**: 
1. Try different configuration formats above
2. Restart Cursor IDE completely
3. Check if the server is responding (use test script)

### **Issue: "Connection failed"**
**Solution**:
1. Verify the URL is correct
2. Check if the server is running (visit the health URL)
3. Try the alternative configurations

### **Issue: "No tools found"**
**Solution**:
1. Wait a few minutes for Cursor to establish connection
2. Restart Cursor IDE
3. Check the MCP protocol test results

## 📊 **Expected Results**

After successful setup:
- ✅ **Green status** in Cursor IDE
- ✅ **11 tools available** in the MCP tools list
- ✅ **Tools working** when called from Cursor

## 🎯 **Available Tools**

Once connected, you'll have access to:
1. `detect_project_type` - Auto-detect project type
2. `read_file` - Read file contents
3. `read_filenames_in_directory` - List directory contents
4. `write_file` - Write to files
5. `analyze_project_structure` - Analyze project structure
6. `analyze_package_json` - Analyze package.json
7. `generate_project_readme` - Generate README
8. `find_files_by_pattern` - Find files by pattern
9. `analyze_code_metrics` - Analyze code metrics
10. `scan_for_todos_and_fixmes` - Scan for TODOs
11. `document_project_comprehensive` - Comprehensive documentation

## 🚀 **Usage Example**

Once connected, you can use commands like:
- "Document my project comprehensively"
- "Analyze the project structure"
- "Generate a README for this project"
- "What type of project is this?"

## 📞 **Support**

If you're still having issues:
1. Run `python test_mcp_protocol.py` to verify server status
2. Check the server logs at https://documenter-mcp.onrender.com/
3. Try the alternative configurations above
4. Restart Cursor IDE completely 