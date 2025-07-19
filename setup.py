#!/usr/bin/env python3
"""
Setup script for Documenter MCP Server
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as f:
        return f.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="documenter-mcp",
    version="2.0.0",
    description="Local MCP server for project documentation and analysis",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="Documenter Team",
    author_email="contact@documenter.dev",
    url="https://github.com/biswajitpanday/Documenter",
    packages=find_packages(),
    py_modules=["local_server"],
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "documenter-mcp=local_server:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Documentation",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    keywords="mcp, documentation, project-analysis, ide-integration",
    project_urls={
        "Bug Reports": "https://github.com/biswajitpanday/Documenter/issues",
        "Source": "https://github.com/biswajitpanday/Documenter",
        "Documentation": "https://github.com/biswajitpanday/Documenter#readme",
    },
) 