#!/bin/bash

# Universal Project Documenter MCP Server Launcher (Unix/Linux/macOS)
# This script launches the MCP server for use with Cursor IDE

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Check if UV is installed
if ! command -v uv &> /dev/null; then
    echo "Error: UV is not installed. Please install UV first:"
    echo "curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Check if dependencies are installed
if [ ! -d ".venv" ]; then
    echo "Installing dependencies..."
    uv sync
fi

# Run the MCP server
echo "Starting Universal Project Documenter MCP Server..."
uv run python main.py 