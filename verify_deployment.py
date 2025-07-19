#!/usr/bin/env python3
"""
Deployment verification script for Documenter MCP Server
Tests all endpoints and functionality after deployment
"""

import requests
import json
import time
import sys

# Configuration
BASE_URL = "https://documenter-mcp.onrender.com"
TIMEOUT = 30

def test_health():
    """Test health endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health OK - {data.get('name', 'Unknown')} v{data.get('version', 'Unknown')}")
            return True
        else:
            print(f"❌ Health failed - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health error: {e}")
        return False

def test_tools():
    """Test tools endpoint"""
    print("🔍 Testing tools endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/tools", timeout=TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            tools_count = data.get('count', 0)
            print(f"✅ Tools OK - Found {tools_count} tools")
            return True
        else:
            print(f"❌ Tools failed - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Tools error: {e}")
        return False

def test_mcp():
    """Test MCP protocol"""
    print("🔍 Testing MCP protocol...")
    try:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list",
            "params": {}
        }
        
        response = requests.post(
            f"{BASE_URL}/mcp/request",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=TIMEOUT
        )
        
        if response.status_code == 200:
            data = response.json()
            if 'result' in data and 'tools' in data['result']:
                tools_count = len(data['result']['tools'])
                print(f"✅ MCP OK - Found {tools_count} tools via MCP")
                return True
            else:
                print("❌ MCP failed - Invalid response format")
                return False
        else:
            print(f"❌ MCP failed - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ MCP error: {e}")
        return False

def test_tool_execution():
    """Test specific tool execution"""
    print("🔍 Testing tool execution...")
    try:
        payload = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "detect_project_type",
                "arguments": {
                    "base_path": "."
                }
            }
        }
        
        response = requests.post(
            f"{BASE_URL}/mcp/request",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=TIMEOUT
        )
        
        if response.status_code == 200:
            data = response.json()
            if 'result' in data and 'content' in data['result']:
                print("✅ Tool execution OK")
                return True
            else:
                print("❌ Tool execution failed - Invalid response")
                return False
        else:
            print(f"❌ Tool execution failed - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Tool execution error: {e}")
        return False

def test_performance():
    """Test response time"""
    print("🔍 Testing performance...")
    start_time = time.time()
    
    try:
        response = requests.get(f"{BASE_URL}/", timeout=TIMEOUT)
        end_time = time.time()
        response_time = end_time - start_time
        
        if response.status_code == 200:
            print(f"✅ Performance OK - {response_time:.2f}s")
            if response_time < 5:
                print("✅ Response time acceptable (< 5s)")
                return True
            else:
                print("⚠️ Response time slow (> 5s)")
                return False
        else:
            print(f"❌ Performance test failed")
            return False
    except Exception as e:
        print(f"❌ Performance error: {e}")
        return False

def main():
    """Run all verification tests"""
    print("🚀 Documenter MCP Server Deployment Verification")
    print("=" * 60)
    print(f"📍 Testing URL: {BASE_URL}")
    print()
    
    tests = [
        ("Health Check", test_health),
        ("Tools Endpoint", test_tools),
        ("MCP Protocol", test_mcp),
        ("Tool Execution", test_tool_execution),
        ("Performance", test_performance)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"🧪 {test_name}")
        print("-" * 40)
        
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} FAILED")
        
        print()
        time.sleep(1)
    
    # Summary
    print("=" * 60)
    print("📊 VERIFICATION SUMMARY")
    print("=" * 60)
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")
    print(f"📈 Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Deployment is successful!")
        print(f"🌐 Your MCP server is ready at: {BASE_URL}")
        print()
        print("📋 Next Steps:")
        print("1. Update your IDE configuration")
        print("2. Test with your projects")
        print("3. Share with the community")
        return 0
    else:
        print("⚠️ Some tests failed. Please check the deployment.")
        print()
        print("🔧 Troubleshooting:")
        print("1. Check Render deployment logs")
        print("2. Verify environment variables")
        print("3. Ensure all files are committed")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 