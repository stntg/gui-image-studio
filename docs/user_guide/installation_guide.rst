Installation Guide
==================

This guide provides detailed instructions for installing GUI Image Studio on different platforms and environments.

System Requirements
-------------------

**Minimum Requirements:**
- Python 3.8 or later
- 512 MB RAM
- 100 MB disk space
- Display resolution: 1024x768

**Recommended Requirements:**
- Python 3.10 or later
- 2 GB RAM
- 500 MB disk space
- Display resolution: 1920x1080 or higher

**Supported Operating Systems:**
- Windows 10/11
- macOS 10.14+
- Linux (Ubuntu 18.04+, CentOS 7+, or equivalent)

Installation Methods
--------------------

Method 1: Install from PyPI (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The easiest way to install GUI Image Studio:

.. code-block:: bash

    pip install gui-image-studio

This installs the latest stable version with all required dependencies.

Method 2: Install from Source
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For the latest development version:

.. code-block:: bash

    git clone https://github.com/stntg/gui-image-studio.git
    cd gui-image-studio
    pip install -e .

Method 3: Development Installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For contributors and developers:

.. code-block:: bash

    git clone https://github.com/stntg/gui-image-studio.git
    cd gui-image-studio
    pip install -e .[dev,test,docs]

This includes all development dependencies.

Dependencies
------------

**Required Dependencies:**

.. code-block:: text

    Pillow >= 8.0.0          # Image processing
    threepanewindows >= 1.0.0 # Window layout system

**Optional Dependencies:**

.. code-block:: text

    customtkinter >= 5.0.0   # Modern UI components

**Development Dependencies:**

.. code-block:: text

    pytest >= 7.0            # Testing framework
    black                     # Code formatting
    flake8                    # Code linting
    mypy                      # Type checking
    sphinx >= 5.0            # Documentation

Platform-Specific Instructions
-------------------------------

Windows Installation
~~~~~~~~~~~~~~~~~~~~~

**Using pip (Recommended):**

.. code-block:: cmd

    pip install gui-image-studio

**Using conda:**

.. code-block:: cmd

    conda install -c conda-forge pillow
    pip install gui-image-studio

**Common Windows Issues:**

1. **Missing Visual C++ Redistributable:**
   Download from Microsoft's website if you encounter compilation errors.

2. **Permission Issues:**
   Run Command Prompt as Administrator or use:

   .. code-block:: cmd

       pip install --user gui-image-studio

3. **PATH Issues:**
   Ensure Python Scripts directory is in your PATH.

macOS Installation
~~~~~~~~~~~~~~~~~~

**Using pip:**

.. code-block:: bash

    pip3 install gui-image-studio

**Using Homebrew:**

.. code-block:: bash

    brew install python
    pip3 install gui-image-studio

**macOS-Specific Notes:**

1. **Xcode Command Line Tools:**
   May be required for some dependencies:

   .. code-block:: bash

       xcode-select --install

2. **Security Warnings:**
   You may need to allow the application in System Preferences > Security & Privacy.

Linux Installation
~~~~~~~~~~~~~~~~~~

**Ubuntu/Debian:**

.. code-block:: bash

    # Install system dependencies
    sudo apt-get update
    sudo apt-get install python3-pip python3-tk python3-dev

    # Install GUI Image Studio
    pip3 install gui-image-studio

**CentOS/RHEL/Fedora:**

.. code-block:: bash

    # Install system dependencies
    sudo yum install python3-pip python3-tkinter python3-devel
    # or for newer versions:
    sudo dnf install python3-pip python3-tkinter python3-devel

    # Install GUI Image Studio
    pip3 install gui-image-studio

**Arch Linux:**

.. code-block:: bash

    # Install system dependencies
    sudo pacman -S python-pip tk python-pillow

    # Install GUI Image Studio
    pip install gui-image-studio

Virtual Environment Setup
--------------------------

**Creating a Virtual Environment:**

.. code-block:: bash

    # Create virtual environment
    python -m venv gui-image-studio-env

    # Activate (Linux/macOS)
    source gui-image-studio-env/bin/activate

    # Activate (Windows)
    gui-image-studio-env\Scripts\activate

    # Install GUI Image Studio
    pip install gui-image-studio

**Using conda:**

.. code-block:: bash

    # Create conda environment
    conda create -n gui-image-studio python=3.10
    conda activate gui-image-studio

    # Install dependencies
    conda install pillow
    pip install gui-image-studio

Verification
------------

**Test Installation:**

.. code-block:: python

    import gui_image_studio
    print(f"GUI Image Studio version: {gui_image_studio.__version__}")

**Test CLI Commands:**

.. code-block:: bash

    # Test designer launch
    gui-image-studio-designer --help

    # Test sample creation
    gui-image-studio-create-samples --help

    # Test image generation
    gui-image-studio-generate --help

**Test Basic Functionality:**

.. code-block:: python

    from gui_image_studio import get_image, create_sample_images

    # Create sample images
    create_sample_images()

    # Load a sample image
    image = get_image("sample_icon", framework="tkinter")
    print("Installation successful!")

Troubleshooting
---------------

Common Installation Issues
~~~~~~~~~~~~~~~~~~~~~~~~~~

**1. ImportError: No module named 'tkinter'**

*Linux Solution:*

.. code-block:: bash

    # Ubuntu/Debian
    sudo apt-get install python3-tk

    # CentOS/RHEL
    sudo yum install tkinter

**2. PIL/Pillow Installation Issues**

.. code-block:: bash

    # Upgrade pip first
    pip install --upgrade pip

    # Install/upgrade Pillow
    pip install --upgrade Pillow

**3. Permission Denied Errors**

.. code-block:: bash

    # Install for current user only
    pip install --user gui-image-studio

**4. SSL Certificate Errors**

.. code-block:: bash

    # Use trusted hosts
    pip install --trusted-host pypi.org --trusted-host pypi.python.org gui-image-studio

**5. Network/Proxy Issues**

.. code-block:: bash

    # Configure proxy
    pip install --proxy http://user:password@proxy.server:port gui-image-studio

Version Management
~~~~~~~~~~~~~~~~~~

**Check Current Version:**

.. code-block:: bash

    pip show gui-image-studio

**Upgrade to Latest Version:**

.. code-block:: bash

    pip install --upgrade gui-image-studio

**Install Specific Version:**

.. code-block:: bash

    pip install gui-image-studio==1.1.0

**Downgrade Version:**

.. code-block:: bash

    pip install gui-image-studio==1.0.0

Uninstallation
--------------

**Remove GUI Image Studio:**

.. code-block:: bash

    pip uninstall gui-image-studio

**Clean Uninstall (remove all dependencies):**

.. code-block:: bash

    pip uninstall gui-image-studio Pillow threepanewindows

**Remove Virtual Environment:**

.. code-block:: bash

    # Deactivate first
    deactivate

    # Remove directory
    rm -rf gui-image-studio-env

Docker Installation
-------------------

**Using Docker:**

.. code-block:: dockerfile

    FROM python:3.10-slim

    # Install system dependencies
    RUN apt-get update && apt-get install -y \
        python3-tk \
        && rm -rf /var/lib/apt/lists/*

    # Install GUI Image Studio
    RUN pip install gui-image-studio

    # Set working directory
    WORKDIR /app

    # Copy your application
    COPY . .

    # Run your application
    CMD ["python", "your_app.py"]

**Docker Compose Example:**

.. code-block:: yaml

    version: '3.8'
    services:
      gui-image-studio:
        build: .
        volumes:
          - ./images:/app/images
          - ./output:/app/output
        environment:
          - DISPLAY=${DISPLAY}
        volumes:
          - /tmp/.X11-unix:/tmp/.X11-unix

CI/CD Integration
-----------------

**GitHub Actions Example:**

.. code-block:: yaml

    name: Test GUI Image Studio
    on: [push, pull_request]

    jobs:
      test:
        runs-on: ubuntu-latest
        strategy:
          matrix:
            python-version: [3.8, 3.9, '3.10', 3.11]

        steps:
        - uses: actions/checkout@v4
        - name: Set up Python ${{ matrix.python-version }}
          uses: actions/setup-python@v4
          with:
            python-version: ${{ matrix.python-version }}

        - name: Install system dependencies
          run: |
            sudo apt-get update
            sudo apt-get install python3-tk

        - name: Install GUI Image Studio
          run: |
            pip install gui-image-studio

        - name: Test installation
          run: |
            python -c "import gui_image_studio; print('Success!')"

**Travis CI Example:**

.. code-block:: yaml

    language: python
    python:
      - "3.8"
      - "3.9"
      - "3.10"
      - "3.11"

    before_install:
      - sudo apt-get update
      - sudo apt-get install python3-tk

    install:
      - pip install gui-image-studio

    script:
      - python -c "import gui_image_studio"

Getting Help
------------

If you encounter installation issues:

1. **Check the troubleshooting section above**
2. **Search existing issues:** https://github.com/stntg/gui-image-studio/issues
3. **Create a new issue** with:
   - Your operating system and version
   - Python version
   - Complete error message
   - Installation method used
4. **Join community discussions**

**Diagnostic Information:**

When reporting issues, include this diagnostic information:

.. code-block:: python

    import sys
    import platform
    import pip

    print(f"Python version: {sys.version}")
    print(f"Platform: {platform.platform()}")
    print(f"Architecture: {platform.architecture()}")

    try:
        import gui_image_studio
        print(f"GUI Image Studio version: {gui_image_studio.__version__}")
    except ImportError as e:
        print(f"Import error: {e}")

Next Steps
----------

After successful installation:

1. **Read the Quick Start Guide:** :doc:`first_steps`
2. **Explore the Interface:** :doc:`interface_overview`
3. **Try the Examples:** :doc:`../examples/index`
4. **Check the API Reference:** :doc:`../api/index`
