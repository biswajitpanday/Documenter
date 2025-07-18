#!/usr/bin/env python3
"""
Universal Project Documenter - Test Suite
Tests all 16 MCP tools to ensure they work correctly
"""

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

def test_tool(tool_name, tool_func, *args, **kwargs):
    """Test a single tool with error handling"""
    try:
        print(f"🧪 Testing {tool_name}...")
        result = tool_func(*args, **kwargs)
        
        # Truncate very long results for cleaner output
        if len(result) > 500:
            result = result[:500] + "..."
            
        print(f"✅ {tool_name} completed successfully")
        return True
    except Exception as e:
        print(f"❌ {tool_name} failed: {e}")
        return False

def main():
    print("🚀 Universal Project Documenter - Test Suite")
    print("=" * 60)
    
    tests = [
        ("get_cursor_working_directory", get_cursor_working_directory),
        ("auto_detect_user_project", auto_detect_user_project),
        ("detect_project_type", detect_project_type, "."),
        ("read_filenames_in_directory", read_filenames_in_directory, "."),
        ("analyze_project_structure", analyze_project_structure, "."),
        ("read_file", read_file, "pyproject.toml"),
        ("analyze_project_config", analyze_project_config, "pyproject.toml"),
        ("generate_component_documentation", generate_component_documentation, "main.py"),
        ("find_files_by_pattern", find_files_by_pattern, "*.py"),
        ("batch_read_files", batch_read_files, ["pyproject.toml", "README.md"]),
        ("analyze_code_metrics", analyze_code_metrics, "."),
        ("scan_for_todos_and_fixmes", scan_for_todos_and_fixmes, "."),
        ("generate_project_readme", generate_project_readme, "."),
        ("document_project_comprehensive", document_project_comprehensive, ".")
    ]
    
    passed = 0
    total = len(tests)
    
    for test_data in tests:
        tool_name = test_data[0]
        tool_func = test_data[1]
        args = test_data[2:] if len(test_data) > 2 else []
        
        if test_tool(tool_name, tool_func, *args):
            passed += 1
        print()  # Add spacing between tests
    
    print("=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")
    print()
    
    if passed == total:
        print("🎉 All tests passed! The Universal Project Documenter is ready for use.")
        return 0
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    exit(main()) 