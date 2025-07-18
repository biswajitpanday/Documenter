#!/usr/bin/env python3
"""
Test script for Universal Project Documenter MCP Server
This script tests all the functionality to ensure everything works correctly.
"""

import sys
import json
from pathlib import Path

# Add the current directory to Python path to import main
sys.path.insert(0, str(Path(__file__).parent))

from main import (
    detect_project_type,
    read_file,
    read_filenames_in_directory,
    analyze_project_structure,
    analyze_package_json,
    analyze_project_config,
    generate_component_documentation,
    generate_project_readme,
    batch_read_files,
    find_files_by_pattern,
    analyze_code_metrics,
    scan_for_todos_and_fixmes,
    get_cursor_working_directory,
    auto_detect_user_project,
    document_project_comprehensive
)

def test_function(func_name, func, *args, **kwargs):
    """Test a function and display results"""
    print(f"\n🧪 Testing {func_name}...")
    print("=" * 50)
    
    try:
        result = func(*args, **kwargs)
        print(result)
        print(f"✅ {func_name} completed successfully")
        return True
    except Exception as e:
        print(f"❌ {func_name} failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Universal Project Documenter - Test Suite")
    print("=" * 60)
    
    test_results = []
    
    # Test 1: Get current working directory
    test_results.append(test_function(
        "get_cursor_working_directory", 
        get_cursor_working_directory
    ))
    
    # Test 2: Auto-detect user project
    test_results.append(test_function(
        "auto_detect_user_project", 
        auto_detect_user_project
    ))
    
    # Test 3: Detect project type
    test_results.append(test_function(
        "detect_project_type", 
        detect_project_type
    ))
    
    # Test 4: Read filenames in directory
    test_results.append(test_function(
        "read_filenames_in_directory", 
        read_filenames_in_directory
    ))
    
    # Test 5: Analyze project structure
    test_results.append(test_function(
        "analyze_project_structure", 
        analyze_project_structure
    ))
    
    # Test 6: Read specific files
    test_results.append(test_function(
        "read_file (pyproject.toml)", 
        read_file,
        "pyproject.toml"
    ))
    
    # Test 7: Analyze package.json (if exists)
    if Path("package.json").exists():
        test_results.append(test_function(
            "analyze_package_json", 
            analyze_package_json
        ))
    
    # Test 8: Analyze project config
    test_results.append(test_function(
        "analyze_project_config (pyproject.toml)", 
        analyze_project_config,
        "pyproject.toml"
    ))
    
    # Test 9: Generate component documentation
    test_results.append(test_function(
        "generate_component_documentation (main.py)", 
        generate_component_documentation,
        "main.py"
    ))
    
    # Test 10: Find files by pattern
    test_results.append(test_function(
        "find_files_by_pattern (*.py)", 
        find_files_by_pattern,
        "*.py"
    ))
    
    # Test 11: Batch read files
    test_results.append(test_function(
        "batch_read_files", 
        batch_read_files,
        ["pyproject.toml", "README.md"]
    ))
    
    # Test 12: Analyze code metrics
    test_results.append(test_function(
        "analyze_code_metrics", 
        analyze_code_metrics
    ))
    
    # Test 13: Scan for TODOs and FIXMEs
    test_results.append(test_function(
        "scan_for_todos_and_fixmes", 
        scan_for_todos_and_fixmes
    ))
    
    # Test 14: Generate project README
    test_results.append(test_function(
        "generate_project_readme", 
        generate_project_readme
    ))
    
    # Test 15: Comprehensive documentation workflow
    test_results.append(test_function(
        "document_project_comprehensive", 
        document_project_comprehensive
    ))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(test_results)
    total = len(test_results)
    
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")
    
    if passed == total:
        print("\n🎉 All tests passed! The Universal Project Documenter is ready for use.")
        return True
    else:
        print(f"\n⚠️  {total - passed} tests failed. Please check the output above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 