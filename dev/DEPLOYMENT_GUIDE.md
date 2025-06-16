# Deployment Guide for GUI Image Studio

This guide covers creating releases, publishing to PyPI, and setting up automated workflows with GitHub Actions.

## Table of Contents

1. [Creating Releases](#creating-releases)
2. [Publishing to PyPI](#publishing-to-pypi)
3. [GitHub Actions Setup](#github-actions-setup)
4. [Automated Release Workflow](#automated-release-workflow)
5. [Best Practices](#best-practices)

## Creating Releases

### 1. Version Management

Update version numbers in these files before creating a release:

**pyproject.toml:**

```toml
[project]
version = "1.0.1"  # Update this
```

**src/gui_image_studio/**init**.py:**

```python
__version__ = "1.0.1"  # Update this
```

### 2. Prepare Release Notes

Create or update `CHANGELOG.md`:

```markdown
# Changelog

## [1.0.1] - 2024-01-XX

### Added
- New feature descriptions

### Changed
- Modified functionality descriptions

### Fixed
- Bug fix descriptions

### Removed
- Deprecated feature removals
```

### 3. Create Git Tag and Release

```bash
# Commit version changes
git add .
git commit -m "Bump version to 1.0.1"
git push origin main

# Create and push tag
git tag -a v1.0.1 -m "Release version 1.0.1"
git push origin v1.0.1
```

### 4. Create GitHub Release

1. Go to your repository: <https://github.com/stntg/gui-image-studio/releases>
2. Click "Releases" → "Create a new release"
3. Choose the tag you just created (v1.0.1)
4. Fill in release details:
   - **Release title**: `v1.0.1`
   - **Description**: Copy from CHANGELOG.md
   - **Attach binaries**: Upload any distribution files if needed
5. Click "Publish release"

## Publishing to PyPI

### 1. Setup PyPI Account

1. Create account at [PyPI.org](https://pypi.org/account/register/)
2. Enable 2FA (recommended)
3. Create API token:
   - Go to Account Settings → API tokens
   - Create token with scope "Entire account" or specific to your project
   - Save the token securely

### 2. Install Build Tools

```bash
pip install --upgrade build twine
```

### 3. Build Distribution

```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info/

# Build source and wheel distributions
python -m build
```

This creates:

- `dist/gui_image_studio-1.0.1.tar.gz` (source distribution)
- `dist/gui_image_studio-1.0.1-py3-none-any.whl` (wheel distribution)

### 4. Test Upload (TestPyPI)

First, test with TestPyPI:

```bash
# Upload to TestPyPI
python -m twine upload --repository testpypi dist/*

# Test installation
pip install --index-url https://test.pypi.org/simple/ gui-image-studio
```

### 5. Upload to PyPI

```bash
# Upload to PyPI
python -m twine upload dist/*
```

When prompted, use:

- Username: `__token__`
- Password: Your API token (including `pypi-` prefix)

### 6. Verify Installation

```bash
pip install gui-image-studio
python -c "import gui_image_studio; print(gui_image_studio.__version__)"
```

## GitHub Actions Setup

### 1. Create Workflow Directory

```bash
mkdir -p .github/workflows
```

### 2. Basic CI Workflow

Create `.github/workflows/ci.yml`:

```yaml
name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ['3.7', '3.8', '3.9', '3.10', '3.11']

    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e .
        pip install pytest pytest-cov
    
    - name: Run tests
      run: |
        python test_package.py
        # Add more comprehensive tests here
    
    - name: Test package import
      run: |
        python -c "import gui_image_studio; print('Package imported successfully')"

  lint:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install linting tools
      run: |
        pip install flake8 black isort
    
    - name: Run linters
      run: |
        flake8 src/ --max-line-length=88 --extend-ignore=E203,W503
        black --check src/
        isort --check-only src/
```

### 3. Release and PyPI Publish Workflow

Create `.github/workflows/release.yml`:

```yaml
name: Release and Publish

on:
  release:
    types: [published]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e .
    
    - name: Run tests
      run: |
        python test_package.py

  build-and-publish:
    needs: test
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install build dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    
    - name: Build package
      run: python -m build
    
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: |
        python -m twine upload dist/*
```

### 4. Setup Repository Secrets

1. Go to your repository settings
2. Navigate to "Secrets and variables" → "Actions"
3. Add repository secrets:
   - `PYPI_API_TOKEN`: Your PyPI API token

## Automated Release Workflow

### Complete Automated Release Process

Create `.github/workflows/auto-release.yml`:

```yaml
name: Auto Release

on:
  push:
    branches: [ main ]
    paths:
      - 'src/gui_image_studio/__init__.py'

jobs:
  check-version:
    runs-on: ubuntu-latest
    outputs:
      version: ${{ steps.version.outputs.version }}
      tag_exists: ${{ steps.tag.outputs.exists }}
    steps:
    - uses: actions/checkout@v4
      with:
        fetch-depth: 0
    
    - name: Get version
      id: version
      run: |
        VERSION=$(python -c "import sys; sys.path.insert(0, 'src'); from gui_image_studio import __version__; print(__version__)")
        echo "version=v$VERSION" >> $GITHUB_OUTPUT
    
    - name: Check if tag exists
      id: tag
      run: |
        if git rev-parse "${{ steps.version.outputs.version }}" >/dev/null 2>&1; then
          echo "exists=true" >> $GITHUB_OUTPUT
        else
          echo "exists=false" >> $GITHUB_OUTPUT
        fi

  create-release:
    needs: check-version
    if: needs.check-version.outputs.tag_exists == 'false'
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Create Release
      uses: actions/create-release@v1
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      with:
        tag_name: ${{ needs.check-version.outputs.version }}
        release_name: Release ${{ needs.check-version.outputs.version }}
        draft: false
        prerelease: false
```

## Best Practices

### 1. Version Numbering (Semantic Versioning)

- **MAJOR.MINOR.PATCH** (e.g., 1.2.3)
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### 2. Pre-release Testing

Always test before releasing:

```bash
# Test in virtual environment
python -m venv test_env
source test_env/bin/activate  # Windows: test_env\Scripts\activate
pip install -e .
python test_package.py
deactivate
rm -rf test_env
```

### 3. Release Checklist

- [ ] Update version numbers
- [ ] Update CHANGELOG.md
- [ ] Run all tests locally
- [ ] Test package installation
- [ ] Create git tag
- [ ] Create GitHub release
- [ ] Verify PyPI upload
- [ ] Test PyPI installation
- [ ] Update documentation if needed

### 4. Security Considerations

- Use API tokens instead of passwords
- Store secrets securely in GitHub
- Enable 2FA on PyPI account
- Regularly rotate API tokens
- Review dependencies for vulnerabilities

### 5. Monitoring

After release:

- Monitor PyPI download statistics
- Watch for user issues/bug reports
- Keep dependencies updated
- Monitor security advisories

## Troubleshooting

### Common Issues

**Build fails:**

```bash
# Clean and rebuild
rm -rf dist/ build/ *.egg-info/
python -m build
```

**Upload fails:**

```bash
# Check credentials
python -m twine check dist/*
```

**Version conflicts:**

```bash
# Ensure version is updated in all files
grep -r "version" pyproject.toml src/gui_image_studio/__init__.py
```

### Getting Help

- [PyPI Help](https://pypi.org/help/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Python Packaging Guide](https://packaging.python.org/)

## Example Release Commands

Complete release process:

```bash
# 1. Update version and commit
git add .
git commit -m "Bump version to 1.0.1"
git push origin main

# 2. Create tag
git tag -a v1.0.1 -m "Release version 1.0.1"
git push origin v1.0.1

# 3. Build and upload
rm -rf dist/
python -m build
python -m twine upload dist/*

# 4. Create GitHub release (via web interface)
```

This completes the deployment setup for your gui_image_studio package!
