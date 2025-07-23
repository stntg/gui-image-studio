Troubleshooting
===============

This comprehensive troubleshooting guide helps you resolve common issues with GUI Image Studio installation, usage, and development.

Installation Issues
-------------------

Package Installation Problems
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Issue: pip install fails**

.. code-block:: text

    ERROR: Could not find a version that satisfies the requirement gui-image-studio

**Solutions:**

.. code-block:: bash

    # Update pip first
    pip install --upgrade pip

    # Try with explicit index
    pip install --index-url https://pypi.org/simple/ gui-image-studio

    # Install from source if PyPI fails
    pip install git+https://github.com/stntg/gui-image-studio.git

**Issue: Permission denied during installation**

.. code-block:: text

    ERROR: Could not install packages due to an EnvironmentError: [Errno 13] Permission denied

**Solutions:**

.. code-block:: bash

    # Install for current user only
    pip install --user gui-image-studio

    # Use virtual environment (recommended)
    python -m venv gui_studio_env
    source gui_studio_env/bin/activate  # Linux/macOS
    # gui_studio_env\Scripts\activate  # Windows
    pip install gui-image-studio

    # On Linux/macOS, use sudo only as last resort
    sudo pip install gui-image-studio

Dependency Issues
~~~~~~~~~~~~~~~~~

**Issue: ImportError: No module named 'tkinter'**

This is common on Linux systems where tkinter is not installed by default.

**Solutions:**

.. code-block:: bash

    # Ubuntu/Debian
    sudo apt-get update
    sudo apt-get install python3-tk

    # CentOS/RHEL/Fedora
    sudo yum install tkinter
    # or for newer versions:
    sudo dnf install python3-tkinter

    # Arch Linux
    sudo pacman -S tk

**Issue: PIL/Pillow installation fails**

.. code-block:: text

    ERROR: Failed building wheel for Pillow

**Solutions:**

.. code-block:: bash

    # Install system dependencies first

    # Ubuntu/Debian
    sudo apt-get install python3-dev python3-setuptools
    sudo apt-get install libtiff5-dev libjpeg8-dev libopenjp2-7-dev
    sudo apt-get install zlib1g-dev libfreetype6-dev liblcms2-dev
    sudo apt-get install libwebp-dev tcl8.6-dev tk8.6-dev python3-tk

    # CentOS/RHEL/Fedora
    sudo yum install python3-devel python3-setuptools
    sudo yum install libtiff-devel libjpeg-devel openjpeg2-devel
    sudo yum install zlib-devel freetype-devel lcms2-devel
    sudo yum install libwebp-devel tcl-devel tk-devel

    # Then reinstall Pillow
    pip install --upgrade Pillow

**Issue: CustomTkinter not found**

.. code-block:: text

    ImportError: No module named 'customtkinter'

**Solutions:**

.. code-block:: bash

    # Install CustomTkinter
    pip install customtkinter

    # Or install specific version
    pip install customtkinter>=5.0.0

    # If you don't need CustomTkinter, use only tkinter
    image = get_image("test.png", framework="tkinter")

Runtime Issues
--------------

Image Loading Problems
~~~~~~~~~~~~~~~~~~~~~~

**Issue: FileNotFoundError when loading images**

.. code-block:: text

    FileNotFoundError: [Errno 2] No such file or directory: 'image.png'

**Solutions:**

.. code-block:: python

    import os
    from gui_image_studio import get_image

    # Check if file exists
    image_path = "path/to/image.png"
    if os.path.exists(image_path):
        image = get_image(image_path, framework="tkinter")
    else:
        print(f"Image not found: {image_path}")

    # Use absolute paths
    import os
    image_path = os.path.abspath("image.png")
    image = get_image(image_path, framework="tkinter")

    # Handle missing images gracefully
    def safe_load_image(path, **kwargs):
        try:
            return get_image(path, **kwargs)
        except FileNotFoundError:
            print(f"Image not found: {path}")
            return None
        except Exception as e:
            print(f"Error loading image: {e}")
            return None

**Issue: Unsupported image format**

.. code-block:: text

    PIL.UnidentifiedImageError: cannot identify image file

**Solutions:**

