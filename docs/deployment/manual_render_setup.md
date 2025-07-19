# 🔧 Manual Render Setup (Backup Configuration)

## 📋 **Step-by-Step Manual Configuration**

### **Step 1: Remove render.yaml (if causing issues)**
```bash
git rm render.yaml
git commit -m "Remove render.yaml for manual configuration"
git push origin master
```

### **Step 2: Create Web Service Manually**
1. Go to [render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Select the `Documenter` repository

### **Step 3: Manual Configuration**
- **Name**: `documenter-mcp`
- **Environment**: `Python 3`
- **Region**: Choose closest to you
- **Branch**: `master`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python server.py`
- **Plan**: `Free`

### **Step 4: Environment Variables (CRITICAL)**
Add these manually in the Environment tab:

| Key | Value | Description |
|-----|-------|-------------|
| `PORT` | `8080` | Server port |
| `PYTHON_VERSION` | `3.11.9` | Python version (or try 3.10.12) |

### **Step 5: Alternative Python Versions**
If `3.11.9` doesn't work, try these in order:
1. `3.11.8`
2. `3.11.7`
3. `3.10.12`
4. `3.10.11`
5. `3.9.18`

### **Step 6: Deploy**
1. Click "Create Web Service"
2. Monitor the build logs
3. Wait for deployment to complete

## 🧪 **Testing After Deployment**

```bash
python verify_deployment.py
```

## 🔧 **Troubleshooting**

### **If Python Version Still Fails**
1. Try different Python versions from the list above
2. Check Render's supported Python versions: https://render.com/docs/python-version
3. Use the latest stable version available

### **If Build Fails**
1. Check the build logs for specific errors
2. Ensure `requirements.txt` is correct
3. Verify `server.py` starts correctly locally

### **If Service Won't Start**
1. Check the start command: `python server.py`
2. Verify the PORT environment variable is set
3. Check if the service is binding to the correct port

## 📊 **Expected Results**

After successful deployment:
- **URL**: `https://documenter-mcp.onrender.com`
- **Health Check**: Returns 200 OK
- **All Tools**: 16 tools available
- **Performance**: < 5 second response time 