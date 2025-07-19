# 🚀 Documenter MCP Server - Installation Guide

## 🎯 **Quick Installation (Recommended)**

### **For Cursor IDE Users**

1. **Open Cursor IDE Settings**
   - Press `Ctrl+,` (Windows/Linux) or `Cmd+,` (Mac)
   - Or go to `File > Preferences > Settings`

2. **Add MCP Server Configuration**
   ```json
   {
     "mcpServers": {
       "documenter": {
         "url": "https://documenter-mcp.onrender.com/mcp/request"
       }
     }
   }
   ```

3. **Restart Cursor IDE**
   - Close and reopen Cursor IDE
   - The MCP server will be loaded automatically

4. **Test the Installation**
   - Open any project
   - Try: `"Detect the project type"`
   - You should see the project type detected

## ✅ **That's It!**

No downloads, no installations, no dependencies. Just add the URL and you're ready to go!

## 📝 **Natural Language Commands That Work**

Once installed, you can use these commands:

### **Project Detection**
- `"Detect the project type"`
- `"What type of project is this?"`
- `"Analyze this project type"`

### **Project Documentation**
- `"Document this project"`
- `"Create comprehensive documentation for this project"`
- `"Generate project documentation"`

### **Project Analysis**
- `"Analyze this project structure"`
- `"Show me the project structure"`
- `"Analyze the code metrics"`

### **README Generation**
- `"Generate README for this project"`
- `"Create a README for this project"`

## 🔧 **Troubleshooting**

### **Issue: "Tool not found"**
**Solution**: 
- Restart Cursor IDE after adding the configuration
- Check that the URL is correct: `https://documenter-mcp.onrender.com/mcp/request`

### **Issue: "Path does not exist"**
**Solution**: 
- Specify the project path: `"Analyze the project at /path/to/your/project"`
- Or use relative paths: `"Analyze the current project"`

### **Issue: "Analyzing server directory"**
**Solution**: 
- Specify your project path explicitly
- Use clear project context in your command

## 🌟 **Pro Tips**

1. **Be specific**: "Document this Next.js project" works better than "Document this"
2. **Use natural language**: "What type of project is this?" works
3. **Combine commands**: "Analyze and document this project" works
4. **Check results**: Always verify the detected project type is correct

## 📊 **What You Get**

- ✅ **25+ Project Types**: React, Next.js, Angular, Vue, Python, Java, Go, Rust, and more
- ✅ **Smart Detection**: Automatic project type detection with confidence scoring
- ✅ **Comprehensive Analysis**: Project structure, dependencies, code metrics
- ✅ **Documentation Generation**: README, component docs, and comprehensive reports
- ✅ **Natural Language**: Simple commands work without technical knowledge

## 🎉 **Success Criteria**

You know it's working when:
- ✅ **Simple commands work**: "Document this project" works
- ✅ **Correct project detection**: Next.js project detected as Next.js
- ✅ **Fast response**: Quick analysis and documentation
- ✅ **No setup required**: Just add the URL to your IDE

## 📞 **Need Help?**

If you're having issues:
1. Check the URL is correct
2. Restart Cursor IDE
3. Try specifying the project path explicitly
4. Check Cursor IDE logs for error messages

---

**That's it! You're ready to document any project with natural language commands.** 