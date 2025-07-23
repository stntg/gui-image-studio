Command Line Tools
==================

GUI Image Studio provides powerful command-line tools for automation, batch processing, and integration with build systems. This guide covers all available CLI commands and their usage patterns.

Overview of CLI Tools
----------------------

GUI Image Studio includes three main command-line tools:

- **gui-image-studio-designer**: Launch the visual image designer
- **gui-image-studio-generate**: Generate embedded image resources from folders
- **gui-image-studio-create-samples**: Create sample images for testing

All tools are automatically installed and available in your PATH when you install GUI Image Studio.

gui-image-studio-designer
--------------------------

Launch the visual image designer application.

Basic Usage
~~~~~~~~~~~

.. code-block:: bash

    # Launch the designer
    gui-image-studio-designer

    # Launch with specific file
    gui-image-studio-designer --file image.png

    # Launch in fullscreen mode
    gui-image-studio-designer --fullscreen

Command Options
~~~~~~~~~~~~~~~

.. code-block:: text

    gui-image-studio-designer [OPTIONS] [FILE]

    Options:
      --file PATH         Open specific image file on startup
      --new              Start with new blank image
      --fullscreen       Launch in fullscreen mode
      --theme THEME      Set initial theme (light/dark/system)
      --size WIDTHxHEIGHT Set initial window size
      --help             Show help message
      --version          Show version information

Examples
~~~~~~~~

.. code-block:: bash

    # Open specific image
    gui-image-studio-designer --file photos/vacation.jpg

    # Start with new image in fullscreen
    gui-image-studio-designer --new --fullscreen

    # Set window size and theme
    gui-image-studio-designer --size 1200x800 --theme dark

    # Show version
    gui-image-studio-designer --version

Integration with File Managers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can integrate the designer with your file manager for easy access:

**Windows (Registry):**

.. code-block:: batch

    # Add "Edit with GUI Image Studio" to context menu
    reg add "HKEY_CLASSES_ROOT\*\shell\EditWithGUIImageStudio" /ve /d "Edit with GUI Image Studio"
    reg add "HKEY_CLASSES_ROOT\*\shell\EditWithGUIImageStudio\command" /ve /d "gui-image-studio-designer --file \"%1\""

**Linux (Desktop Entry):**

.. code-block:: ini

    # ~/.local/share/applications/gui-image-studio.desktop
    [Desktop Entry]
    Name=GUI Image Studio
    Comment=Visual image editor and processor
    Exec=gui-image-studio-designer %f
    Icon=gui-image-studio
    Terminal=false
    Type=Application
    Categories=Graphics;Photography;
    MimeType=image/png;image/jpeg;image/gif;image/bmp;

**macOS (Automator Service):**

Create an Automator service that runs:

.. code-block:: bash

    gui-image-studio-designer --file "$@"

gui-image-studio-generate
--------------------------

Generate embedded Python modules from image folders.

Basic Usage
~~~~~~~~~~~

.. code-block:: bash

    # Generate from folder
    gui-image-studio-generate --folder images/

    # Specify output file
    gui-image-studio-generate --folder icons/ --output resources.py

    # Set compression quality
    gui-image-studio-generate --folder photos/ --quality 75

Command Options
~~~~~~~~~~~~~~~

.. code-block:: text

    gui-image-studio-generate [OPTIONS]

    Required:
      --folder PATH       Input folder containing images

    Optional:
      --output FILE       Output Python file (default: embedded_images.py)
      --quality INT       Compression quality 1-100 (default: 85)
      --recursive         Process subfolders recursively
      --formats LIST      Include only specific formats (comma-separated)
      --exclude PATTERN   Exclude files matching pattern
      --prefix STRING     Add prefix to image names
      --module-name NAME  Set module name in generated file
      --help             Show help message
      --version          Show version information

Examples
~~~~~~~~

.. code-block:: bash

    # Basic generation
    gui-image-studio-generate --folder assets/images/

    # High-quality icons
    gui-image-studio-generate \
      --folder icons/ \
      --output src/icons.py \
      --quality 95

    # Recursive processing with format filter
    gui-image-studio-generate \
      --folder project/assets/ \
      --output resources/all_images.py \
      --recursive \
      --formats png,jpg,gif

    # Exclude temporary files
    gui-image-studio-generate \
      --folder images/ \
      --exclude "*.tmp,*_backup.*,*.DS_Store"

    # Add prefix to image names
    gui-image-studio-generate \
      --folder ui_icons/ \
      --output ui_resources.py \
      --prefix ui_

