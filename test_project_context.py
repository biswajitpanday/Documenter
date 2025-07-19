#!/usr/bin/env python3
"""
Test Project Context Detection
"""

import os
import json
import requests
from pathlib import Path

def test_project_context_detection():
    """Test different methods of detecting user's project directory"""
    
    print("🧪 Testing Project Context Detection")
    print("=" * 50)
    
    # Test 1: Environment Variables
    print("\n1. Environment Variables")
    env_vars = [
        'CURSOR_CWD', 'VSCODE_CWD', 'WINDSURF_CWD', 'CLAUDE_CWD',
        'PWD', 'CD', 'INIT_CWD', 'PROJECT_ROOT', 'WORKSPACE_FOLDER',
        'npm_config_prefix', 'CARGO_MANIFEST_DIR'
    ]
    
    for env_var in env_vars:
        value = os.environ.get(env_var, '')
        if value:
            print(f"✅ {env_var}: {value}")
        else:
            print(f"❌ {env_var}: Not set")
    
    # Test 2: Current Working Directory
    print("\n2. Current Working Directory")
    cwd = Path.cwd().resolve()
    print(f"📁 CWD: {cwd}")
    print(f"🔍 Is Documenter project: {'documenter' in str(cwd).lower()}")
    print(f"🔍 Is Render server: {'render' in str(cwd).lower()}")
    
    # Test 3: Process Tree Analysis
    print("\n3. Process Tree Analysis")
    try:
        import psutil
        current_process = psutil.Process()
        print(f"📊 Current process: {current_process.name()} (PID: {current_process.pid})")
        print(f"📁 Process CWD: {current_process.cwd()}")
        
        # Check parent processes
        parent = current_process.parent()
        if parent:
            print(f"👤 Parent process: {parent.name()} (PID: {parent.pid})")
            print(f"📁 Parent CWD: {parent.cwd()}")
    except ImportError:
        print("❌ psutil not available")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 4: Git Repository Detection
    print("\n4. Git Repository Detection")
    current_dir = Path.cwd().resolve()
    for parent in [current_dir] + list(current_dir.parents)[:5]:
        if (parent / '.git').exists():
            print(f"✅ Git repository found: {parent}")
            break
    else:
        print("❌ No git repository found in current path or parents")
    
    # Test 5: Project Indicators
    print("\n5. Project Indicators")
    current_dir = Path.cwd().resolve()
    project_indicators = [
        'package.json', 'pyproject.toml', 'requirements.txt', 'pom.xml',
        'Cargo.toml', 'go.mod', 'composer.json', '.csproj', '.sln'
    ]
    
    found_indicators = []
    for indicator in project_indicators:
        if (current_dir / indicator).exists():
            found_indicators.append(indicator)
    
    if found_indicators:
        print(f"✅ Project indicators found: {', '.join(found_indicators)}")
    else:
        print("❌ No project indicators found")
    
    # Test 6: MCP Server Test
    print("\n6. MCP Server Test with Context")
    try:
        # Test with a Next.js project context
        test_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "detect_project_type",
                "arguments": {
                    "base_path": "/tmp/test-nextjs-project"  # Simulate user project
                }
            }
        }
        
        response = requests.post(
            "https://documenter-mcp.onrender.com/mcp/request",
            json=test_request,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"✅ MCP Response Status: {response.status_code}")
        data = response.json()
        if "result" in data and "content" in data["result"]:
            result_text = data["result"]["content"][0]["text"]
            print(f"📄 Result: {result_text[:200]}...")
        else:
            print(f"📄 Full Response: {json.dumps(data, indent=2)}")
            
    except Exception as e:
        print(f"❌ MCP Test Error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Project Context Test Complete")

if __name__ == "__main__":
    test_project_context_detection() 