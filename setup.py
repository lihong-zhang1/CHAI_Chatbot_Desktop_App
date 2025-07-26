#!/usr/bin/env python3
"""
Setup script for CHAI Friend - AI Chat Companion

This script provides installation and packaging configuration
for the CHAI Friend desktop application.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read requirements from requirements.txt
requirements = []
requirements_file = this_directory / "requirements.txt"
if requirements_file.exists():
    with open(requirements_file, 'r', encoding='utf-8') as f:
        requirements = [
            line.strip() 
            for line in f 
            if line.strip() and not line.startswith('#')
        ]

setup(
    name="chai-friend",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A beautifully crafted desktop chat application for conversing with AI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/chai-friend",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Communications :: Chat",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: User Interfaces",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "chai-friend=main:main",
        ],
    },
    keywords="ai chat desktop pyqt5 conversation assistant",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/chai-friend/issues",
        "Source": "https://github.com/yourusername/chai-friend",
        "Documentation": "https://github.com/yourusername/chai-friend#readme",
    },
    include_package_data=True,
    zip_safe=False,
)