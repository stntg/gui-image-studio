# PyPI and TestPyPI Setup Guide

This document explains how to set up both PyPI (production) and TestPyPI (testing)
publishing for this repository.

## Overview

- **PyPI** ([https://pypi.org](https://pypi.org)):
  Production package repository for real releases
- **TestPyPI** ([https://test.pypi.org](https://test.pypi.org)):
  Testing repository for validating packages before production

## Setting up TestPyPI (Testing)

### 1. Create TestPyPI Account

- Go to [test.pypi.org](https://test.pypi.org) and create an account
- Verify your email address
- **Note**: This is separate from your main PyPI account

### 2. Generate TestPyPI API Token

- Go to [TestPyPI Account Settings](https://test.pypi.org/manage/account/)
- Scroll down to the "API tokens" section
- Click "Add API token"
- Give it a descriptive name (e.g., "GitHub Actions - gui-image-studio-test")
- Set the scope to "Entire account"
- Copy the generated token (starts with `pypi-`)

### 3. Add TestPyPI Token to GitHub Secrets

- Go to your GitHub repository
- Navigate to Settings > Secrets and variables > Actions
- Click "New repository secret"
- Name: `TEST_PYPI_API_TOKEN`
- Value: Paste the TestPyPI API token
- Click "Add secret"

## Setting up PyPI (Production)

### 1. Create PyPI Account

- Go to [pypi.org](https://pypi.org) and create an account
- Verify your email address

### 2. Generate PyPI API Token

- Go to [PyPI Account Settings](https://pypi.org/manage/account/)
- Scroll down to the "API tokens" section
- Click "Add API token"
- Give it a descriptive name (e.g., "GitHub Actions - gui-image-studio")
- Set the scope to "Entire account" or limit to specific project
- Copy the generated token (starts with `pypi-`)

### 3. Add PyPI Token to GitHub Secrets

- Go to your GitHub repository
- Navigate to Settings > Secrets and variables > Actions
- Click "New repository secret"
- Name: `PYPI_API_TOKEN`
- Value: Paste the PyPI API token
- Click "Add secret"

## Using the Workflows

### TestPyPI Workflow (test-pypi.yml)

**Triggers:**

- Manual trigger via GitHub Actions UI (workflow_dispatch)
- Automatic trigger on pushes to `develop` branch that modify package files

**Features:**

- Creates test versions with timestamps (e.g., `1.0.0.dev20241201123456`)
- Uploads to TestPyPI for testing
- Validates package installation
- Provides installation commands for testing

**Manual Trigger:**

1. Go to Actions tab in your repository
2. Select "Test PyPI Upload" workflow
3. Click "Run workflow"
4. Optionally specify a version suffix (dev, rc1, alpha1, etc.)

### Production PyPI Workflow (release.yml)

**Triggers:**

- Automatic trigger when you create a GitHub release/tag

**Features:**

- Uses the exact version from `pyproject.toml`
- Publishes to production PyPI
- Creates GitHub release assets

## Testing Your Package

### From TestPyPI

```bash
# Install from TestPyPI (includes dependencies from regular PyPI)
pip install \
  --index-url https://test.pypi.org/simple/ \
  --extra-index-url https://pypi.org/simple/ \
  gui-image-studio==1.0.0.dev20241201123456

# Test the package
python -c "import gui_image_studio; print(gui_image_studio.__version__)"
```

### From Production PyPI

```bash
# Install from PyPI
pip install gui-image-studio

# Test the package
python -c "import gui_image_studio; print(gui_image_studio.__version__)"
```

## Recommended Workflow

1. **Development**: Work on your features in feature branches
2. **Testing**: Merge to `develop` branch to trigger TestPyPI upload
3. **Validation**: Test the package from TestPyPI
4. **Release**: When ready, create a GitHub release to publish to production PyPI

## Troubleshooting

### Common Issues

1. **"Invalid credentials" error**
   - Verify you're using the correct token for the correct service
   - TestPyPI tokens only work with TestPyPI
   - PyPI tokens only work with PyPI

2. **"Package already exists" error**
   - TestPyPI: The workflow creates unique versions with timestamps
   - PyPI: Increment the version in `pyproject.toml` before creating a release

3. **"Token not available" message**
   - The workflows will skip publishing if tokens aren't configured
   - This won't fail the workflow, just skip the upload step

4. **Installation from TestPyPI fails**
   - TestPyPI has propagation delays (can take a few minutes)
   - Some dependencies might not be available on TestPyPI

### Security Notes

- **Never commit API tokens** to your repository
- Use **separate tokens** for TestPyPI and PyPI
- Consider using **project-scoped tokens** for better security
- **Regularly rotate** your API tokens
- TestPyPI and PyPI are **completely separate** services

## Manual Publishing

### To TestPyPI

```bash
# Build the package
python -m build

# Upload to TestPyPI
python -m twine upload --repository testpypi dist/*
```

### To PyPI

```bash
# Build the package
python -m build

# Upload to PyPI
python -m twine upload dist/*
```

## Version Management

- **Production releases**: Use semantic versioning (1.0.0, 1.0.1, 1.1.0)
- **Test releases**: Automatically generated with timestamps
- **Pre-releases**: Use suffixes like `1.0.0rc1`, `1.0.0alpha1`, `1.0.0beta1`