.. code-block:: python

    # Check supported formats
    from PIL import Image
    print("Supported formats:", Image.registered_extensions())

    # Convert unsupported formats first
    from PIL import Image

    # Convert HEIC to JPEG (requires pillow-heif)
    try:
        from pillow_heif import register_heif_opener
        register_heif_opener()

        image = Image.open("photo.heic")
        image.save("photo.jpg", "JPEG")
    except ImportError:
        print("Install pillow-heif for HEIC support: pip install pillow-heif")

**Issue: Corrupted image files**

.. code-block:: text

    OSError: cannot identify image file

**Solutions:**

.. code-block:: python

    from PIL import Image
    import os

    def validate_image(image_path):
        """Validate image file integrity."""
        try:
            # Check file exists and has size
            if not os.path.exists(image_path):
                return False, "File does not exist"

            if os.path.getsize(image_path) == 0:
                return False, "File is empty"

            # Try to open with PIL
            with Image.open(image_path) as img:
                img.verify()  # Verify image integrity

            return True, "Valid image"

        except Exception as e:
            return False, f"Invalid image: {e}"

    # Usage
    is_valid, message = validate_image("suspicious_image.jpg")
    if is_valid:
        image = get_image("suspicious_image.jpg", framework="tkinter")
    else:
        print(f"Cannot load image: {message}")

Memory and Performance Issues
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Issue: Memory errors with large images**

.. code-block:: text

    MemoryError: Unable to allocate array

**Solutions:**

.. code-block:: python

    # Resize large images before processing
    from PIL import Image

    def load_large_image_safely(path, max_size=(2000, 2000)):
        """Load large image with size limit."""
        try:
            with Image.open(path) as img:
                # Check size
                if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
                    print(f"Resizing large image: {img.size} -> {max_size}")
                    img.thumbnail(max_size, Image.Resampling.LANCZOS)

                # Save to temporary file if needed
                import tempfile
                with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                    img.save(tmp.name, 'PNG')
                    return tmp.name
        except Exception as e:
            print(f"Error processing large image: {e}")
            return None

    # Use with GUI Image Studio
    temp_path = load_large_image_safely("huge_image.jpg")
    if temp_path:
        image = get_image(temp_path, framework="tkinter", size=(800, 600))
        os.unlink(temp_path)  # Clean up

**Issue: Slow performance with many images**

**Solutions:**

.. code-block:: python

    # Implement caching
    from functools import lru_cache

    @lru_cache(maxsize=100)
    def cached_get_image(image_path, framework, size):
        """Cached image loading."""
        return get_image(image_path, framework=framework, size=size)

    # Use appropriate sizes
    # Don't load 4K images for 64x64 display
    thumbnail = get_image("large_photo.jpg", framework="tkinter", size=(150, 150))

    # Process in batches
    def process_images_in_batches(image_list, batch_size=10):
        """Process images in smaller batches."""
        for i in range(0, len(image_list), batch_size):
            batch = image_list[i:i + batch_size]

            for image_path in batch:
                try:
                    processed = get_image(image_path, framework="tkinter")
                    # Process image...
                except Exception as e:
                    print(f"Error processing {image_path}: {e}")

            # Optional: garbage collection between batches
            import gc
            gc.collect()

GUI Framework Issues
--------------------

Tkinter Problems
~~~~~~~~~~~~~~~~

**Issue: Images not displaying in tkinter**

.. code-block:: text

    # Image loads but doesn't appear in GUI

**Solutions:**

.. code-block:: python

    import tkinter as tk
    from gui_image_studio import get_image

    class ImageApp:
        def __init__(self, root):
            self.root = root

            # Load image
            self.image = get_image("test.png", framework="tkinter")

            # Create label - MUST keep reference to image
            self.label = tk.Label(root, image=self.image)
            self.label.pack()

            # Keep reference to prevent garbage collection
            self.label.image = self.image  # Important!

    # Alternative: Store images in instance variable
    class BetterImageApp:
        def __init__(self, root):
            self.root = root
            self.images = {}  # Store all images here

            # Load and store image
            self.images['test'] = get_image("test.png", framework="tkinter")

            # Use stored image
            label = tk.Label(root, image=self.images['test'])
            label.pack()

**Issue: tkinter GUI freezes during image processing**

**Solutions:**

