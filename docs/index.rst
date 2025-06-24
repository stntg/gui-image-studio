GUI Image Studio Documentation
===============================

.. image:: https://img.shields.io/pypi/v/gui-image-studio.svg
    :target: https://pypi.org/project/gui-image-studio/
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/gui-image-studio.svg
    :target: https://pypi.org/project/gui-image-studio/
    :alt: Python versions

.. image:: https://github.com/stntg/gui-image-studio/workflows/CI/badge.svg
    :target: https://github.com/stntg/gui-image-studio/actions
    :alt: CI Status

.. image:: https://www.codefactor.io/repository/github/stntg/gui-image-studio/badge
    :target: https://www.codefactor.io/repository/github/stntg/gui-image-studio
    :alt: CodeFactor

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code style: black

**GUI Image Studio** is a professional Python library and application for advanced image processing, manipulation, and GUI design. It provides a comprehensive toolkit for creating, editing, and managing images with a modern, intuitive interface built on Tkinter and CustomTkinter.

Features
--------

* **Professional Image Editor**: Full-featured GUI application with advanced editing tools
* **Comprehensive Image Processing**: Support for filters, transformations, and effects
* **Animation Support**: Create and edit animated GIFs with timeline controls
* **Theme System**: Built-in light and dark themes with customization options
* **Batch Processing**: Process multiple images with automated workflows
* **Plugin Architecture**: Extensible system for custom filters and tools
* **Multiple Export Formats**: Support for PNG, JPEG, GIF, BMP, and more
* **Cross-Platform**: Works on Windows, macOS, and Linux

Quick Start
-----------

Installation
~~~~~~~~~~~~

.. code-block:: bash

    pip install gui-image-studio

Launch the Application
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    # Launch the main GUI application
    gui-image-studio-designer

    # Or use Python module
    python -m gui_image_studio

    # Or use the launcher script
    python launch_designer.py

Basic Usage
~~~~~~~~~~~

.. code-block:: python

    import gui_image_studio

    # Load an image
    image = gui_image_studio.get_image("path/to/image.png")

    # Apply transformations
    resized = gui_image_studio.resize_image(image, (800, 600))
    tinted = gui_image_studio.apply_tint(resized, "#FF6B6B")

    # Save the result
    gui_image_studio.save_image(tinted, "output.png")

Command Line Tools
~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    # Create sample images for testing
    gui-image-studio-create-samples

    # Generate embedded image resources
    gui-image-studio-generate --folder images/

    # Check version
    gui-image-studio-designer --version

Table of Contents
-----------------

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   installation
   quickstart
   user_guide/index
   examples/index

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/index
   api/image_loader
   api/image_studio
   api/generator
   api/sample_creator
   api/cli

.. toctree::
   :maxdepth: 2
   :caption: Development

   contributing
   changelog
   license

.. toctree::
   :maxdepth: 1
   :caption: Links

   GitHub Repository <https://github.com/stntg/gui-image-studio>
   PyPI Package <https://pypi.org/project/gui-image-studio/>
   Issue Tracker <https://github.com/stntg/gui-image-studio/issues>

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
