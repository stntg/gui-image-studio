#!/usr/bin/env python3
"""
Setup script for gui-image-studio - GUI Image Studio
"""

import os

from setuptools import find_packages, setup


# Read the README file for long description
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            return f.read()
    return "GUI Image Studio - Complete toolkit for creating, embedding, and managing images in Python GUI applications"


# Read version from __init__.py
def get_version():
    version_file = os.path.join(
        os.path.dirname(__file__), "src", "gui_image_studio", "__init__.py"
    )
    if os.path.exists(version_file):
        with open(version_file, "r") as f:
            for line in f:
                if line.startswith("__version__"):
                    return line.split("=")[1].strip().strip("\"'")
    return "1.0.0"


setup(
    name="gui-image-studio",
    version=get_version(),
    author="Stan Griffiths",  # Replace with your name
    author_email="stantgriffiths@gmail.com",  # Replace with your email
    description="GUI Image Studio - Complete toolkit for creating, embedding, and managing images in Python GUI applications",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/stntg/gui-image-studio",  # Replace with your repository URL
    project_urls={
        "Bug Reports": "https://github.com/stntg/gui-image-studio/issues",
        "Source": "https://github.com/stntg/gui-image-studio",
        "Documentation": "https://github.com/stntg/gui-image-studio#readme",
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Software Development :: User Interfaces",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Framework :: tkinter",
    ],
    python_requires=">=3.8",
    install_requires=[
        "Pillow>=8.0.0",
    ],
    extras_require={
        "customtkinter": ["customtkinter>=5.0.0"],
        "dev": [
            "pytest>=6.0",
            "pytest-cov",
            "black",
            "flake8",
            "mypy",
        ],
        "examples": [
            "customtkinter>=5.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "gui-image-studio-generate=gui_image_studio.cli:generate_embedded_images",
            "gui-image-studio-create-samples=gui_image_studio.cli:create_sample_images",
            "gui-image-studio-designer=gui_image_studio.cli:launch_designer",
        ],
    },
    include_package_data=True,
    package_data={
        "gui_image_studio": ["*.py"],
    },
    keywords="image gui tkinter customtkinter embed resources PIL Pillow",
    zip_safe=False,
)