Advanced Usage Patterns
~~~~~~~~~~~~~~~~~~~~~~~~

**Build System Integration:**

.. code-block:: bash

    # Makefile target
    generate-resources:
        gui-image-studio-generate \
          --folder src/assets/ \
          --output src/resources.py \
          --quality 90 \
          --recursive

    # Package.json script
    {
      "scripts": {
        "build-images": "gui-image-studio-generate --folder assets/ --output src/images.py"
      }
    }

**Batch Processing Multiple Folders:**

.. code-block:: bash

    #!/bin/bash
    # generate_all_resources.sh

    # Generate icons
    gui-image-studio-generate \
      --folder assets/icons/ \
      --output src/resources/icons.py \
      --quality 95

    # Generate images
    gui-image-studio-generate \
      --folder assets/images/ \
      --output src/resources/images.py \
      --quality 80

    # Generate backgrounds
    gui-image-studio-generate \
      --folder assets/backgrounds/ \
      --output src/resources/backgrounds.py \
      --quality 70

**CI/CD Integration:**

.. code-block:: yaml

    # GitHub Actions
    name: Generate Image Resources
    on:
      push:
        paths:
          - 'assets/**'

    jobs:
      generate:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v4
          - name: Setup Python
            uses: actions/setup-python@v4
            with:
              python-version: '3.10'
          - name: Install GUI Image Studio
            run: pip install gui-image-studio
          - name: Generate resources
            run: |
              gui-image-studio-generate \
                --folder assets/ \
                --output src/resources.py \
                --recursive \
                --quality 85
          - name: Commit changes
            run: |
              git config --local user.email "action@github.com"
              git config --local user.name "GitHub Action"
              git add src/resources.py
              git commit -m "Update image resources" || exit 0
              git push

gui-image-studio-create-samples
--------------------------------

Create sample images for testing and development.

Basic Usage
~~~~~~~~~~~

.. code-block:: bash

    # Create samples in default location
    gui-image-studio-create-samples

    # Create in specific directory
    gui-image-studio-create-samples --output test_images/

    # Create specific number of samples
    gui-image-studio-create-samples --count 20

Command Options
~~~~~~~~~~~~~~~

.. code-block:: text

    gui-image-studio-create-samples [OPTIONS]

    Optional:
      --output DIR        Output directory (default: sample_images)
      --count INT         Number of samples to create (default: 10)
      --size WIDTHxHEIGHT Sample image size (default: 64x64)
      --formats LIST      Image formats to create (default: png,jpg)
      --animated          Include animated GIF samples
      --prefix STRING     Filename prefix (default: sample_)
      --help             Show help message
      --version          Show version information

Examples
~~~~~~~~

.. code-block:: bash

    # Create default samples
    gui-image-studio-create-samples

    # Create large samples
    gui-image-studio-create-samples \
      --output large_samples/ \
      --size 256x256 \
      --count 15

    # Create samples with animation
    gui-image-studio-create-samples \
      --output test_data/ \
      --animated \
      --formats png,jpg,gif

    # Create samples with custom prefix
    gui-image-studio-create-samples \
      --output icons/ \
      --prefix icon_ \
      --size 32x32

Use Cases
~~~~~~~~~

**Testing and Development:**

.. code-block:: bash

    # Create test data for unit tests
    gui-image-studio-create-samples --output tests/fixtures/

    # Create samples for UI development
    gui-image-studio-create-samples \
      --output ui_mockups/ \
      --size 128x128 \
      --count 25

**Documentation and Examples:**

.. code-block:: bash

    # Create samples for documentation
    gui-image-studio-create-samples \
      --output docs/examples/ \
      --formats png \
      --size 64x64

**Performance Testing:**

.. code-block:: bash

    # Create large dataset for performance testing
    gui-image-studio-create-samples \
      --output perf_test/ \
      --count 1000 \
      --size 512x512

Automation and Scripting
-------------------------

Shell Scripts
~~~~~~~~~~~~~

**Complete Build Script:**

