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

**GUI Image Studio** is a comprehensive Python toolkit for creating, embedding, and managing images in Python GUI applications. It provides support for tkinter and customtkinter frameworks with features like image transformations, animated GIF support, and a visual image studio GUI for creating and editing images.

Features
--------

* 🎨 **Visual Image Studio GUI** - Create and edit images with drawing tools
* 🖼️ **Image Embedding** - Convert images to base64 encoded strings for easy distribution
* 📁 **Batch Processing** - Process entire folders of images automatically
* 🎨 **Multi-Framework Support** - Works with tkinter and customtkinter
* 🔧 **Image Transformations** - Resize, rotate, flip, tint, contrast, saturation adjustments
* 📦 **Embedded Python Modules** - Generate Python files with embedded images
* 🎬 **Animated GIF Support** - Create and process animated GIFs with frame control
* 🎯 **High-Quality Compression** - Configurable compression options for optimal file sizes
* 📝 **Sample Image Generation** - Built-in sample creator for testing
* 👁️ **Real-time Preview** - Live preview of transformations and code generation
* 🔍 **Comprehensive Image Information** - Detailed image analysis with smart recommendations
* 🌟 **Advanced Transparency Features** - Preserve existing transparency when making areas transparent

Quick Start
-----------

Installation
~~~~~~~~~~~~

.. code-block:: bash

    pip install gui-image-studio

Launch the Application
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    # For PyPI installations (recommended)
    gui-image-studio-designer

    # For development/contributors (GitHub repo only)
    python launch_designer.py

Basic Usage
~~~~~~~~~~~

.. code-block:: python

    from gui_image_studio import get_image, embed_images_from_folder

    # Get a single image with transformations
    image = get_image(
        "my_image.png",
        framework="tkinter",
        size=(64, 64),
        theme="default"
    )

    # Embed all images from a folder
    embed_images_from_folder(
        folder_path="images/",
        output_file="embedded_images.py",
        compression_quality=85
    )

Command Line Tools
~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    # Launch the Image Studio GUI
    gui-image-studio-designer

    # Create sample images for testing
    gui-image-studio-create-samples

    # Embed images from a folder
    gui-image-studio-generate \
      --folder images/ \
      --output embedded_images.py \
      --quality 85

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
