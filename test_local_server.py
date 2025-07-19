#!/usr/bin/env python3
"""
Test Local MCP Server
"""

import subprocess
import json
import sys
from pathlib import Path

def test_local_mcp_server():
    """Test the local MCP server with various commands"""
    
    print("🧪 Testing Local MCP Server")
    print("=" * 50)
    
    # Test 1: Initialize
    print("\n1. Testing MCP Initialize")
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
        
        result = send_mcp_request(init_request)
        if result:
            print("✅ Initialize successful")
            print(f"📄 Server info: {result.get('result', {}).get('serverInfo', {})}")
        else:
            print("❌ Initialize failed")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Tools List
    print("\n2. Testing Tools List")
    try:
        tools_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }
        
        result = send_mcp_request(tools_request)
        if result and "result" in result and "tools" in result["result"]:
            tools = result["result"]["tools"]
            print(f"✅ Found {len(tools)} tools:")
            for tool in tools:
                print(f"   - {tool['name']}: {tool['description'][:50]}...")
        else:
            print("❌ Tools list failed")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: Project Type Detection
    print("\n3. Testing Project Type Detection")
    try:
        detect_request = {
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
        
        result = send_mcp_request(detect_request)
        if result and "result" in result and "content" in result["result"]:
            content = result["result"]["content"][0]["text"]
            print("✅ Project type detection successful")
            print(f"📄 Result: {content[:200]}...")
        else:
            print("❌ Project type detection failed")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 4: Directory Listing
    print("\n4. Testing Directory Listing")
    try:
        dir_request = {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {
                "name": "read_filenames_in_directory",
                "arguments": {
                    "directory": "."
                }
            }
        }
        
        result = send_mcp_request(dir_request)
        if result and "result" in result and "content" in result["result"]:
            content = result["result"]["content"][0]["text"]
            print("✅ Directory listing successful")
            print(f"📄 Result: {content[:200]}...")
        else:
            print("❌ Directory listing failed")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 5: Comprehensive Documentation
    print("\n5. Testing Comprehensive Documentation")
    try:
        doc_request = {
            "jsonrpc": "2.0",
            "id": 5,
            "method": "tools/call",
            "params": {
                "name": "document_project_comprehensive",
                "arguments": {
                    "project_path": "."
                }
            }
        }
        
        result = send_mcp_request(doc_request)
        if result and "result" in result and "content" in result["result"]:
            content = result["result"]["content"][0]["text"]
            print("✅ Comprehensive documentation successful")
            print(f"📄 Result: {content[:200]}...")
        else:
            print("❌ Comprehensive documentation failed")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Local MCP Server Test Complete")

def send_mcp_request(request):
    """Send a request to the local MCP server"""
    try:
        # Start the local server process
        process = subprocess.Popen(
            [sys.executable, "local_server.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Send the request
        request_json = json.dumps(request) + "\n"
        stdout, stderr = process.communicate(input=request_json, timeout=30)
        
        if stderr:
            print(f"⚠️  Server stderr: {stderr}")
        
        if stdout:
            try:
                return json.loads(stdout.strip())
            except json.JSONDecodeError:
                print(f"⚠️  Invalid JSON response: {stdout}")
                return None
        else:
            print("⚠️  No response from server")
            return None
            
    except subprocess.TimeoutExpired:
        print("⚠️  Request timed out")
        process.kill()
        return None
    except Exception as e:
        print(f"⚠️  Error communicating with server: {e}")
        return None

if __name__ == "__main__":
    test_local_mcp_server() 