.. code-block:: bash

    #!/bin/bash
    # build_resources.sh - Complete resource build script

    set -e  # Exit on error

    echo "Building GUI Image Studio Resources..."

    # Configuration
    ASSETS_DIR="assets"
    OUTPUT_DIR="src/resources"
    TEMP_DIR="temp_build"

    # Create directories
    mkdir -p "$OUTPUT_DIR"
    mkdir -p "$TEMP_DIR"

    # Function to generate resources
    generate_resources() {
        local folder=$1
        local output=$2
        local quality=${3:-85}

        echo "Generating $output from $folder..."

        gui-image-studio-generate \
            --folder "$ASSETS_DIR/$folder" \
            --output "$OUTPUT_DIR/$output" \
            --quality "$quality" \
            --recursive

        if [ $? -eq 0 ]; then
            echo "✓ Generated $output"
        else
            echo "✗ Failed to generate $output"
            exit 1
        fi
    }

    # Generate different resource types
    generate_resources "icons" "icons.py" 95
    generate_resources "images" "images.py" 80
    generate_resources "backgrounds" "backgrounds.py" 70

    # Create test samples if needed
    if [ "$1" = "--with-samples" ]; then
        echo "Creating test samples..."
        gui-image-studio-create-samples \
            --output "$TEMP_DIR/samples" \
            --count 10
        echo "✓ Created test samples"
    fi

    # Cleanup
    rm -rf "$TEMP_DIR"

    echo "✓ Resource build complete!"

**Windows Batch Script:**

.. code-block:: batch

    @echo off
    REM build_resources.bat - Windows resource build script

    echo Building GUI Image Studio Resources...

    REM Configuration
    set ASSETS_DIR=assets
    set OUTPUT_DIR=src\resources
    set QUALITY=85

    REM Create output directory
    if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"

    REM Generate icons
    echo Generating icons...
    gui-image-studio-generate ^
        --folder "%ASSETS_DIR%\icons" ^
        --output "%OUTPUT_DIR%\icons.py" ^
        --quality 95

    if errorlevel 1 (
        echo Failed to generate icons
        exit /b 1
    )

    REM Generate images
    echo Generating images...
    gui-image-studio-generate ^
        --folder "%ASSETS_DIR%\images" ^
        --output "%OUTPUT_DIR%\images.py" ^
        --quality %QUALITY%

    if errorlevel 1 (
        echo Failed to generate images
        exit /b 1
    )

    echo Resource build complete!

Python Automation Scripts
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Advanced Build Script:**

.. code-block:: python

    #!/usr/bin/env python3
    """
    Advanced build script for GUI Image Studio resources.
    """

    import os
    import sys
    import subprocess
    import argparse
    from pathlib import Path

    class ResourceBuilder:
        def __init__(self, config):
            self.config = config
            self.assets_dir = Path(config['assets_dir'])
            self.output_dir = Path(config['output_dir'])

        def ensure_directories(self):
            """Create necessary directories."""
            self.output_dir.mkdir(parents=True, exist_ok=True)

        def run_command(self, cmd):
            """Run command and handle errors."""
            try:
                result = subprocess.run(
                    cmd,
                    shell=True,
                    check=True,
                    capture_output=True,
                    text=True
                )
                return True, result.stdout
            except subprocess.CalledProcessError as e:
                return False, e.stderr

        def generate_resources(self, folder, output_file, quality=85):
            """Generate resources from folder."""

            input_path = self.assets_dir / folder
            output_path = self.output_dir / output_file

            if not input_path.exists():
                print(f"Warning: Input folder {input_path} does not exist")
                return False

            cmd = [
                "gui-image-studio-generate",
                "--folder", str(input_path),
                "--output", str(output_path),
                "--quality", str(quality),
                "--recursive"
            ]

            print(f"Generating {output_file} from {folder}...")
            success, output = self.run_command(" ".join(cmd))

            if success:
                print(f"✓ Generated {output_file}")
                return True
            else:
                print(f"✗ Failed to generate {output_file}: {output}")
                return False

        def create_samples(self, output_dir, count=10):
            """Create sample images."""

            sample_path = Path(output_dir)
            sample_path.mkdir(parents=True, exist_ok=True)

            cmd = [
                "gui-image-studio-create-samples",
                "--output", str(sample_path),
                "--count", str(count)
            ]

            print(f"Creating {count} sample images...")
            success, output = self.run_command(" ".join(cmd))

            if success:
                print(f"✓ Created samples in {sample_path}")
                return True
            else:
                print(f"✗ Failed to create samples: {output}")
                return False

        def build_all(self):
            """Build all resources."""

            self.ensure_directories()

            # Resource configurations
            resources = [
                ("icons", "icons.py", 95),
                ("images", "images.py", 80),
                ("backgrounds", "backgrounds.py", 70),
                ("ui", "ui_elements.py", 90)
            ]

            success_count = 0

            for folder, output_file, quality in resources:
                if self.generate_resources(folder, output_file, quality):
                    success_count += 1

            print(f"\nBuild complete: {success_count}/{len(resources)} successful")

            return success_count == len(resources)

    def main():
        parser = argparse.ArgumentParser(description="Build GUI Image Studio resources")
        parser.add_argument("--assets", default="assets", help="Assets directory")
        parser.add_argument("--output", default="src/resources", help="Output directory")
        parser.add_argument("--samples", action="store_true", help="Create sample images")
        parser.add_argument("--config", help="Configuration file")

        args = parser.parse_args()

        # Configuration
        config = {
            'assets_dir': args.assets,
            'output_dir': args.output
        }

        # Load config file if provided
        if args.config and os.path.exists(args.config):
            import json
            with open(args.config) as f:
                config.update(json.load(f))

        # Build resources
        builder = ResourceBuilder(config)

        if builder.build_all():
            print("✓ All resources built successfully")

            # Create samples if requested
            if args.samples:
                builder.create_samples("temp/samples")

            sys.exit(0)
        else:
            print("✗ Some resources failed to build")
            sys.exit(1)

    if __name__ == "__main__":
        main()

