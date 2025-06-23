#!/usr/bin/env python3
"""
Development Environment Setup Script for GUI Image Studio

This script sets up a complete development environment for GUI Image Studio,
including all necessary dependencies, pre-commit hooks, and development tools.
"""

import os
import subprocess
import sys
from pathlib import Path


def run_command(cmd, check=True, shell=False):
    """Run a command and handle errors."""
    print(f"Running: {cmd}")
    try:
        if isinstance(cmd, str) and not shell:
            cmd = cmd.split()
        result = subprocess.run(cmd, check=check, shell=shell, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        if check:
            sys.exit(1)
        return e


def check_python_version():
    """Check if Python version is supported."""
    version = sys.version_info
    if version < (3, 8):
        print("Error: Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✓ Python {version.major}.{version.minor}.{version.micro} is supported")


def check_git():
    """Check if git is available."""
    try:
        result = run_command("git --version")
        print(f"✓ Git is available: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠ Git is not available. Some features may not work.")
        return False


def install_package_dev():
    """Install the package in development mode."""
    print("\n📦 Installing package in development mode...")
    run_command([sys.executable, "-m", "pip", "install", "-e", ".[dev,test,docs]"])
    print("✓ Package installed in development mode")


def setup_pre_commit():
    """Set up pre-commit hooks."""
    print("\n🔧 Setting up pre-commit hooks...")
    try:
        run_command("pre-commit install")
        run_command("pre-commit install --hook-type commit-msg")
        print("✓ Pre-commit hooks installed")
        
        # Run pre-commit on all files to ensure everything is set up correctly
        print("Running pre-commit on all files...")
        result = run_command("pre-commit run --all-files", check=False)
        if result.returncode == 0:
            print("✓ Pre-commit checks passed")
        else:
            print("⚠ Some pre-commit checks failed. This is normal for initial setup.")
            print("Run 'pre-commit run --all-files' again after fixing any issues.")
    except subprocess.CalledProcessError:
        print("⚠ Failed to set up pre-commit hooks. You may need to install pre-commit manually.")


def create_directories():
    """Create necessary directories."""
    print("\n📁 Creating necessary directories...")
    directories = [
        "tests",
        "docs",
        "examples",
        "scripts",
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✓ Created/verified directory: {directory}")


def verify_installation():
    """Verify that the installation was successful."""
    print("\n🔍 Verifying installation...")
    
    try:
        # Test package import
        result = run_command([sys.executable, "-c", "import gui_image_studio; print(f'GUI Image Studio version: {gui_image_studio.__version__}')"])
        print("✓ Package import successful")
        
        # Test CLI commands
        try:
            run_command([sys.executable, "-m", "gui_image_studio", "--help"], check=False)
            print("✓ CLI commands available")
        except:
            print("⚠ CLI commands may not be fully functional")
        
        # Test development tools
        tools = ["black", "flake8", "mypy", "pytest", "isort"]
        for tool in tools:
            try:
                run_command([tool, "--version"], check=False)
                print(f"✓ {tool} is available")
            except:
                print(f"⚠ {tool} may not be available")
                
    except Exception as e:
        print(f"⚠ Verification failed: {e}")


def run_tests():
    """Run a quick test to ensure everything is working."""
    print("\n🧪 Running quick tests...")
    try:
        result = run_command([sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short"], check=False)
        if result.returncode == 0:
            print("✓ All tests passed")
        else:
            print("⚠ Some tests failed. This may be normal for initial setup.")
    except:
        print("⚠ Could not run tests. Make sure pytest is installed.")


def print_next_steps():
    """Print next steps for the developer."""
    print("\n🎉 Development environment setup complete!")
    print("\nNext steps:")
    print("1. Start developing! The package is installed in editable mode.")
    print("2. Run tests with: pytest")
    print("3. Format code with: black .")
    print("4. Check code quality with: flake8 src/")
    print("5. Type check with: mypy src/gui_image_studio")
    print("6. Run all checks with: tox")
    print("\nUseful commands:")
    print("- pytest --cov=gui_image_studio  # Run tests with coverage")
    print("- pre-commit run --all-files     # Run all pre-commit checks")
    print("- python -m gui_image_studio     # Run the CLI")
    print("- tox -e lint                    # Run linting checks")
    print("- tox -e docs                    # Build documentation")


def main():
    """Main setup function."""
    print("🚀 Setting up GUI Image Studio development environment...")
    print("=" * 60)
    
    # Change to project root directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    os.chdir(project_root)
    print(f"Working directory: {project_root}")
    
    # Run setup steps
    check_python_version()
    git_available = check_git()
    create_directories()
    install_package_dev()
    
    if git_available:
        setup_pre_commit()
    
    verify_installation()
    run_tests()
    print_next_steps()


if __name__ == "__main__":
    main()