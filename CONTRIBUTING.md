# Contributing to GUI Image Studio

Thank you for your interest in contributing to GUI Image Studio! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Documentation](#documentation)
- [Submitting Changes](#submitting-changes)
- [Release Process](#release-process)

## Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- A GitHub account
- Tkinter (usually included with Python)
- CustomTkinter for modern UI components

### Development Setup

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:

   ```bash
   git clone https://github.com/stntg/gui-image-studio.git
   cd gui-image-studio
   ```

3. **Set up the development environment**:

   ```bash
   # Create a virtual environment
   python -m venv venv

   # Activate it (Windows)
   venv\Scripts\activate
   # Or on Unix/macOS
   source venv/bin/activate

   # Install in development mode
   pip install -e .[dev,docs,test]
   ```

4. **Install pre-commit hooks**:

   ```bash
   pre-commit install
   ```

5. **Verify the setup**:

   ```bash
   pytest
   python -m gui_image_studio
   ```

## Making Changes

### Branching Strategy

We use a Git Flow-inspired branching model:

- `main` - Production-ready code
- `develop` - Integration branch for features
- `feature/*` - Feature branches
- `hotfix/*` - Critical bug fixes
- `release/*` - Release preparation

### Creating a Feature Branch

```bash
# Switch to develop branch
git checkout develop
git pull origin develop

# Create a new feature branch
git checkout -b feature/your-feature-name

# Make your changes...

# Push the branch
git push -u origin feature/your-feature-name
```

### Coding Standards

We follow these coding standards:

- **PEP 8** for Python code style
- **Black** for code formatting (line length: 88)
- **isort** for import sorting
- **Type hints** for all public APIs
- **Docstrings** for all public functions and classes

### Code Quality Tools

Before submitting, ensure your code passes all checks:

```bash
# Format code
black .
isort .

# Lint code
flake8 .
mypy src/gui_image_studio

# Run security checks
bandit -r src/gui_image_studio/
safety check

# Or run all checks with tox
tox -e lint
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=gui_image_studio

# Run specific test file
pytest tests/test_image_studio.py

# Run tests for specific Python versions
tox -e py38,py39,py310,py311,py312
```

### Writing Tests

- Place tests in the `tests/` directory
- Name test files `test_*.py`
- Use descriptive test names
- Include both unit and integration tests
- Mock external dependencies
- Test edge cases and error conditions

Example test structure:

```python
import pytest
import tkinter as tk
from gui_image_studio import ImageStudio

class TestImageStudio:
    def test_initialization(self, root):
        """Test basic initialization."""
        studio = ImageStudio(root)
        assert studio.master == root

    def test_image_loading(self, root, sample_image):
        """Test image loading functionality."""
        studio = ImageStudio(root)
        studio.load_image(sample_image)
        assert studio.current_image is not None
```

### Visual Tests

For GUI components, we have visual tests marked with `@pytest.mark.visual`:

```bash
# Run visual tests (requires display)
pytest -m visual

# Skip visual tests
pytest -m "not visual"
```

## Documentation

### Building Documentation

```bash
# Install documentation dependencies
pip install -e .[docs]

# Build documentation
cd docs
make html

# Or use tox
tox -e docs
```

### Writing Documentation

- Use **Markdown** for most documentation
- Include **docstrings** for all public APIs
- Add **examples** for complex features
- Update **CHANGELOG.md** for user-facing changes

### Documentation Structure

```text
docs/
├── index.md              # Main documentation page
├── installation.md       # Installation instructions
├── quickstart.md         # Quick start guide
├── user_guide/           # Detailed user guides
├── examples/             # Example code and tutorials
├── api/                  # API reference
└── _static/              # Static assets
```

## Submitting Changes

### Pull Request Process

1. **Ensure your branch is up to date**:

   ```bash
   git checkout develop
   git pull origin develop
   git checkout feature/your-feature-name
   git rebase develop
   ```

2. **Run the full test suite**:

   ```bash
   tox
   ```

3. **Create a pull request** on GitHub:
   - Use a descriptive title
   - Reference any related issues
   - Describe what changes you made and why
   - Include screenshots for UI changes

4. **Address review feedback**:
   - Make requested changes
   - Push updates to your branch
   - Respond to reviewer comments

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] Added tests for new functionality
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
```

## Release Process

### Version Management

We use semantic versioning (SemVer):

- `MAJOR.MINOR.PATCH`
- `MAJOR`: Breaking changes
- `MINOR`: New features (backward compatible)
- `PATCH`: Bug fixes (backward compatible)

### Creating a Release

1. **Create a release branch**:

   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b release/v1.2.0
   ```

2. **Update version numbers**:
   - `src/gui_image_studio/__init__.py`
   - `pyproject.toml`
   - `setup.py`

3. **Update CHANGELOG.md**:
   - Add release notes
   - List all changes since last release

4. **Test the release**:

   ```bash
   tox
   python -m build
   twine check dist/*
   ```

5. **Create pull request** to `main`

6. **After merge, create and push tag**:

   ```bash
   git checkout main
   git pull origin main
   git tag -a v1.2.0 -m "Release version 1.2.0"
   git push origin v1.2.0
   ```

7. **GitHub Actions will automatically**:
   - Run tests
   - Build packages
   - Publish to PyPI
   - Create GitHub release

### Hotfix Process

For critical bugs in production:

1. **Create hotfix branch from main**:

   ```bash
   git checkout main
   git pull origin main
   git checkout -b hotfix/critical-bug-fix
   ```

2. **Make minimal fix**
3. **Test thoroughly**
4. **Create PR to main**
5. **After merge, also merge to develop**

## Getting Help

- **GitHub Issues**: Report bugs or request features
- **GitHub Discussions**: Ask questions or discuss ideas
- **Documentation**: Check the docs first
- **Code Review**: Ask for feedback on your changes

## Recognition

Contributors are recognized in:

- `CONTRIBUTORS.md` file
- GitHub contributors page
- Release notes for significant contributions

Thank you for contributing to GUI Image Studio! 🎉
