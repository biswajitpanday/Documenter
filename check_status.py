#!/usr/bin/env python3
"""
Simple status checker for Documenter MCP Server
Quick check if the server is running and responding
"""

import requests
import sys

def check_status():
    """Check if the server is running"""
    url = "https://documenter-mcp.onrender.com"
    
    try:
        print(f"🔍 Checking status of {url}...")
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Server is running!")
            print(f"📊 Name: {data.get('name', 'Unknown')}")
            print(f"📊 Version: {data.get('version', 'Unknown')}")
            print(f"📊 Platform: {data.get('platform', 'Unknown')}")
            print(f"📊 Status: {data.get('status', 'Unknown')}")
            return True
        else:
            print(f"❌ Server returned status code: {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Server is not responding (timeout)")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server")
        return False
    except Exception as e:
        print(f"❌ Error checking status: {e}")
        return False

if __name__ == "__main__":
    success = check_status()
    sys.exit(0 if success else 1) 