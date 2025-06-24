# Development Setup - Quick Start

This is a quick reference for setting up and using the development workflow.

## 🚀 Quick Setup

### 1. Repository Configuration (One-time setup)

**Set up branch protection rules** in GitHub:

- Go to **Settings** → **Branches**
- Add protection for `main` and `develop` branches
- See [DEVELOPMENT_FLOW.md](DEVELOPMENT_FLOW.md) for detailed instructions

**Add repository secrets**:

- Go to **Settings** → **Secrets and variables** → **Actions**
- Add `PYPI_API_TOKEN` (from [https://pypi.org](https://pypi.org))
- Add `TEST_PYPI_API_TOKEN` (from [https://test.pypi.org](https://test.pypi.org))

### 2. Local Development Setup

```bash
# Clone and setup
git clone <your-repo-url>
cd gui-image-studio

# Install development dependencies
pip install -e .[dev]
# Or install manually:
pip install pillow>=8.0.0 customtkinter>=5.0.0 pytest>=6.0

# Check development status
python dev_tools.py status
```

## 🔄 Daily Development Workflow

### Starting a New Feature

```bash
# Option 1: Use dev tools (recommended)
python dev_tools.py feature my-awesome-feature

# Option 2: Manual
git checkout develop
git pull origin develop
git checkout -b feature/my-awesome-feature
```

### Working on Feature

```bash
# Make your changes
# ... edit files ...

# Commit changes
git add .
git commit -m "Add awesome new feature"

# Push and create PR
git push -u origin feature/my-awesome-feature
# Create PR to 'develop' via GitHub UI
```

### Testing Your Changes

```bash
# Test locally
python dev_tools.py test

# After merging to develop, test from TestPyPI
pip install \
  --index-url https://test.pypi.org/simple/ \
  --extra-index-url https://pypi.org/simple/ \
  gui-image-studio==1.0.0.dev20241201123456
```

### Creating a Release

```bash
# Option 1: Use dev tools (recommended)
python dev_tools.py release 1.0.1

# Option 2: Manual
git checkout main
git pull origin main
git checkout -b release/v1.0.1
git merge develop
# Update version in pyproject.toml
git add pyproject.toml
git commit -m "Bump version to 1.0.1"
git push -u origin release/v1.0.1
# Create PR to main, then GitHub release
```

## 🎯 Branch Strategy

```text
main (production)
├── develop (integration/testing)
│   ├── feature/new-loader
│   ├── feature/better-ui
│   └── bugfix/image-scaling
└── hotfix/critical-security-fix
```

## 🤖 Automated Workflows

| Trigger | Workflow | Purpose |
|---------|----------|---------|
| Push to `develop` | TestPyPI Upload | Test package uploads |
| PR to `main` | CI Tests | Validate code quality |
| GitHub Release | PyPI Upload | Production release |

## 📋 Quick Commands

```bash
# Development status
python dev_tools.py status

# Create feature branch
python dev_tools.py feature my-feature

# Start release
python dev_tools.py release 1.0.1

# Test package locally
python dev_tools.py test

# Run tests
pytest

# Check code quality
flake8 src/
black --check src/
```

## 🔧 Troubleshooting

**Common Issues:**

1. **TestPyPI upload fails**: Check `TEST_PYPI_API_TOKEN` secret
2. **PyPI upload fails**: Check `PYPI_API_TOKEN` secret
3. **CI fails**: Run tests locally first with `pytest`
4. **Version conflicts**: Ensure version is incremented in `pyproject.toml`

**Getting Help:**

- Check [DEVELOPMENT_FLOW.md](DEVELOPMENT_FLOW.md) for detailed instructions
- Check [PYPI_SETUP.md](PYPI_SETUP.md) for PyPI configuration
- Look at GitHub Actions logs for specific error messages

## 🎉 You're Ready

The development workflow is now set up. Start by creating your first feature branch:

```bash
python dev_tools.py feature my-first-feature
```

Happy coding! 🚀
