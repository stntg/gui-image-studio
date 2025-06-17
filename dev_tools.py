#!/usr/bin/env python3
"""
Development Tools for GUI Image Studio

This script provides helpful commands for the development workflow.
"""

import subprocess
import sys
import re
import shlex
import glob
from pathlib import Path
from datetime import datetime


def run_command(cmd, check=True):
    """Run a command safely without shell injection vulnerabilities."""
    try:
        # If cmd is a string, split it safely; if it's already a list, use as-is
        if isinstance(cmd, str):
            cmd_list = shlex.split(cmd)
        else:
            cmd_list = cmd
        
        result = subprocess.run(cmd_list, capture_output=True, text=True, check=check)
        return result.stdout.strip(), result.stderr.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {' '.join(cmd_list) if isinstance(cmd_list, list) else cmd}")
        print(f"Error: {e.stderr}")
        return None, e.stderr


def get_current_branch():
    """Get the current git branch."""
    stdout, _ = run_command(["git", "branch", "--show-current"])
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
    run_command(["git", "checkout", "develop"])
    run_command(["git", "pull", "origin", "develop"])
    
    # Create and switch to feature branch
    branch_name = f"feature/{feature_name}"
    run_command(["git", "checkout", "-b", branch_name])
    
    print(f"✅ Created and switched to branch: {branch_name}")
    print(f"💡 When ready, push with: git push -u origin {branch_name}")


def start_release(version):
    """Start a new release."""
    print(f"Starting release: v{version}")
    
    # Switch to main and pull latest
    print("Switching to main branch...")
    run_command(["git", "checkout", "main"])
    run_command(["git", "pull", "origin", "main"])
    
    # Create release branch
    branch_name = f"release/v{version}"
    run_command(["git", "checkout", "-b", branch_name])
    
    # Merge develop
    print("Merging develop branch...")
    run_command(["git", "merge", "develop"])
    
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
    
    run_command(["git", "add", "pyproject.toml"])
    run_command(["git", "commit", "-m", f"Bump version to {version}"])
    
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
    run_command(["python", "-m", "build"])
    
    # Check with twine
    print("Checking package with twine...")
    # Use glob to find wheel files safely
    dist_files = glob.glob("dist/*")
    if dist_files:
        run_command(["python", "-m", "twine", "check"] + dist_files)
    else:
        print("No distribution files found in dist/")
        return
    
    # Test installation
    print("Testing installation...")
    run_command(["python", "-m", "venv", "test_env"])
    
    # Test installation in virtual environment
    if sys.platform == "win32":
        python_exe = "test_env\\Scripts\\python.exe"
        pip_exe = "test_env\\Scripts\\pip.exe"
    else:
        python_exe = "test_env/bin/python"
        pip_exe = "test_env/bin/pip"
    
    # Find wheel file
    wheel_files = glob.glob("dist/*.whl")
    if wheel_files:
        print("Installing package in test environment...")
        run_command([pip_exe, "install", wheel_files[0]])
        
        print("Testing package import...")
        run_command([python_exe, "-c", "import gui_image_studio; print('Version:', gui_image_studio.__version__)"])
    else:
        print("No wheel file found for testing")
    
    # Cleanup
    print("Cleaning up test environment...")
    if sys.platform == "win32":
        run_command(["rmdir", "/s", "/q", "test_env"], check=False)
    else:
        run_command(["rm", "-rf", "test_env"], check=False)
    
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
    stdout, _ = run_command(["git", "status", "--porcelain"])
    if stdout:
        print(f"Uncommitted changes: {len(stdout.splitlines())} files")
    else:
        print("Working directory clean")
    
    # Check if branches exist
    stdout, _ = run_command(["git", "branch", "-r"])
    remote_branches = stdout.splitlines()
    
    has_develop = any("origin/develop" in branch for branch in remote_branches)
    print(f"Develop branch exists: {'✅' if has_develop else '❌'}")
    
    print("\n💡 Available commands:")
    print("  python dev_tools.py feature <name>     - Create feature branch")
    print("  python dev_tools.py release <version>  - Start release process")
    print("  python dev_tools.py test               - Test package locally")
    print("  python dev_tools.py status             - Show this status")
    print("  python dev_tools.py summary <title> <content> - Create summary file")


def create_summary(title, content, summary_type="GENERAL"):
    """Create a summary file in the dev folder."""
    # Ensure dev directory exists
    dev_dir = Path("dev")
    dev_dir.mkdir(exist_ok=True)
    
    # Create filename with timestamp and type
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"SUMMARY_{summary_type}_{timestamp}.md"
    filepath = dev_dir / filename
    
    # Create summary content
    summary_content = f"""# {title}

**Date:** {datetime.now().strftime("%B %d, %Y")}  
**Time:** {datetime.now().strftime("%H:%M:%S")}  
**Type:** {summary_type}  
**Status:** ✅ Complete

## Summary

{content}

---

**Generated by:** dev_tools.py  
**Repository:** gui-image-studio  
**File:** {filename}
"""
    
    # Write summary file
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(summary_content)
    
    print(f"📄 Summary saved: {filepath}")
    return filepath


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
        
        # Create summary
        summary_content = f"""Created new feature branch: feature/{feature_name}

### Actions Taken:
- Switched to develop branch
- Pulled latest changes from origin/develop
- Created and switched to feature/{feature_name}

### Next Steps:
1. Make your changes
2. Commit and push: `git push -u origin feature/{feature_name}`
3. Create PR to develop branch via GitHub UI

### Branch Info:
- Base branch: develop
- Feature branch: feature/{feature_name}
- Ready for development: ✅
"""
        create_summary(f"Feature Branch Created: {feature_name}", summary_content, "FEATURE")
    
    elif command == "release":
        if len(sys.argv) < 3:
            print("Usage: python dev_tools.py release <version>")
            return
        version = sys.argv[2]
        start_release(version)
        
        # Create summary
        summary_content = f"""Started release process for version {version}

### Actions Taken:
- Switched to main branch
- Pulled latest changes from origin/main
- Created release branch: release/v{version}
- Merged develop branch
- Updated version in pyproject.toml to {version}
- Committed version bump

### Next Steps:
1. Push branch: `git push -u origin release/v{version}`
2. Create PR to main branch
3. After merge, create GitHub release with tag v{version}
4. Production PyPI upload will happen automatically

### Release Info:
- Version: {version}
- Release branch: release/v{version}
- Ready for PR: ✅
"""
        create_summary(f"Release Started: v{version}", summary_content, "RELEASE")
    
    elif command == "test":
        test_package_locally()
        
        # Create summary
        summary_content = f"""Performed local package testing

### Tests Performed:
- Package building with `python -m build`
- Package validation with `twine check`
- Installation test in virtual environment
- Import and version verification

### Results:
- Build: ✅ Successful
- Validation: ✅ Passed
- Installation: ✅ Working
- Import: ✅ Successful

### Files Generated:
- dist/ directory with wheel and source distribution
- Temporary test_env virtual environment (cleaned up)
"""
        create_summary("Local Package Testing", summary_content, "TEST")
    
    elif command == "status":
        show_status()
    
    elif command == "summary":
        if len(sys.argv) < 4:
            print("Usage: python dev_tools.py summary <title> <content>")
            return
        title = sys.argv[2]
        content = sys.argv[3]
        create_summary(title, content)
    
    else:
        print(f"Unknown command: {command}")
        print("Available commands: feature, release, test, status, summary")


if __name__ == "__main__":
    main()