.. code-block:: python

    import tkinter as tk
    import threading
    from gui_image_studio import get_image

    class ResponsiveImageApp:
        def __init__(self, root):
            self.root = root
            self.setup_ui()

        def setup_ui(self):
            self.label = tk.Label(self.root, text="Loading...")
            self.label.pack()

            self.load_btn = tk.Button(
                self.root,
                text="Load Image",
                command=self.load_image_async
            )
            self.load_btn.pack()

        def load_image_async(self):
            """Load image in background thread."""
            self.load_btn.configure(state='disabled', text="Loading...")

            # Start background thread
            thread = threading.Thread(target=self.load_image_worker)
            thread.daemon = True
            thread.start()

        def load_image_worker(self):
            """Background image loading."""
            try:
                # Load image (this might take time)
                image = get_image("large_image.jpg", framework="tkinter", size=(400, 300))

                # Update GUI in main thread
                self.root.after(0, self.update_image, image)

            except Exception as e:
                self.root.after(0, self.handle_error, str(e))

        def update_image(self, image):
            """Update GUI with loaded image."""
            self.label.configure(image=image, text="")
            self.label.image = image  # Keep reference
            self.load_btn.configure(state='normal', text="Load Image")

        def handle_error(self, error_msg):
            """Handle loading errors."""
            self.label.configure(text=f"Error: {error_msg}")
            self.load_btn.configure(state='normal', text="Load Image")

CustomTkinter Problems
~~~~~~~~~~~~~~~~~~~~~~

**Issue: CustomTkinter images not updating with theme changes**

**Solutions:**

.. code-block:: python

    import customtkinter as ctk
    from gui_image_studio import get_image

    class ThemedApp:
        def __init__(self):
            ctk.set_appearance_mode("dark")

            self.root = ctk.CTk()
            self.current_theme = "dark"

            self.setup_ui()

        def setup_ui(self):
            # Load initial image
            self.update_images()

            # Image display
            self.image_label = ctk.CTkLabel(self.root, image=self.logo, text="")
            self.image_label.pack(pady=20)

            # Theme toggle
            self.theme_btn = ctk.CTkButton(
                self.root,
                text="Toggle Theme",
                command=self.toggle_theme
            )
            self.theme_btn.pack()

        def update_images(self):
            """Load images with current theme."""
            self.logo = get_image(
                "logo.png",
                framework="customtkinter",
                theme=self.current_theme,
                size=(100, 100)
            )

        def toggle_theme(self):
            """Toggle theme and update images."""
            # Change CustomTkinter theme
            if self.current_theme == "dark":
                self.current_theme = "light"
                ctk.set_appearance_mode("light")
            else:
                self.current_theme = "dark"
                ctk.set_appearance_mode("dark")

            # Reload images with new theme
            self.update_images()

            # Update UI
            self.image_label.configure(image=self.logo)

**Issue: CustomTkinter not found or import errors**

.. code-block:: text

    ModuleNotFoundError: No module named 'customtkinter'

**Solutions:**

.. code-block:: bash

    # Install CustomTkinter
    pip install customtkinter

    # Check version compatibility
    pip show customtkinter

    # If using older Python version, try specific version
    pip install "customtkinter>=5.0.0,<6.0.0"

.. code-block:: python

    # Graceful fallback to tkinter
    try:
        import customtkinter as ctk
        CUSTOMTKINTER_AVAILABLE = True
    except ImportError:
        import tkinter as tk
        CUSTOMTKINTER_AVAILABLE = False
        print("CustomTkinter not available, using tkinter")

    # Use appropriate framework
    framework = "customtkinter" if CUSTOMTKINTER_AVAILABLE else "tkinter"
    image = get_image("test.png", framework=framework)

Command Line Issues
-------------------

CLI Tools Not Found
~~~~~~~~~~~~~~~~~~~~

**Issue: Command not found**

.. code-block:: text

    bash: gui-image-studio-designer: command not found

**Solutions:**

.. code-block:: bash

    # Check if GUI Image Studio is installed
    pip show gui-image-studio

    # Check Python scripts directory in PATH
    python -m site --user-base
    # Add Scripts directory to PATH if needed

    # Reinstall with --force-reinstall
    pip install --force-reinstall gui-image-studio

    # Use Python module syntax as alternative
    python -m gui_image_studio
    python -c "from gui_image_studio import launch_designer; launch_designer()"

**Issue: Permission denied on Linux/macOS**

.. code-block:: text

    bash: /usr/local/bin/gui-image-studio-designer: Permission denied

