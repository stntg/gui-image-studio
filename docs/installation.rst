Installation
============

Requirements
------------

GUI Image Studio requires Python 3.8 or later and works with the following operating systems:

* Windows 10/11
* macOS 10.14+
* Linux (Ubuntu 18.04+, CentOS 7+, or equivalent)

Dependencies
~~~~~~~~~~~~

The package has the following dependencies:

* **tkinter** - Usually included with Python
* **customtkinter** - Modern UI components
* **Pillow (PIL)** - Image processing library
* **typing-extensions** - For Python < 3.10 compatibility

Install from PyPI
-----------------

The easiest way to install GUI Image Studio is using pip:

.. code-block:: bash

    pip install gui-image-studio

This will install the latest stable version from PyPI along with all required dependencies.

Install from Source
-------------------

To install the latest development version from GitHub:

.. code-block:: bash

    pip install git+https://github.com/stntg/gui-image-studio.git

Development Installation
------------------------

If you want to contribute to GUI Image Studio or modify the source code:

.. code-block:: bash

    git clone https://github.com/stntg/gui-image-studio.git
    cd gui-image-studio
    pip install -e .[dev]

This installs the package in "editable" mode with development dependencies including:

* **pytest** - Testing framework
* **black** - Code formatting
* **flake8** - Code linting
* **mypy** - Type checking
* **sphinx** - Documentation generation

Verify Installation
-------------------

To verify that GUI Image Studio is installed correctly:

.. code-block:: python

    import gui_image_studio
    print(gui_image_studio.__version__)

Or test the CLI commands:

.. code-block:: bash

    gui-image-studio-designer --version
    gui-image-studio-create-samples --help

Or run the verification script:

.. code-block:: bash

    python scripts/verify-install.py

Troubleshooting
---------------

Common Issues
~~~~~~~~~~~~~

**ImportError: No module named 'tkinter'**

On some Linux distributions, tkinter is not installed by default:

.. code-block:: bash

    # Ubuntu/Debian
    sudo apt-get install python3-tk

    # CentOS/RHEL/Fedora
    sudo yum install tkinter
    # or
    sudo dnf install python3-tkinter

**ImportError: No module named 'customtkinter'**

If CustomTkinter is not installed automatically:

.. code-block:: bash

    pip install customtkinter

**PIL/Pillow Issues**

If you encounter Pillow-related errors:

.. code-block:: bash

    pip install --upgrade Pillow

**Display Issues on Linux**

If you're running on a headless Linux server or in a container, you may need to set up a virtual display:

.. code-block:: bash

    sudo apt-get install xvfb
    export DISPLAY=:99
    Xvfb :99 -screen 0 1024x768x24 &

**Permission Issues**

If you encounter permission errors during installation:

.. code-block:: bash

    pip install --user gui-image-studio

This installs the package for the current user only.

**Windows-Specific Issues**

On Windows, if you encounter issues with the GUI not displaying properly:

1. Ensure you have the latest Windows updates
2. Try running as administrator
3. Check Windows Defender/antivirus settings

**macOS-Specific Issues**

On macOS, if you encounter permission issues:

.. code-block:: bash

    # Use Homebrew Python instead of system Python
    brew install python
    /usr/local/bin/pip3 install gui-image-studio

Optional Dependencies
---------------------

For enhanced functionality, you can install optional dependencies:

**Enhanced Image Formats**

.. code-block:: bash

    pip install pillow-heif  # HEIF/HEIC support
    pip install pillow-avif  # AVIF support

**Performance Improvements**

.. code-block:: bash

    pip install numpy  # Faster array operations
    pip install opencv-python  # Advanced image processing

**Development Tools**

.. code-block:: bash

    pip install gui-image-studio[dev]  # All development dependencies

Getting Help
------------

If you encounter issues not covered here:

1. Check the `GitHub Issues <https://github.com/stntg/gui-image-studio/issues>`_
2. Search the documentation
3. Run the diagnostic script: ``python scripts/verify-install.py``
4. Create a new issue with details about your environment and the problem

System Requirements
-------------------

**Minimum Requirements**

* Python 3.8+
* 512 MB RAM
* 100 MB disk space
* Display resolution: 1024x768

**Recommended Requirements**

* Python 3.10+
* 2 GB RAM
* 500 MB disk space
* Display resolution: 1920x1080 or higher
* Dedicated graphics card (for better performance with large images)

**Supported Image Formats**

* **Input**: PNG, JPEG, GIF, BMP, TIFF, WebP, ICO
* **Output**: PNG, JPEG, GIF, BMP, TIFF, WebP
* **Animation**: GIF (with timeline editing support)