Configuration Files
~~~~~~~~~~~~~~~~~~~~

**JSON Configuration:**

.. code-block:: json

    {
      "assets_dir": "assets",
      "output_dir": "src/resources",
      "resources": [
        {
          "folder": "icons",
          "output": "icons.py",
          "quality": 95,
          "formats": ["png", "svg"]
        },
        {
          "folder": "images",
          "output": "images.py",
          "quality": 80,
          "exclude": ["*.tmp", "*_backup.*"]
        },
        {
          "folder": "backgrounds",
          "output": "backgrounds.py",
          "quality": 70,
          "recursive": true
        }
      ],
      "samples": {
        "enabled": true,
        "output": "test_samples",
        "count": 15,
        "size": "64x64"
      }
    }

**YAML Configuration:**

.. code-block:: yaml

    # gui-image-studio.yml
    assets_dir: assets
    output_dir: src/resources

    resources:
      - folder: icons
        output: icons.py
        quality: 95
        formats: [png, svg]

      - folder: images
        output: images.py
        quality: 80
        exclude: ["*.tmp", "*_backup.*"]

      - folder: backgrounds
        output: backgrounds.py
        quality: 70
        recursive: true

    samples:
      enabled: true
      output: test_samples
      count: 15
      size: "64x64"

IDE Integration
---------------

Visual Studio Code
~~~~~~~~~~~~~~~~~~

**Tasks Configuration (.vscode/tasks.json):**

.. code-block:: json

    {
      "version": "2.0.0",
      "tasks": [
        {
          "label": "Generate Image Resources",
          "type": "shell",
          "command": "gui-image-studio-generate",
          "args": [
            "--folder", "assets/",
            "--output", "src/resources.py",
            "--quality", "85"
          ],
          "group": "build",
          "presentation": {
            "echo": true,
            "reveal": "always",
            "focus": false,
            "panel": "shared"
          },
          "problemMatcher": []
        },
        {
          "label": "Create Sample Images",
          "type": "shell",
          "command": "gui-image-studio-create-samples",
          "args": [
            "--output", "test_samples/",
            "--count", "10"
          ],
          "group": "test"
        },
        {
          "label": "Launch Designer",
          "type": "shell",
          "command": "gui-image-studio-designer",
          "args": ["${file}"],
          "group": "build"
        }
      ]
    }

**Keyboard Shortcuts (.vscode/keybindings.json):**

.. code-block:: json

    [
      {
        "key": "ctrl+shift+g",
        "command": "workbench.action.tasks.runTask",
        "args": "Generate Image Resources"
      },
      {
        "key": "ctrl+shift+d",
        "command": "workbench.action.tasks.runTask",
        "args": "Launch Designer"
      }
    ]

PyCharm Integration
~~~~~~~~~~~~~~~~~~~

**External Tools Configuration:**

1. Go to File → Settings → Tools → External Tools
2. Add new tool:

.. code-block:: text

    Name: Generate Image Resources
    Program: gui-image-studio-generate
    Arguments: --folder assets/ --output src/resources.py
    Working directory: $ProjectFileDir$

3. Add keyboard shortcut in Keymap settings

Docker Integration
------------------