**Solutions:**

.. code-block:: bash

    # Check permissions
    ls -la /usr/local/bin/gui-image-studio-*

    # Fix permissions
    chmod +x /usr/local/bin/gui-image-studio-*

    # Or reinstall with user flag
    pip install --user --force-reinstall gui-image-studio

CLI Processing Errors
~~~~~~~~~~~~~~~~~~~~~~

**Issue: Generation fails silently**

**Solutions:**

.. code-block:: bash

    # Enable verbose output
    gui-image-studio-generate --folder images/ --verbose

    # Check for hidden error messages
    gui-image-studio-generate --folder images/ 2>&1 | tee generation.log

    # Validate input folder
    ls -la images/
    find images/ -name "*.png" -o -name "*.jpg" | head -5

**Issue: Output file not created**

**Solutions:**

.. code-block:: bash

    # Check output directory permissions
    ls -ld output_directory/

    # Use absolute paths
    gui-image-studio-generate \
      --folder "$(pwd)/images" \
      --output "$(pwd)/resources.py"

    # Check disk space
    df -h

Development Issues
------------------

Import and Module Issues
~~~~~~~~~~~~~~~~~~~~~~~~

**Issue: Cannot import gui_image_studio**

.. code-block:: text

    ImportError: No module named 'gui_image_studio'

**Solutions:**

.. code-block:: python

    # Check installation
    import sys
    print(sys.path)

    # Try explicit import
    try:
        import gui_image_studio
        print(f"GUI Image Studio version: {gui_image_studio.__version__}")
    except ImportError as e:
        print(f"Import error: {e}")

    # Check if installed in different environment
    import subprocess
    result = subprocess.run([sys.executable, "-m", "pip", "show", "gui-image-studio"],
                          capture_output=True, text=True)
    print(result.stdout)

**Issue: Version conflicts**

.. code-block:: text

    AttributeError: module 'gui_image_studio' has no attribute 'get_image'

**Solutions:**

.. code-block:: bash

    # Check installed version
    pip show gui-image-studio

    # Update to latest version
    pip install --upgrade gui-image-studio

    # Check for multiple installations
    pip list | grep gui-image-studio

    # Clean install
    pip uninstall gui-image-studio
    pip install gui-image-studio

API Usage Issues
~~~~~~~~~~~~~~~~

**Issue: Unexpected parameter errors**

.. code-block:: text

    TypeError: get_image() got an unexpected keyword argument 'invalid_param'

**Solutions:**

.. code-block:: python

    # Check valid parameters
    from gui_image_studio import get_image
    help(get_image)

    # Use only documented parameters
    valid_params = {
        'framework': 'tkinter',
        'size': (64, 64),
        'theme': 'default',
        'rotate': 0,
        'grayscale': False,
        'tint_color': (255, 0, 0),
        'tint_intensity': 0.3,
        'contrast': 1.2,
        'saturation': 1.1,
        'transparency': 1.0,
        'animated': False,
        'frame_delay': 100
    }

    image = get_image("test.png", **valid_params)

**Issue: Type errors with parameters**

.. code-block:: text

    TypeError: 'str' object cannot be interpreted as an integer

**Solutions:**

.. code-block:: python

    # Ensure correct parameter types

    # Size must be tuple of integers
    image = get_image("test.png", framework="tkinter", size=(64, 64))  # Correct
    # image = get_image("test.png", framework="tkinter", size="64x64")  # Wrong

    # Tint color must be tuple of integers
    image = get_image("test.png", framework="tkinter", tint_color=(255, 0, 0))  # Correct
    # image = get_image("test.png", framework="tkinter", tint_color="#FF0000")  # Wrong

    # Numeric parameters must be numbers
    image = get_image("test.png", framework="tkinter", contrast=1.2)  # Correct
    # image = get_image("test.png", framework="tkinter", contrast="1.2")  # Wrong

Platform-Specific Issues
-------------------------

Windows Issues
~~~~~~~~~~~~~~

**Issue: Path separator problems**

.. code-block:: text

    FileNotFoundError: [Errno 2] No such file or directory: 'images\\test.png'

**Solutions:**

