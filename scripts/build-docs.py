#!/usr/bin/env python3
"""
Documentation build script for GUI Image Studio.

This script provides a convenient way to build and serve documentation locally.
"""

import os
import sys
import subprocess
import argparse
import webbrowser
import shutil
from pathlib import Path


def find_executable(name):
    """Find the full path to an executable, handling Windows .exe extension."""
    # First try to find the executable as-is
    path = shutil.which(name)
    if path:
        return path

    # On Windows, try with .exe extension
    if sys.platform == "win32" and not name.endswith(".exe"):
        path = shutil.which(name + ".exe")
        if path:
            return path

    # Return the original name if not found (will likely fail, but with better error)
    return name


def get_make_command():
    """Get the appropriate make command for the platform."""
    # On Windows, try to find make alternatives
    if sys.platform == "win32":
        # Try common Windows make alternatives
        for make_cmd in ["make", "mingw32-make", "nmake"]:
            if shutil.which(make_cmd):
                return make_cmd
        # If no make found, suggest using sphinx-build directly
        return None
    else:
        # On Unix-like systems, use make
        return find_executable("make")


def run_command(cmd, cwd=None, check=True):
    """Run a command and return the result."""
    # Resolve executable path for the first command
    if cmd and isinstance(cmd, list):
        cmd = cmd.copy()  # Don't modify the original list
        cmd[0] = find_executable(cmd[0])

    print(f"Running: {' '.join(cmd)}")
    try:
        result = subprocess.run(
            cmd, cwd=cwd, check=check, capture_output=True, text=True
        )
        if result.stdout:
            print(result.stdout)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        if check:
            sys.exit(1)
        return e


def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import sphinx

        print(f"✅ Sphinx {sphinx.__version__} found")
    except ImportError:
        print(
            "❌ Sphinx not found. Install with: pip install -r docs/requirements-docs.txt"
        )
        return False

    # Check if the package is installed
    try:
        import gui_image_studio

        print("✅ GUI Image Studio package found")
    except ImportError:
        print("⚠️ GUI Image Studio package not found. Install with: pip install -e .")
        print("   (This is needed for API documentation generation)")

    return True


def create_sample_images():
    """Create sample images for documentation examples."""
    try:
        from gui_image_studio.sample_creator import SampleCreator

        sample_dir = Path("sample_images")
        if sample_dir.exists() and any(sample_dir.iterdir()):
            print("✅ Sample images already exist")
            return True

        print("📸 Creating sample images...")
        creator = SampleCreator(str(sample_dir), count=3)
        creator.create_all_samples()
        print("✅ Sample images created")
        return True

    except Exception as e:
        print(f"⚠️ Could not create sample images: {e}")
        # Create minimal directory structure
        sample_dir = Path("sample_images")
        sample_dir.mkdir(exist_ok=True)
        return False


def build_docs(format_type="html", clean=False):
    """Build documentation in specified format."""
    docs_dir = Path("docs")
    if not docs_dir.exists():
        print("❌ docs/ directory not found")
        return False

    # Change to docs directory
    original_cwd = os.getcwd()
    os.chdir(docs_dir)

    try:
        make_cmd = get_make_command()

        if not make_cmd:
            print("❌ Make command not found. Using sphinx-build directly...")
            # Fallback to using sphinx-build directly
            sphinx_build = find_executable("sphinx-build")

            if clean:
                print("🧹 Cleaning previous build...")
                import shutil as sh

                if Path("_build").exists():
                    sh.rmtree("_build")

            # Build documentation using sphinx-build
            print(f"📚 Building {format_type} documentation...")
            if format_type == "html":
                result = run_command([sphinx_build, "-b", "html", ".", "_build/html"])
            elif format_type == "pdf":
                result = run_command([sphinx_build, "-b", "latex", ".", "_build/latex"])
                if result.returncode == 0:
                    # Build PDF from LaTeX
                    latex_dir = Path("_build/latex")
                    if latex_dir.exists():
                        os.chdir(latex_dir)
                        pdflatex = find_executable("pdflatex")
                        result = run_command([pdflatex, "*.tex"], check=False)
                        os.chdir("..")
            else:
                result = run_command(
                    [sphinx_build, "-b", format_type, ".", f"_build/{format_type}"]
                )
        else:
            # Use make command
            if clean:
                print("🧹 Cleaning previous build...")
                run_command([make_cmd, "clean"])

            # Build documentation
            print(f"📚 Building {format_type} documentation...")
            result = run_command([make_cmd, format_type])

        if result.returncode == 0:
            print(f"✅ {format_type.upper()} documentation built successfully")

            # Show output location
            if format_type == "html":
                output_path = Path("_build/html/index.html").resolve()
                print(f"📄 Documentation available at: {output_path}")
            elif format_type == "pdf":
                pdf_files = list(Path("_build/latex").glob("*.pdf"))
                if pdf_files:
                    print(f"📄 PDF available at: {pdf_files[0].resolve()}")

            return True
        else:
            print(f"❌ {format_type.upper()} build failed")
            return False

    finally:
        os.chdir(original_cwd)


