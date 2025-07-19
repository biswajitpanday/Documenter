# 🔧 Project Context Detection Solution

## 🎯 **Problem Analysis**

The issue is that when Cursor IDE calls the MCP server, the server is running on Render (`/opt/render/project/src`) and doesn't have access to the user's local project directory. The server needs to know which project the user wants to analyze.

## 🔍 **Root Cause**

1. **Server Location**: MCP server runs on Render cloud platform
2. **User Context**: User's project is on their local machine
3. **Missing Bridge**: No mechanism to pass user's project path to server
4. **Default Behavior**: Server uses its own directory (`/opt/render/project/src`)

## 💡 **Solution Approaches**

### **Approach 1: User-Specified Project Path (Recommended)**

**How it works:**
- User provides their project path in the MCP request
- Server validates and uses the provided path
- Fallback to intelligent detection if path not provided

**Implementation:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "detect_project_type",
    "arguments": {
      "base_path": "/path/to/user/project",
      "project_context": {
        "user_project_path": "/path/to/user/project",
        "project_name": "my-nextjs-app"
      }
    }
  }
}
```

### **Approach 2: Environment Variable Detection**

**How it works:**
- Cursor IDE sets environment variables with user's project path
- Server reads these variables to determine context
- Requires Cursor IDE to set `CURSOR_PROJECT_PATH` or similar

**Implementation:**
```bash
# Cursor IDE would set this
export CURSOR_PROJECT_PATH="/path/to/user/project"
```

### **Approach 3: Request Header Detection**

**How it works:**
- Cursor IDE sends project path in HTTP headers
- Server reads headers to determine user's project
- Most reliable but requires IDE support

**Implementation:**
```http
POST /mcp/request
X-Project-Path: /path/to/user/project
X-Workspace-Path: /path/to/user/project
Content-Type: application/json
```

### **Approach 4: File Upload/Content Analysis**

**How it works:**
- User uploads key project files (package.json, etc.)
- Server analyzes uploaded content
- Works without direct file system access

## 🚀 **Recommended Implementation**

### **Phase 1: Enhanced Argument Handling**

1. **Update tool descriptions** to clearly indicate they need project path
2. **Add validation** for project paths
3. **Implement fallback detection** for common scenarios

### **Phase 2: Cursor IDE Integration**

1. **Create Cursor IDE plugin** that automatically provides project context
2. **Add project path detection** in Cursor IDE
3. **Implement automatic context injection**

### **Phase 3: Smart Detection**

1. **Implement project boundary detection**
2. **Add project type hints** from user
3. **Create project context validation**

## 📋 **Immediate Fix**

### **For Users (Workaround):**

**Option 1: Specify Project Path**
```json
{
  "mcpServers": {
    "documenter": {
      "url": "https://documenter-mcp.onrender.com/mcp/request"
    }
  }
}
```

Then use commands like:
- "Analyze the project at /path/to/my/project"
- "Document the project in /Users/me/projects/my-app"

**Option 2: Use Relative Paths**
- "Analyze the current project directory"
- "Document this project"

### **For Developers (Server Fix):**

1. **Update tool descriptions** to be clearer about path requirements
2. **Add better error messages** when wrong path is used
3. **Implement project path validation**
4. **Add examples** in tool descriptions

## 🧪 **Testing Strategy**

### **Test Cases:**

1. **Next.js Project**: Should detect Next.js, not Python
2. **React Project**: Should detect React, not generic
3. **Python Project**: Should detect Python correctly
4. **Invalid Path**: Should provide clear error message
5. **No Path**: Should use intelligent fallback

### **Test Commands:**

```bash
# Test with specific project path
curl -X POST https://documenter-mcp.onrender.com/mcp/request \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "detect_project_type",
      "arguments": {
        "base_path": "/path/to/nextjs/project"
      }
    }
  }'
```

## 🎯 **Success Criteria**

- ✅ **Correct Project Detection**: Next.js project detected as Next.js, not Python
- ✅ **Proper Path Usage**: Uses user's project path, not server path
- ✅ **Clear Error Messages**: Helpful feedback when path is wrong
- ✅ **Intuitive Usage**: Easy for users to specify their project
- ✅ **Fallback Behavior**: Graceful handling when path not provided

## 📊 **Implementation Priority**

1. **High Priority**: Fix tool descriptions and error messages
2. **Medium Priority**: Implement project path validation
3. **Low Priority**: Add smart detection features
4. **Future**: Cursor IDE integration for automatic context 