.. code-block:: python

    import os
    from gui_image_studio import get_image

    # Use os.path.join for cross-platform paths
    image_path = os.path.join("images", "test.png")
    image = get_image(image_path, framework="tkinter")

    # Or use pathlib (Python 3.4+)
    from pathlib import Path
    image_path = Path("images") / "test.png"
    image = get_image(str(image_path), framework="tkinter")

    # Use forward slashes (works on Windows too)
    image = get_image("images/test.png", framework="tkinter")

**Issue: Windows Defender blocking execution**

**Solutions:**

1. Add Python and pip to Windows Defender exclusions
2. Run Command Prompt as Administrator
3. Use Windows Store Python if available

.. code-block:: batch

    REM Run as Administrator
    powershell -Command "Start-Process cmd -Verb RunAs"

macOS Issues
~~~~~~~~~~~~

**Issue: Permission errors on macOS**

.. code-block:: text

    PermissionError: [Errno 1] Operation not permitted

**Solutions:**

.. code-block:: bash

    # Use Homebrew Python instead of system Python
    brew install python
    /opt/homebrew/bin/pip3 install gui-image-studio

    # Or use user installation
    pip3 install --user gui-image-studio

    # Add user bin to PATH
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
    source ~/.zshrc

**Issue: GUI not appearing on macOS**

**Solutions:**

.. code-block:: bash

    # Install tkinter if missing
    brew install python-tk

    # For GUI apps, may need to run from terminal
    python3 -c "from gui_image_studio import launch_designer; launch_designer()"

Linux Issues
~~~~~~~~~~~~

**Issue: Display issues on headless servers**

.. code-block:: text

    _tkinter.TclError: no display name and no $DISPLAY environment variable

**Solutions:**

.. code-block:: bash

    # Install virtual display
    sudo apt-get install xvfb

    # Set up virtual display
    export DISPLAY=:99
    Xvfb :99 -screen 0 1024x768x24 &

    # Run GUI Image Studio
    gui-image-studio-designer

    # Or use in scripts
    xvfb-run -a gui-image-studio-designer

**Issue: Missing system libraries**

.. code-block:: text

    ImportError: libSM.so.6: cannot open shared object file

**Solutions:**

.. code-block:: bash

    # Install missing libraries
    sudo apt-get install libsm6 libxext6 libxrender-dev libglib2.0-0

    # For CentOS/RHEL
    sudo yum install libSM libXext libXrender glib2

Debugging and Diagnostics
-------------------------

Diagnostic Script
~~~~~~~~~~~~~~~~~

Create a diagnostic script to check your installation:

.. code-block:: python

    #!/usr/bin/env python3
    """
    GUI Image Studio diagnostic script
    """

    import sys
    import os
    import platform
    import subprocess

    def check_python_version():
        """Check Python version."""
        version = sys.version_info
        print(f"Python version: {version.major}.{version.minor}.{version.micro}")

        if version < (3, 8):
            print("❌ Python 3.8+ required")
            return False
        else:
            print("✅ Python version OK")
            return True

    def check_gui_image_studio():
        """Check GUI Image Studio installation."""
        try:
            import gui_image_studio
            print(f"✅ GUI Image Studio installed: {gui_image_studio.__version__}")
            return True
        except ImportError as e:
            print(f"❌ GUI Image Studio not found: {e}")
            return False

    def check_dependencies():
        """Check required dependencies."""
        dependencies = {
            'PIL': 'Pillow',
            'tkinter': 'tkinter'
        }

        all_ok = True

        for module, package in dependencies.items():
            try:
                __import__(module)
                print(f"✅ {package} available")
            except ImportError:
                print(f"❌ {package} missing")
                all_ok = False

        # Check optional dependencies
        try:
            import customtkinter
            print(f"✅ CustomTkinter available: {customtkinter.__version__}")
        except ImportError:
            print("⚠️  CustomTkinter not available (optional)")

        return all_ok

    def check_cli_tools():
        """Check CLI tools."""
        tools = [
            'gui-image-studio-designer',
            'gui-image-studio-generate',
            'gui-image-studio-create-samples'
        ]

        for tool in tools:
            try:
                result = subprocess.run([tool, '--version'],
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    print(f"✅ {tool} available")
                else:
                    print(f"❌ {tool} error: {result.stderr}")
            except (subprocess.TimeoutExpired, FileNotFoundError):
                print(f"❌ {tool} not found")

    def check_image_loading():
        """Test basic image loading."""
        try:
            from gui_image_studio import create_sample_images, get_image
            import tempfile

            # Create temporary directory
            with tempfile.TemporaryDirectory() as temp_dir:
                # Create sample images
                create_sample_images(temp_dir)

                # Try to load sample
                sample_path = os.path.join(temp_dir, "sample_icon.png")
                if os.path.exists(sample_path):
                    image = get_image(sample_path, framework="tkinter")
                    print("✅ Image loading test passed")
                    return True
                else:
                    print("❌ Sample image not created")
                    return False

        except Exception as e:
            print(f"❌ Image loading test failed: {e}")
            return False

    def main():
        """Run all diagnostic checks."""
        print("GUI Image Studio Diagnostic Report")
        print("=" * 40)

        print(f"Platform: {platform.platform()}")
        print(f"Architecture: {platform.architecture()}")
        print()

        checks = [
            ("Python Version", check_python_version),
            ("GUI Image Studio", check_gui_image_studio),
            ("Dependencies", check_dependencies),
            ("CLI Tools", check_cli_tools),
            ("Image Loading", check_image_loading)
        ]

        results = []

        for name, check_func in checks:
            print(f"Checking {name}...")
            try:
                result = check_func()
                results.append(result)
            except Exception as e:
                print(f"❌ {name} check failed: {e}")
                results.append(False)
            print()

        # Summary
        passed = sum(results)
        total = len(results)

        print("Summary")
        print("-" * 20)
        print(f"Checks passed: {passed}/{total}")

        if passed == total:
            print("✅ All checks passed! GUI Image Studio should work correctly.")
        else:
            print("❌ Some checks failed. Please address the issues above.")

        return passed == total

    if __name__ == "__main__":
        success = main()
        sys.exit(0 if success else 1)

Save this as `diagnose.py` and run:

.. code-block:: bash

    python diagnose.py

Getting Help
------------

When to Seek Help
~~~~~~~~~~~~~~~~~

Seek help when you encounter:

1. **Installation failures** after trying standard solutions
2. **Consistent crashes** or unexpected behavior
3. **Performance issues** that affect usability
4. **Missing features** you expected to find

How to Report Issues
~~~~~~~~~~~~~~~~~~~~

When reporting issues, include:

1. **System Information:**
   - Operating system and version
   - Python version
   - GUI Image Studio version

2. **Complete Error Messages:**
   - Full traceback
   - Command that caused the error
   - Any relevant log output

3. **Steps to Reproduce:**
   - Minimal code example
   - Input files (if relevant)
   - Expected vs actual behavior

4. **Environment Details:**
   - Virtual environment info
   - Other installed packages
   - Any custom configurations

**Example Issue Report:**

.. code-block:: text

    **System Information:**
    - OS: Ubuntu 20.04 LTS
    - Python: 3.8.10
    - GUI Image Studio: 1.1.0

    **Issue:**
    get_image() fails with large JPEG files

    **Error Message:**
    ```
    MemoryError: Unable to allocate 1.2 GiB for an array with shape (10000, 8000, 4) and data type uint8
    ```

    **Steps to Reproduce:**
    ```python
    from gui_image_studio import get_image
    image = get_image("large_photo.jpg", framework="tkinter", size=(800, 600))
    ```

    **Additional Info:**
    - Image file: 25MB JPEG, 10000x8000 pixels
    - Available RAM: 8GB
    - Works fine with smaller images

Resources for Help
~~~~~~~~~~~~~~~~~~

1. **Documentation:** https://stntg.github.io/gui-image-studio/
2. **GitHub Issues:** https://github.com/stntg/gui-image-studio/issues
3. **GitHub Discussions:** https://github.com/stntg/gui-image-studio/discussions
4. **Stack Overflow:** Tag questions with `gui-image-studio`

Self-Help Checklist
~~~~~~~~~~~~~~~~~~~~

Before seeking help, try:

- [ ] Update to the latest version
- [ ] Check the documentation
- [ ] Search existing issues
- [ ] Run the diagnostic script
- [ ] Try with a minimal example
- [ ] Test in a clean environment

Next Steps
----------

If you've resolved your issues:

1. **Continue Learning:** :doc:`../examples/index`
2. **Build Something:** :doc:`gui_development`
3. **Share Your Experience:** Help others in the community
4. **Contribute:** Consider contributing improvements or documentation
