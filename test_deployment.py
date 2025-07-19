#!/usr/bin/env python3
"""
Test script for Documenter MCP Server deployment
Tests all endpoints and basic functionality
"""

import requests
import json
import time
import sys

# Configuration
BASE_URL = "https://documenter-mcp.onrender.com"
TIMEOUT = 30  # 30 seconds timeout

def test_health_endpoint():
    """Test the health check endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health endpoint OK - {data.get('name', 'Unknown')} v{data.get('version', 'Unknown')}")
            return True
        else:
            print(f"❌ Health endpoint failed - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")
        return False

def test_tools_endpoint():
    """Test the tools listing endpoint"""
    print("🔍 Testing tools endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/tools", timeout=TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            tools_count = data.get('count', 0)
            print(f"✅ Tools endpoint OK - Found {tools_count} tools")
            return True
        else:
            print(f"❌ Tools endpoint failed - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Tools endpoint error: {e}")
        return False

def test_mcp_endpoint():
    """Test the MCP protocol endpoint"""
    print("🔍 Testing MCP endpoint...")
    try:
        # Test tools/list method
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
                print(f"✅ MCP endpoint OK - Found {tools_count} tools via MCP")
                return True
            else:
                print(f"❌ MCP endpoint failed - Invalid response format")
                return False
        else:
            print(f"❌ MCP endpoint failed - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ MCP endpoint error: {e}")
        return False

def test_specific_tool():
    """Test a specific tool (detect_project_type)"""
    print("🔍 Testing specific tool (detect_project_type)...")
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
                print("✅ Tool execution OK - detect_project_type working")
                return True
            else:
                print(f"❌ Tool execution failed - Invalid response format")
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
            print(f"✅ Performance OK - Response time: {response_time:.2f} seconds")
            if response_time < 5:
                print("✅ Response time is acceptable (< 5 seconds)")
                return True
            else:
                print("⚠️ Response time is slow (> 5 seconds)")
                return False
        else:
            print(f"❌ Performance test failed - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Performance test error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Documenter MCP Server Deployment Tests")
    print("=" * 60)
    print(f"📍 Testing URL: {BASE_URL}")
    print(f"⏱️  Timeout: {TIMEOUT} seconds")
    print()
    
    tests = [
        ("Health Endpoint", test_health_endpoint),
        ("Tools Endpoint", test_tools_endpoint),
        ("MCP Endpoint", test_mcp_endpoint),
        ("Tool Execution", test_specific_tool),
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
        time.sleep(1)  # Small delay between tests
    
    # Summary
    print("=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")
    print(f"📈 Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Deployment is successful!")
        print(f"🌐 Your MCP server is ready at: {BASE_URL}")
        return 0
    else:
        print("⚠️ Some tests failed. Please check the deployment.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 