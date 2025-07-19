#!/usr/bin/env python3
"""
Test MCP Protocol Communication
"""

import requests
import json

def test_mcp_protocol():
    """Test MCP protocol communication with the server"""
    
    base_url = "https://documenter-mcp.onrender.com"
    
    print("🧪 Testing MCP Protocol Communication")
    print("=" * 50)
    
    # Test 1: Health check
    print("\n1. Health Check")
    try:
        response = requests.get(f"{base_url}/")
        print(f"✅ Status: {response.status_code}")
        print(f"📄 Response: {response.json()}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Tools endpoint
    print("\n2. Tools Endpoint")
    try:
        response = requests.get(f"{base_url}/tools")
        print(f"✅ Status: {response.status_code}")
        data = response.json()
        print(f"🔧 Tools found: {data.get('count', 0)}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: MCP Initialize
    print("\n3. MCP Initialize")
    try:
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }
        
        response = requests.post(
            f"{base_url}/mcp/request",
            json=init_request,
            headers={"Content-Type": "application/json"}
        )
        print(f"✅ Status: {response.status_code}")
        data = response.json()
        print(f"📄 Response: {json.dumps(data, indent=2)}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 4: MCP Tools List
    print("\n4. MCP Tools List")
    try:
        tools_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }
        
        response = requests.post(
            f"{base_url}/mcp/request",
            json=tools_request,
            headers={"Content-Type": "application/json"}
        )
        print(f"✅ Status: {response.status_code}")
        data = response.json()
        if "result" in data and "tools" in data["result"]:
            print(f"🔧 Tools found: {len(data['result']['tools'])}")
            for tool in data["result"]["tools"][:3]:  # Show first 3
                print(f"   - {tool['name']}: {tool['description'][:50]}...")
        else:
            print(f"📄 Response: {json.dumps(data, indent=2)}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 5: MCP Tool Call
    print("\n5. MCP Tool Call")
    try:
        tool_request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "detect_project_type",
                "arguments": {
                    "base_path": "."
                }
            }
        }
        
        response = requests.post(
            f"{base_url}/mcp/request",
            json=tool_request,
            headers={"Content-Type": "application/json"}
        )
        print(f"✅ Status: {response.status_code}")
        data = response.json()
        if "result" in data and "content" in data["result"]:
            print(f"📄 Tool result: {data['result']['content'][0]['text'][:100]}...")
        else:
            print(f"📄 Response: {json.dumps(data, indent=2)}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 MCP Protocol Test Complete")

if __name__ == "__main__":
    test_mcp_protocol() 