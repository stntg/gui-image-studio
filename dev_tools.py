#!/usr/bin/env python3
"""
Development Tools for GUI Image Studio

This script provides helpful commands for the development workflow.
"""

import subprocess
import sys
import re
from pathlib import Path


def run_command(cmd, check=True):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=check)
        return result.stdout.strip(), result.stderr.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {cmd}")
        print(f"Error: {e.stderr}")
        return None, e.stderr


def get_current_branch():
    """Get the current git branch."""
    stdout, _ = run_command("git branch --show-current")
    return stdout


def get_current_version():
    """Get the current version from pyproject.toml."""
    try:
        with open("pyproject.toml", "r") as f:
            content = f.read()
            match = re.search(r'version = "([^"]+)"', content)
            if match:
                return match.group(1)
    except FileNotFoundError:
        pass
    return None


def create_feature_branch(feature_name):
    """Create a new feature branch."""
    print(f"Creating feature branch: feature/{feature_name}")
    
    # Switch to develop and pull latest
    print("Switching to develop branch...")
    run_command("git checkout develop")
    run_command("git pull origin develop")
    
    # Create and switch to feature branch
    branch_name = f"feature/{feature_name}"
    run_command(f"git checkout -b {branch_name}")
    
    print(f"✅ Created and switched to branch: {branch_name}")
    print(f"💡 When ready, push with: git push -u origin {branch_name}")


def start_release(version):
    """Start a new release."""
    print(f"Starting release: v{version}")
    
    # Switch to main and pull latest
    print("Switching to main branch...")
    run_command("git checkout main")
    run_command("git pull origin main")
    
    # Create release branch
    branch_name = f"release/v{version}"
    run_command(f"git checkout -b {branch_name}")
    
    # Merge develop
    print("Merging develop branch...")
    run_command("git merge develop")
    
    # Update version in pyproject.toml
    print(f"Updating version to {version}...")
    with open("pyproject.toml", "r") as f:
        content = f.read()
    
    updated_content = re.sub(
        r'version = "[^"]+"',
        f'version = "{version}"',
        content
    )
    
    with open("pyproject.toml", "w") as f:
        f.write(updated_content)
    
    run_command("git add pyproject.toml")
    run_command(f'git commit -m "Bump version to {version}"')
    
    print(f"✅ Release branch created: {branch_name}")
    print(f"💡 Next steps:")
    print(f"   1. Push branch: git push -u origin {branch_name}")
    print(f"   2. Create PR to main")
    print(f"   3. After merge, create GitHub release with tag v{version}")


def test_package_locally():
    """Test the package locally."""
    print("Testing package locally...")
    
    # Build package
    print("Building package...")
    run_command("python -m build")
    
    # Check with twine
    print("Checking package with twine...")
    run_command("python -m twine check dist/*")
    
    # Test installation
    print("Testing installation...")
    run_command("python -m venv test_env")
    
    # Activate virtual environment and test
    if sys.platform == "win32":
        activate_cmd = "test_env\\Scripts\\activate"
    else:
        activate_cmd = "source test_env/bin/activate"
    
    test_commands = [
        f"{activate_cmd} && pip install dist/*.whl",
        f"{activate_cmd} && python -c \"import gui_image_studio; print('Version:', gui_image_studio.__version__)\"",
    ]
    
    for cmd in test_commands:
        stdout, stderr = run_command(cmd)
        if stdout:
            print(stdout)
        if stderr:
            print(stderr)
    
    # Cleanup
    run_command("rmdir /s test_env" if sys.platform == "win32" else "rm -rf test_env", check=False)
    
    print("✅ Local package test completed")


def show_status():
    """Show current development status."""
    print("🔍 Development Status")
    print("=" * 50)
    
    # Current branch
    branch = get_current_branch()
    print(f"Current branch: {branch}")
    
    # Current version
    version = get_current_version()
    print(f"Current version: {version}")
    
    # Git status
    stdout, _ = run_command("git status --porcelain")
    if stdout:
        print(f"Uncommitted changes: {len(stdout.splitlines())} files")
    else:
        print("Working directory clean")
    
    # Check if branches exist
    stdout, _ = run_command("git branch -r")
    remote_branches = stdout.splitlines()
    
    has_develop = any("origin/develop" in branch for branch in remote_branches)
    print(f"Develop branch exists: {'✅' if has_develop else '❌'}")
    
    print("\n💡 Available commands:")
    print("  python dev_tools.py feature <name>     - Create feature branch")
    print("  python dev_tools.py release <version>  - Start release process")
    print("  python dev_tools.py test               - Test package locally")
    print("  python dev_tools.py status             - Show this status")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        show_status()
        return
    
    command = sys.argv[1].lower()
    
    if command == "feature":
        if len(sys.argv) < 3:
            print("Usage: python dev_tools.py feature <feature-name>")
            return
        feature_name = sys.argv[2]
        create_feature_branch(feature_name)
    
    elif command == "release":
        if len(sys.argv) < 3:
            print("Usage: python dev_tools.py release <version>")
            return
        version = sys.argv[2]
        start_release(version)
    
    elif command == "test":
        test_package_locally()
    
    elif command == "status":
        show_status()
    
    else:
        print(f"Unknown command: {command}")
        print("Available commands: feature, release, test, status")


if __name__ == "__main__":
    main()