Dockerfile for CLI Tools
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: dockerfile

    FROM python:3.10-slim

    # Install system dependencies
    RUN apt-get update && apt-get install -y \
        python3-tk \
        && rm -rf /var/lib/apt/lists/*

    # Install GUI Image Studio
    RUN pip install gui-image-studio

    # Set working directory
    WORKDIR /workspace

    # Default command
    CMD ["gui-image-studio-generate", "--help"]

**Usage:**

.. code-block:: bash

    # Build image
    docker build -t gui-image-studio-cli .

    # Generate resources
    docker run -v $(pwd):/workspace gui-image-studio-cli \
        gui-image-studio-generate --folder assets/ --output resources.py

    # Create samples
    docker run -v $(pwd):/workspace gui-image-studio-cli \
        gui-image-studio-create-samples --output samples/

Docker Compose for Development
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    version: '3.8'
    services:
      gui-image-studio:
        build: .
        volumes:
          - ./assets:/workspace/assets
          - ./src:/workspace/src
        environment:
          - DISPLAY=${DISPLAY}
        command: >
          bash -c "
            gui-image-studio-generate --folder assets/ --output src/resources.py &&
            gui-image-studio-create-samples --output test_samples/
          "

Troubleshooting CLI Tools
-------------------------

Common Issues
~~~~~~~~~~~~~

**Command Not Found:**

.. code-block:: bash

    # Check if GUI Image Studio is installed
    pip show gui-image-studio

    # Reinstall if necessary
    pip install --force-reinstall gui-image-studio

    # Check PATH
    echo $PATH

**Permission Errors:**

.. code-block:: bash

    # Linux/macOS: Check file permissions
    ls -la /usr/local/bin/gui-image-studio-*

    # Windows: Run as administrator
    # Right-click Command Prompt → "Run as administrator"

**Import Errors:**

.. code-block:: bash

    # Check Python environment
    python -c "import gui_image_studio; print('OK')"

    # Check dependencies
    pip install --upgrade Pillow

**Display Issues (Linux):**

.. code-block:: bash

    # For headless systems
    export DISPLAY=:99
    Xvfb :99 -screen 0 1024x768x24 &

    # Install X11 forwarding for SSH
    ssh -X user@server

Debugging and Logging
~~~~~~~~~~~~~~~~~~~~~

**Enable Verbose Output:**

.. code-block:: bash

    # Most CLI tools support verbose mode
    gui-image-studio-generate --folder assets/ --verbose

    # Or set environment variable
    export GUI_IMAGE_STUDIO_DEBUG=1
    gui-image-studio-generate --folder assets/

**Log Files:**

.. code-block:: bash

    # Redirect output to log file
    gui-image-studio-generate --folder assets/ > build.log 2>&1

    # View logs
    tail -f build.log

Best Practices
--------------

CLI Usage Guidelines
~~~~~~~~~~~~~~~~~~~~

1. **Use absolute paths** when possible
2. **Validate inputs** before processing
3. **Handle errors gracefully** in scripts
4. **Use configuration files** for complex setups
5. **Document your build processes**

.. code-block:: bash

    # Good: Explicit and safe
    gui-image-studio-generate \
      --folder "$(pwd)/assets/icons" \
      --output "$(pwd)/src/resources/icons.py" \
      --quality 95

    # Check for errors
    if [ $? -ne 0 ]; then
        echo "Failed to generate resources"
        exit 1
    fi

Performance Optimization
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    # Process smaller batches for large folders
    find assets/ -name "*.png" | head -100 | xargs -I {} \
        gui-image-studio-generate --folder {} --output batch1.py

    # Use parallel processing
    parallel gui-image-studio-generate --folder {} --output {/.}.py ::: assets/*/

Security Considerations
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    # Validate input paths
    if [[ "$INPUT_FOLDER" =~ ^[a-zA-Z0-9/_-]+$ ]]; then
        gui-image-studio-generate --folder "$INPUT_FOLDER"
    else
        echo "Invalid folder path"
        exit 1
    fi

    # Use temporary directories safely
    TEMP_DIR=$(mktemp -d)
    trap "rm -rf $TEMP_DIR" EXIT

Next Steps
----------

Now that you understand the command-line tools:

1. **Learn Scripting**: :doc:`scripting`
2. **Explore GUI Development**: :doc:`gui_development`
3. **Try Advanced Examples**: :doc:`../examples/index`
4. **Integrate with Your Workflow**: Start automating your image processing tasks!