def serve_docs(port=8000, open_browser=True):
    """Serve documentation with live reload."""
    docs_dir = Path("docs")
    if not docs_dir.exists():
        print("❌ docs/ directory not found")
        return False

    # Check if sphinx-autobuild is available
    sphinx_autobuild = find_executable("sphinx-autobuild")
    try:
        subprocess.run([sphinx_autobuild, "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ sphinx-autobuild not found. Install with:")
        print("   pip install sphinx-autobuild")
        return False

    print(f"🚀 Starting documentation server on port {port}...")
    print(f"📄 Documentation will be available at: http://localhost:{port}")
    print("🔄 Auto-reload enabled - changes will be reflected automatically")
    print("Press Ctrl+C to stop the server")

    # Open browser if requested
    if open_browser:
        import threading
        import time

        def open_browser_delayed():
            time.sleep(2)  # Wait for server to start
            webbrowser.open(f"http://localhost:{port}")

        threading.Thread(target=open_browser_delayed, daemon=True).start()

    # Start the server
    try:
        sphinx_autobuild = find_executable("sphinx-autobuild")
        subprocess.run(
            [
                sphinx_autobuild,
                str(docs_dir),
                str(docs_dir / "_build" / "html"),
                "--port",
                str(port),
                "--host",
                "localhost",
                "--ignore",
                "*.tmp",
                "--ignore",
                "*~",
            ]
        )
    except KeyboardInterrupt:
        print("\n👋 Documentation server stopped")


def run_checks():
    """Run documentation quality checks."""
    docs_dir = Path("docs")
    if not docs_dir.exists():
        print("❌ docs/ directory not found")
        return False

    original_cwd = os.getcwd()
    os.chdir(docs_dir)

    try:
        print("🔍 Running documentation checks...")
        make_cmd = get_make_command()

        if not make_cmd:
            print(
                "❌ Make command not found. Using sphinx-build directly for checks..."
            )
            sphinx_build = find_executable("sphinx-build")

            # Link check
            print("\n📎 Checking links...")
            result = run_command(
                [sphinx_build, "-b", "linkcheck", ".", "_build/linkcheck"], check=False
            )
            if result.returncode == 0:
                print("✅ Link check passed")
            else:
                print("⚠️ Some links may be broken")

            # Doctest
            print("\n🧪 Running doctests...")
            result = run_command(
                [sphinx_build, "-b", "doctest", ".", "_build/doctest"], check=False
            )
            if result.returncode == 0:
                print("✅ Doctests passed")
            else:
                print("⚠️ Some doctests failed")

            # Coverage
            print("\n📊 Checking documentation coverage...")
            result = run_command(
                [sphinx_build, "-b", "coverage", ".", "_build/coverage"], check=False
            )
            if result.returncode == 0:
                print("✅ Coverage check completed")
            else:
                print("⚠️ Coverage check had issues")
        else:
            # Use make command
            # Link check
            print("\n📎 Checking links...")
            result = run_command([make_cmd, "linkcheck"], check=False)
            if result.returncode == 0:
                print("✅ Link check passed")
            else:
                print("⚠️ Some links may be broken")

            # Doctest
            print("\n🧪 Running doctests...")
            result = run_command([make_cmd, "doctest"], check=False)
            if result.returncode == 0:
                print("✅ Doctests passed")
            else:
                print("⚠️ Some doctests failed")

            # Coverage
            print("\n📊 Checking documentation coverage...")
            result = run_command([make_cmd, "coverage"], check=False)
            if result.returncode == 0:
                print("✅ Coverage check completed")
            else:
                print("⚠️ Coverage check had issues")

        return True

    finally:
        os.chdir(original_cwd)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Build and serve GUI Image Studio documentation"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Build command
    build_parser = subparsers.add_parser("build", help="Build documentation")
    build_parser.add_argument(
        "--format",
        choices=["html", "pdf", "epub"],
        default="html",
        help="Output format (default: html)",
    )
    build_parser.add_argument(
        "--clean", action="store_true", help="Clean previous build before building"
    )

    # Serve command
    serve_parser = subparsers.add_parser(
        "serve", help="Serve documentation with live reload"
    )
    serve_parser.add_argument(
        "--port", type=int, default=8000, help="Port to serve on (default: 8000)"
    )
    serve_parser.add_argument(
        "--no-browser", action="store_true", help="Don't open browser automatically"
    )

    # Check command
    subparsers.add_parser("check", help="Run documentation quality checks")

    # Setup command
    subparsers.add_parser("setup", help="Setup documentation environment")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Check dependencies
    if not check_dependencies():
        print("\n❌ Please install required dependencies first:")
        print("   pip install -r docs/requirements-docs.txt")
        print("   pip install -e .")
        return

    # Create sample images
    create_sample_images()

    # Execute command
    if args.command == "build":
        success = build_docs(args.format, args.clean)
        if success and args.format == "html":
            output_path = Path("docs/_build/html/index.html")
            if output_path.exists():
                print(f"\n🌐 Open in browser: file://{output_path.resolve()}")

    elif args.command == "serve":
        serve_docs(args.port, not args.no_browser)

    elif args.command == "check":
        run_checks()

    elif args.command == "setup":
        print("🔧 Setting up documentation environment...")

        # Install dependencies
        print("📦 Installing documentation dependencies...")
        run_command(
            [sys.executable, "-m", "pip", "install", "-r", "docs/requirements-docs.txt"]
        )

        # Install package in development mode
        print("📦 Installing GUI Image Studio in development mode...")
        run_command([sys.executable, "-m", "pip", "install", "-e", "."])

        # Create sample images
        create_sample_images()

        # Build documentation
        build_docs("html", clean=True)

        print("✅ Documentation environment setup complete!")
        print("💡 Try: python scripts/build-docs.py serve")


if __name__ == "__main__":
    main()
