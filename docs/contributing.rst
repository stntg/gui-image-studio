Contributing
============

We welcome contributions to GUI Image Studio! This guide will help you get started with contributing to the project.

Getting Started
---------------

**Prerequisites**

* Python 3.8 or later
* Git for version control
* Basic knowledge of image processing concepts
* Familiarity with Tkinter/CustomTkinter (for GUI contributions)

**Development Setup**

1. **Fork and Clone the Repository**

   .. code-block:: bash

       git clone https://github.com/yourusername/gui-image-studio.git
       cd gui-image-studio

2. **Create a Virtual Environment**

   .. code-block:: bash

       python -m venv venv
       source venv/bin/activate  # On Windows: venv\Scripts\activate

3. **Install Development Dependencies**

   .. code-block:: bash

       pip install -e .[dev]

4. **Verify Installation**

   .. code-block:: bash

       python scripts/verify-install.py
       pytest tests/

Types of Contributions
----------------------

**Code Contributions**

* Bug fixes and improvements
* New image processing features
* GUI enhancements
* Performance optimizations
* Documentation improvements

**Non-Code Contributions**

* Bug reports and feature requests
* Documentation improvements
* Example applications
* Testing and quality assurance
* Community support

**Areas Needing Help**

* Advanced image filters and effects
* Animation tools and timeline features
* Plugin system development
* Performance optimization
* Cross-platform compatibility
* Accessibility improvements

Development Workflow
--------------------

**1. Create a Feature Branch**

.. code-block:: bash

    git checkout -b feature/your-feature-name

**2. Make Your Changes**

* Follow the coding standards (see below)
* Add tests for new functionality
* Update documentation as needed
* Test your changes thoroughly

**3. Run Quality Checks**

.. code-block:: bash

    # Run tests
    pytest tests/

    # Check code formatting
    black --check src/

    # Run linting
    flake8 src/

    # Type checking
    mypy src/

**4. Commit Your Changes**

.. code-block:: bash

    git add .
    git commit -m "Add feature: your feature description"

**5. Push and Create Pull Request**

.. code-block:: bash

    git push origin feature/your-feature-name

Then create a pull request on GitHub.

Coding Standards
----------------

**Python Style**

* Follow PEP 8 style guidelines
* Use Black for code formatting
* Maximum line length: 88 characters
* Use type hints for all public functions

**Code Organization**

.. code-block:: python

    """
    Module docstring describing the module's purpose.
    """

    import standard_library_modules
    import third_party_modules
    import local_modules

    # Constants
    DEFAULT_QUALITY = 95

    class ExampleClass:
        """Class docstring."""

        def __init__(self, param: str) -> None:
            """Initialize with parameter."""
            self.param = param

        def public_method(self, arg: int) -> str:
            """Public method with type hints and docstring."""
            return self._private_method(arg)

        def _private_method(self, arg: int) -> str:
            """Private method (prefixed with underscore)."""
            return f"{self.param}: {arg}"

**Documentation Standards**

* Use Google-style docstrings
* Include type hints in function signatures
* Provide examples for complex functions
* Document all public APIs

.. code-block:: python

    def process_image(image: Image.Image, filter_type: str, intensity: float = 1.0) -> Image.Image:
        """Apply a filter to an image.

        Args:
            image: The input PIL Image object
            filter_type: Type of filter to apply ('blur', 'sharpen', 'emboss')
            intensity: Filter intensity from 0.0 to 1.0 (default: 1.0)

        Returns:
            Processed PIL Image object

        Raises:
            ValueError: If filter_type is not supported
            TypeError: If image is not a PIL Image object

        Example:
            >>> image = get_image("photo.jpg")
            >>> blurred = process_image(image, "blur", 0.5)
            >>> save_image(blurred, "blurred_photo.jpg")
        """
        # Implementation would go here
        if filter_type not in ['blur', 'sharpen', 'emboss']:
            raise ValueError(f"Unsupported filter type: {filter_type}")

        # Apply the filter based on type and intensity
        # This is a placeholder implementation
        return image

Testing Guidelines
------------------

**Test Structure**

.. code-block:: text

    tests/
    ├── test_image_loader.py      # Test core image operations
    ├── test_image_studio.py      # Test GUI components
    ├── test_generator.py         # Test resource generation
    ├── test_cli.py              # Test command-line interface
    └── fixtures/                # Test images and data
        ├── sample_image.png
        └── sample_animation.gif

**Writing Tests**

