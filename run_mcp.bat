@echo off
REM Windows batch script to run MCP server with proper UV setup
REM This ensures UV is found even if not in Cursor's PATH

REM Add common UV locations to PATH
set "PATH=%PATH%;%USERPROFILE%\.local\bin;%APPDATA%\Python\Scripts"

REM Change to the script directory
cd /d "%~dp0"

REM Run the MCP server with UV
"C:\Users\BiPanday\.local\bin\uv.exe" run python main.py 