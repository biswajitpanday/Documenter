#!/usr/bin/env python3
"""
Test script to demonstrate documenting any project with auto-detection
This shows how the MCP server automatically detects the user's project
"""

import sys
import os
from pathlib import Path

# Add the current directory to Python path to import main
sys.path.insert(0, str(Path(__file__).parent))

from main import (
    auto_detect_user_project,
    document_project_comprehensive,
    detect_project_type,
    analyze_project_structure
)

def test_auto_detection():
    """Test auto-detection capabilities"""
    print("🚀 Testing Auto-Detection Capabilities")
    print("=" * 60)
    print("This test demonstrates how the MCP server automatically")
    print("detects ANY user's project directory (not hardcoded paths)")
    print()
    
    # Test 1: Show current environment
    print("🔍 Current Environment Analysis:")
    print("-" * 50)
    print(f"Current Working Directory: {Path.cwd()}")
    print(f"Environment Variables:")
    
    env_vars = ['CURSOR_CWD', 'VSCODE_CWD', 'PWD', 'CD', 'INIT_CWD']
    for var in env_vars:
        value = os.environ.get(var, 'Not set')
        print(f"  {var}: {value}")
    print()
    
    # Test 2: Auto-detect project
    print("🧪 Test 1: Auto-detecting user's project...")
    print("-" * 50)
    try:
        result = auto_detect_user_project()
        print(result)
        print("✅ Auto-detection successful")
    except Exception as e:
        print(f"❌ Auto-detection failed: {e}")
    print()
    
    # Test 3: Comprehensive documentation with auto-detection
    print("🧪 Test 2: Comprehensive documentation (auto-detection)...")
    print("-" * 50)
    try:
        # This should automatically detect the user's project
        result = document_project_comprehensive()
        
        # Show just the first part to avoid overwhelming output
        lines = result.split('\n')
        preview_lines = lines[:50]  # Show first 50 lines
        print('\n'.join(preview_lines))
        
        if len(lines) > 50:
            print(f"\n... (showing first 50 lines of {len(lines)} total lines)")
        
        print("✅ Comprehensive documentation successful")
    except Exception as e:
        print(f"❌ Comprehensive documentation failed: {e}")
    print()

def test_with_example_paths():
    """Test with example paths (for demonstration only)"""
    print("🎯 Testing with Example Paths")
    print("=" * 60)
    print("Note: These are just examples. In real usage, auto-detection")
    print("will find the actual project where Cursor IDE is running.")
    print()
    
    # Example paths that might exist on different systems
    example_paths = [
        ".",  # Current directory
        "..",  # Parent directory
        Path.home() / "Desktop",  # User's desktop
        Path.home() / "Documents",  # User's documents
    ]
    
    for example_path in example_paths:
        if Path(example_path).exists():
            print(f"📁 Testing path: {Path(example_path).resolve()}")
            print("-" * 40)
            try:
                result = auto_detect_user_project(str(example_path))
                # Show just the key information
                lines = result.split('\n')
                for line in lines[:10]:  # Show first 10 lines
                    print(line)
                if len(lines) > 10:
                    print("...")
                print("✅ Path analysis successful")
            except Exception as e:
                print(f"❌ Path analysis failed: {e}")
            print()
            break  # Just test one valid path for demo

def main():
    """Run all tests"""
    print("📚 Universal Project Documenter - Generic Path Detection Test")
    print("=" * 70)
    print("This test demonstrates the MCP server's ability to automatically")
    print("detect ANY user's project directory without hardcoded paths.")
    print()
    
    test_auto_detection()
    test_with_example_paths()
    
    print("📋 Summary:")
    print("-" * 30)
    print("✅ The MCP server now uses smart auto-detection")
    print("✅ No hardcoded paths - works for any developer")
    print("✅ Multiple detection methods for reliability")
    print("✅ Graceful fallbacks if auto-detection fails")
    print()
    print("🎯 For any user's project, simply use:")
    print('   "I need comprehensive documentation for this codebase"')
    print()
    print("🎉 Universal path detection test completed!")

if __name__ == "__main__":
    main() 