.. code-block:: python

    import pytest
    from PIL import Image
    import gui_image_studio

    class TestImageLoader:
        """Test cases for image loading functionality."""

        def test_load_valid_image(self):
            """Test loading a valid image file."""
            image = gui_image_studio.get_image("tests/fixtures/sample_image.png")
            assert isinstance(image, Image.Image)
            assert image.size == (100, 100)

        def test_load_nonexistent_image(self):
            """Test loading a non-existent image file."""
            with pytest.raises(FileNotFoundError):
                gui_image_studio.get_image("nonexistent.png")

        @pytest.mark.parametrize("color,expected", [
            ("#FF0000", (255, 0, 0)),
            ("#00FF00", (0, 255, 0)),
            ("#0000FF", (0, 0, 255)),
        ])
        def test_apply_tint_colors(self, color, expected):
            """Test tinting with different colors."""
            image = Image.new("RGB", (10, 10), "white")
            tinted = gui_image_studio.apply_tint(image, color)
            # Add assertions to verify tinting worked correctly

**Running Tests**

.. code-block:: bash

    # Run all tests
    pytest

    # Run specific test file
    pytest tests/test_image_loader.py

    # Run with coverage
    pytest --cov=gui_image_studio

    # Run tests matching pattern
    pytest -k "test_load"

Pull Request Guidelines
-----------------------

**Before Submitting**

* Ensure all tests pass
* Update documentation if needed
* Add changelog entry for significant changes
* Rebase your branch on the latest main

**Pull Request Template**

.. code-block:: text

    ## Description
    Brief description of the changes made.

    ## Type of Change
    - [ ] Bug fix (non-breaking change which fixes an issue)
    - [ ] New feature (non-breaking change which adds functionality)
    - [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
    - [ ] Documentation update

    ## Testing
    - [ ] Tests pass locally
    - [ ] New tests added for new functionality
    - [ ] Manual testing completed

    ## Checklist
    - [ ] Code follows project style guidelines
    - [ ] Self-review completed
    - [ ] Documentation updated
    - [ ] Changelog updated (if applicable)

**Review Process**

1. Automated checks run (CI/CD)
2. Code review by maintainers
3. Address feedback and make changes
4. Final approval and merge

Issue Reporting
---------------

**Bug Reports**

Use the bug report template and include:

* GUI Image Studio version
* Python version and platform
* Steps to reproduce
* Expected vs actual behavior
* Error messages and stack traces
* Sample images (if relevant)

**Feature Requests**

Use the feature request template and include:

* Clear description of the feature
* Use case and motivation
* Proposed implementation (if any)
* Examples from other tools

**Security Issues**

For security vulnerabilities:

* Do not create public issues
* Email security@gui-image-studio.org
* Include detailed description
* Allow time for fix before disclosure

Documentation Contributions
---------------------------

**Types of Documentation**

* API documentation (docstrings)
* User guides and tutorials
* Example applications
* Developer documentation

**Documentation Standards**

* Use reStructuredText (.rst) format
* Follow existing structure and style
* Include code examples
* Test all code examples

**Building Documentation**

.. code-block:: bash

    cd docs/
    make html
    # Open _build/html/index.html in browser

Community Guidelines
--------------------

**Code of Conduct**

* Be respectful and inclusive
* Focus on constructive feedback
* Help newcomers learn and contribute
* Maintain professional communication

**Communication Channels**

* GitHub Issues for bugs and features
* GitHub Discussions for questions
* Pull Request reviews for code feedback

**Recognition**

Contributors are recognized in:

* CONTRIBUTORS.md file
* Release notes
* Documentation credits
* Annual contributor highlights

Getting Help
------------

**For Contributors**

* Check existing issues and pull requests
* Read the developer documentation
* Ask questions in GitHub Discussions
* Join the contributor chat (if available)

**Mentorship**

New contributors can request mentorship:

* Comment on "good first issue" labels
* Ask for guidance in discussions
* Pair programming sessions (when available)

Release Process
---------------

**Version Numbering**

We follow Semantic Versioning (SemVer):

* MAJOR.MINOR.PATCH (e.g., 1.2.3)
* MAJOR: Breaking changes
* MINOR: New features (backward compatible)
* PATCH: Bug fixes (backward compatible)

**Release Checklist**

1. Update version numbers
2. Update CHANGELOG.md
3. Run full test suite
4. Build and test packages
5. Create release tag
6. Deploy to PyPI
7. Update documentation

Thank You!
----------

Thank you for contributing to GUI Image Studio! Your contributions help make this project better for everyone.

**Questions?**

If you have questions about contributing:

* Check the FAQ in our documentation
* Search existing GitHub issues
* Create a new discussion
* Contact the maintainers

We appreciate your time and effort in making GUI Image Studio better!
