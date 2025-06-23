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
from pathlib import Path

def run_command(cmd, cwd=None, check=True):
    """Run a command and return the result."""
    print(f"Running: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, cwd=cwd, check=check, 
                              capture_output=True, text=True)
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
        print("❌ Sphinx not found. Install with: pip install -r docs/requirements-docs.txt")
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
        # Clean if requested
        if clean:
            print("🧹 Cleaning previous build...")
            run_command(["make", "clean"])
        
        # Build documentation
        print(f"📚 Building {format_type} documentation...")
        result = run_command(["make", format_type])
        
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
    try:
        subprocess.run(["sphinx-autobuild", "--version"], 
                      capture_output=True, check=True)
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
        subprocess.run([
            "sphinx-autobuild",
            str(docs_dir),
            str(docs_dir / "_build" / "html"),
            "--port", str(port),
            "--host", "localhost",
            "--ignore", "*.tmp",
            "--ignore", "*~"
        ])
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
        
        # Link check
        print("\n📎 Checking links...")
        result = run_command(["make", "linkcheck"], check=False)
        if result.returncode == 0:
            print("✅ Link check passed")
        else:
            print("⚠️ Some links may be broken")
        
        # Doctest
        print("\n🧪 Running doctests...")
        result = run_command(["make", "doctest"], check=False)
        if result.returncode == 0:
            print("✅ Doctests passed")
        else:
            print("⚠️ Some doctests failed")
        
        # Coverage
        print("\n📊 Checking documentation coverage...")
        result = run_command(["make", "coverage"], check=False)
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
        "--format", choices=["html", "pdf", "epub"], default="html",
        help="Output format (default: html)"
    )
    build_parser.add_argument(
        "--clean", action="store_true",
        help="Clean previous build before building"
    )
    
    # Serve command
    serve_parser = subparsers.add_parser("serve", help="Serve documentation with live reload")
    serve_parser.add_argument(
        "--port", type=int, default=8000,
        help="Port to serve on (default: 8000)"
    )
    serve_parser.add_argument(
        "--no-browser", action="store_true",
        help="Don't open browser automatically"
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
        run_command([sys.executable, "-m", "pip", "install", "-r", "docs/requirements-docs.txt"])
        
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