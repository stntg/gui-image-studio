# Development Guide

This guide provides detailed information for developers who want to contribute to GUI Image Studio.

## Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/stntg/gui-image-studio.git
   cd gui-image-studio
   ```

2. **Set up development environment**:
   ```bash
   python scripts/setup-dev.py
   ```

3. **Verify installation**:
   ```bash
   python scripts/verify-install.py
   ```

## Development Environment Setup

### Prerequisites

- Python 3.8 or higher
- Git
- Virtual environment (recommended)

### Manual Setup

If you prefer to set up the environment manually:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Unix/macOS:
source venv/bin/activate

# Install in development mode
pip install -e .[dev,test,docs]

# Install pre-commit hooks
pre-commit install
```

## Project Structure

```
gui-image-studio/
├── src/
│   └── gui_image_studio/          # Main package
│       ├── __init__.py            # Package initialization
│       ├── __main__.py            # Module entry point
│       ├── image_studio.py        # GUI Image Studio application
│       ├── generator.py           # Image embedding generator
│       ├── image_loader.py        # Image loading utilities
│       ├── embedded_images.py     # Default embedded images
│       ├── sample_creator.py      # Sample image creation
│       └── cli.py                 # Command-line interface
├── tests/                         # Test suite
├── examples/                      # Usage examples
├── docs/                          # Documentation
├── scripts/                       # Development scripts
├── dev_files/                     # Development-only files (not in repo)
├── .github/                       # GitHub workflows and templates
├── pyproject.toml                 # Project configuration
├── CONTRIBUTING.md                # Contribution guidelines
└── README.md                      # Main documentation
```

## Development Workflow

### 1. Creating a Feature Branch

```bash
git checkout develop
git pull origin develop
git checkout -b feature/your-feature-name
```

### 2. Making Changes

- Write code following the project's coding standards
- Add tests for new functionality
- Update documentation as needed
- Run pre-commit checks

### 3. Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=gui_image_studio

# Run specific test file
pytest tests/test_image_studio.py

# Run visual tests (requires display)
pytest -m visual

# Skip visual tests
pytest -m "not visual"
```

### 4. Code Quality

```bash
# Format code
black .
isort .

# Lint code
flake8 src/gui_image_studio tests

# Type checking
mypy src/gui_image_studio

# Security checks
bandit -r src/gui_image_studio/

# Run all checks
tox -e lint
```

### 5. Submitting Changes

```bash
# Push your branch
git push -u origin feature/your-feature-name

# Create a pull request on GitHub
```

## Testing

### Test Categories

- **Unit tests**: Test individual functions and classes
- **Integration tests**: Test component interactions
- **Visual tests**: Test GUI components (marked with `@pytest.mark.visual`)
- **Image tests**: Test image processing functionality

### Running Tests

```bash
# All tests
pytest

# Specific categories
pytest -m "not visual"  # Skip visual tests
pytest -m image         # Only image processing tests
pytest -m gui           # Only GUI tests

# With coverage
pytest --cov=gui_image_studio --cov-report=html
```

### Writing Tests

```python
import pytest
from gui_image_studio import ImageStudio

class TestImageStudio:
    def test_initialization(self):
        """Test basic initialization."""
        studio = ImageStudio()
        assert studio is not None

    @pytest.mark.visual
    def test_gui_creation(self):
        """Test GUI creation (requires display)."""
        import tkinter as tk
        root = tk.Tk()
        studio = ImageStudio(root)
        # Test GUI components
        root.destroy()
```

## Code Style

### Python Code Style

- Follow PEP 8
- Use Black for formatting (line length: 88)
- Use isort for import sorting
- Add type hints for public APIs
- Write docstrings for all public functions

### Example:

```python
from typing import Optional, Tuple
from PIL import Image

def resize_image(
    image: Image.Image,
    size: Tuple[int, int],
    resample: Optional[int] = None
) -> Image.Image:
    """
    Resize an image to the specified size.

    Args:
        image: The input image
        size: Target size as (width, height)
        resample: Resampling algorithm

    Returns:
        Resized image
    """
    return image.resize(size, resample or Image.LANCZOS)
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

- Use clear, concise language
- Include code examples
- Add docstrings to all public APIs
- Update README.md for user-facing changes

## Release Process

### Creating a Release

```bash
# Use the release script
python scripts/release.py 1.2.0

# Or manually:
# 1. Update version numbers
# 2. Create release branch
# 3. Run tests
# 4. Build package
# 5. Create release notes
```

### Version Numbering

We use semantic versioning (SemVer):
- `MAJOR.MINOR.PATCH`
- `MAJOR`: Breaking changes
- `MINOR`: New features (backward compatible)
- `PATCH`: Bug fixes (backward compatible)

## Debugging

### Common Issues

1. **Import errors**: Make sure package is installed in development mode
2. **GUI tests failing**: Ensure you have a display available or use xvfb
3. **Type checking errors**: Add type hints or use `# type: ignore`

### Debugging Tools

```bash
# Run with verbose output
pytest -v

# Run with debugging
pytest --pdb

# Profile performance
pytest --profile

# Check test coverage
pytest --cov=gui_image_studio --cov-report=html
```

## Contributing Guidelines

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for detailed contribution guidelines.

### Key Points

- Follow the code style guidelines
- Write tests for new functionality
- Update documentation
- Use descriptive commit messages
- Create focused pull requests

## Getting Help

- **GitHub Issues**: Report bugs or request features
- **GitHub Discussions**: Ask questions or discuss ideas
- **Code Review**: Ask for feedback on your changes

## Development Scripts

- `scripts/setup-dev.py`: Set up development environment
- `scripts/verify-install.py`: Verify installation
- `scripts/release.py`: Manage releases

## Useful Commands

```bash
# Development setup
python scripts/setup-dev.py

# Run all checks
tox

# Format code
black . && isort .

# Run tests with coverage
pytest --cov=gui_image_studio --cov-report=html

# Build package
python -m build

# Install from local build
pip install dist/*.whl
```
