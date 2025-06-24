#!/usr/bin/env python3
"""
Release Management Script for GUI Image Studio

This script helps manage releases by:
- Updating version numbers
- Creating release branches
- Running tests
- Building packages
- Creating release notes
"""

import argparse
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def run_command(cmd, check=True, capture_output=True):
    """Run a command and return the result."""
    print(f"Running: {cmd}")
    if isinstance(cmd, str):
        cmd = cmd.split()

    result = subprocess.run(cmd, check=check, capture_output=capture_output, text=True)

    if capture_output and result.stdout:
        print(result.stdout.strip())

    return result


def get_current_version():
    """Get the current version from the package."""
    try:
        result = run_command(
            [
                sys.executable,
                "-c",
                "import gui_image_studio; print(gui_image_studio.__version__)",
            ]
        )
        return result.stdout.strip()
    except (
        subprocess.CalledProcessError,
        ImportError,
        AttributeError,
        FileNotFoundError,
    ) as e:
        # Fallback to reading from __init__.py if package import fails
        print(f"Warning: Could not import package to get version: {e}")
        init_file = Path("src/gui_image_studio/__init__.py")
        if init_file.exists():
            try:
                content = init_file.read_text()
                match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
                if match:
                    return match.group(1)
            except (OSError, IOError) as e:
                print(f"Warning: Could not read __init__.py: {e}")
        return "0.0.0"


def update_version_in_file(file_path, old_version, new_version):
    """Update version in a specific file."""
    if not Path(file_path).exists():
        print(f"Warning: {file_path} not found")
        return False

    content = Path(file_path).read_text()
    updated_content = content.replace(old_version, new_version)

    if content != updated_content:
        Path(file_path).write_text(updated_content)
        print(f"Updated version in {file_path}")
        return True
    else:
        print(f"No version found to update in {file_path}")
        return False


def update_version(new_version):
    """Update version in all relevant files."""
    current_version = get_current_version()
    print(f"Updating version from {current_version} to {new_version}")

    files_to_update = [
        "src/gui_image_studio/__init__.py",
        "pyproject.toml",
        "setup.py",
    ]

    updated_files = []
    for file_path in files_to_update:
        if update_version_in_file(file_path, current_version, new_version):
            updated_files.append(file_path)

    return updated_files


def run_tests():
    """Run the test suite."""
    print("Running test suite...")
    try:
        run_command("pytest", capture_output=False)
        print("✓ All tests passed")
        return True
    except subprocess.CalledProcessError:
        print("✗ Tests failed")
        return False


def run_linting():
    """Run code quality checks."""
    print("Running code quality checks...")
    checks = [
        ("black --check .", "Code formatting"),
        ("isort --check-only .", "Import sorting"),
        ("flake8 src/", "Code linting"),
        ("mypy src/gui_image_studio", "Type checking"),
    ]

    all_passed = True
    for cmd, description in checks:
        try:
            run_command(cmd)
            print(f"✓ {description} passed")
        except subprocess.CalledProcessError:
            print(f"✗ {description} failed")
            all_passed = False

    return all_passed


def build_package():
    """Build the package."""
    print("Building package...")
    try:
        # Clean previous builds
        run_command("rm -rf dist/ build/ *.egg-info/", check=False)

        # Build package
        run_command([sys.executable, "-m", "build"])

        # Check package
        run_command([sys.executable, "-m", "twine", "check", "dist/*"])

        print("✓ Package built successfully")
        return True
    except subprocess.CalledProcessError:
        print("✗ Package build failed")
        return False


def create_release_notes(version):
    """Create release notes template."""
    date = datetime.now().strftime("%Y-%m-%d")

    template = f"""# Release Notes - v{version}

**Release Date:** {date}

## 🎉 What's New

### ✨ New Features
-

### 🐛 Bug Fixes
-

### 🔧 Improvements
-

### 📚 Documentation
-

### 🧪 Testing
-

## 🔄 Breaking Changes

None in this release.

## 📦 Installation

```bash
pip install gui-image-studio=={version}
```

## 🙏 Contributors

Thanks to all contributors who made this release possible!

---

**Full Changelog:** https://github.com/stntg/gui-image-studio/compare/v{get_current_version()}...v{version}
"""

    release_notes_file = f"RELEASE_NOTES_v{version}.md"
    Path(release_notes_file).write_text(template)
    print(f"Created release notes template: {release_notes_file}")
    return release_notes_file


def create_release_branch(version):
    """Create a release branch."""
    branch_name = f"release/v{version}"

    try:
        # Create and checkout release branch
        run_command(f"git checkout -b {branch_name}")
        print(f"✓ Created release branch: {branch_name}")
        return branch_name
    except subprocess.CalledProcessError:
        print(f"✗ Failed to create release branch: {branch_name}")
        return None


def commit_version_changes(version, updated_files):
    """Commit version changes."""
    if not updated_files:
        print("No files to commit")
        return False

    try:
        # Add updated files
        for file_path in updated_files:
            run_command(f"git add {file_path}")

        # Commit changes
        run_command(f"git commit -m 'Bump version to {version}'")
        print(f"✓ Committed version changes")
        return True
    except subprocess.CalledProcessError:
        print("✗ Failed to commit version changes")
        return False


def validate_version(version):
    """Validate version format."""
    pattern = r"^\d+\.\d+\.\d+(?:-[a-zA-Z0-9]+)?$"
    if not re.match(pattern, version):
        print(f"Invalid version format: {version}")
        print("Expected format: MAJOR.MINOR.PATCH or MAJOR.MINOR.PATCH-SUFFIX")
        return False
    return True


def main():
    """Main release function."""
    parser = argparse.ArgumentParser(
        description="Release management for GUI Image Studio"
    )
    parser.add_argument("version", help="New version number (e.g., 1.2.0)")
    parser.add_argument("--skip-tests", action="store_true", help="Skip running tests")
    parser.add_argument("--skip-lint", action="store_true", help="Skip linting checks")
    parser.add_argument(
        "--skip-build", action="store_true", help="Skip building package"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes",
    )

    args = parser.parse_args()

    # Validate version
    if not validate_version(args.version):
        sys.exit(1)

    print(f"🚀 Preparing release v{args.version}")
    print("=" * 50)

    # Change to project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    os.chdir(project_root)

    if args.dry_run:
        print("DRY RUN MODE - No changes will be made")
        print(f"Would update version to: {args.version}")
        print(f"Current version: {get_current_version()}")
        return

    # Run pre-release checks
    if not args.skip_lint:
        if not run_linting():
            print("Linting failed. Fix issues before releasing.")
            sys.exit(1)

    if not args.skip_tests:
        if not run_tests():
            print("Tests failed. Fix issues before releasing.")
            sys.exit(1)

    # Update version
    updated_files = update_version(args.version)

    # Create release branch
    branch_name = create_release_branch(args.version)
    if not branch_name:
        sys.exit(1)

    # Commit version changes
    if not commit_version_changes(args.version, updated_files):
        sys.exit(1)

    # Build package
    if not args.skip_build:
        if not build_package():
            print("Package build failed.")
            sys.exit(1)

    # Create release notes
    release_notes_file = create_release_notes(args.version)

    print("\n🎉 Release preparation complete!")
    print(f"Release branch: {branch_name}")
    print(f"Release notes: {release_notes_file}")
    print("\nNext steps:")
    print("1. Edit the release notes")
    print("2. Push the release branch: git push -u origin " + branch_name)
    print("3. Create a pull request to main")
    print("4. After merge, create and push a tag: git tag v" + args.version)
    print("5. Create a GitHub release")


if __name__ == "__main__":
    main()
