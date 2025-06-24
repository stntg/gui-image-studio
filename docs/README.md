# GUI Image Studio Documentation

This directory contains comprehensive documentation for GUI Image Studio, built using Sphinx and following the same professional standards as the ThreePaneWindows project.

## Documentation Structure

```text
docs/
├── conf.py                     # Sphinx configuration
├── index.rst                   # Main documentation index
├── installation.rst            # Installation guide
├── quickstart.rst             # Quick start guide
├── contributing.rst           # Contribution guidelines
├── changelog.rst              # Version history
├── license.rst                # License information
├── Makefile                   # Build automation
├── requirements-docs.txt      # Documentation dependencies
├── _static/                   # Static assets
├── api/                       # API reference
│   ├── index.rst
│   ├── image_loader.rst
│   ├── image_studio.rst
│   ├── generator.rst
│   ├── sample_creator.rst
│   └── cli.rst
├── examples/                  # Code examples
│   ├── index.rst
│   ├── basic_usage.rst
│   └── image_processing.rst
└── user_guide/               # User documentation
    └── index.rst
```

## Building the Documentation

### Prerequisites

Install documentation dependencies:

```bash
pip install -r docs/requirements-docs.txt
```

### Build HTML Documentation

```bash
cd docs/
make html
```

The built documentation will be available in `_build/html/index.html`.

### Live Development Server

For live editing with auto-reload:

```bash
cd docs/
make livehtml
```

This starts a development server at `http://localhost:8000`.

### Development Scripts

We provide convenient scripts for documentation development:

**Python Script (Cross-platform):**
```bash
# Setup documentation environment
python scripts/build-docs.py setup

# Build documentation
python scripts/build-docs.py build
python scripts/build-docs.py build --format pdf --clean

# Serve with live reload
python scripts/build-docs.py serve
python scripts/build-docs.py serve --port 8080 --no-browser

# Run quality checks
python scripts/build-docs.py check
```

**PowerShell Script (Windows):**
```powershell
# Setup documentation environment
.\scripts\build-docs.ps1 setup

# Build documentation
.\scripts\build-docs.ps1 build
.\scripts\build-docs.ps1 build -Format pdf -Clean

# Serve with live reload
.\scripts\build-docs.ps1 serve
.\scripts\build-docs.ps1 serve -Port 8080 -NoBrowser

# Run quality checks
.\scripts\build-docs.ps1 check
```

### Other Formats

```bash
# Build PDF
make pdf

# Build EPUB
make epub

# Check links
make linkcheck

# Run doctests
make doctest
```

## Documentation Features

### Professional Structure
- **Comprehensive API Reference**: Complete documentation of all modules and functions
- **Detailed Examples**: Step-by-step tutorials with working code
- **User Guides**: Complete guides for different user types
- **Installation Instructions**: Detailed setup and troubleshooting
- **Contributing Guidelines**: Complete guide for contributors

### Advanced Features
- **Auto-generated API docs**: Using Sphinx autodoc
- **Cross-references**: Automatic linking between sections
- **Code highlighting**: Syntax highlighting for all code blocks
- **Search functionality**: Full-text search capability
- **Multiple formats**: HTML, PDF, EPUB output
- **Mobile responsive**: Works on all device sizes

### Quality Assurance
- **Link checking**: Automated validation of all links
- **Spell checking**: Built-in spell checking
- **Style validation**: Consistent formatting
- **Code testing**: All examples are tested

## Documentation Standards

### Writing Style
- Clear, concise language
- Step-by-step instructions
- Comprehensive examples
- Error handling guidance
- Performance considerations

### Code Examples
- Complete, runnable examples
- Proper error handling
- Type hints included
- Comprehensive comments
- Real-world use cases

### API Documentation
- Complete function signatures
- Parameter descriptions
- Return value documentation
- Exception information
- Usage examples

## Maintenance

### Regular Updates
- Keep examples current with latest API
- Update installation instructions
- Maintain compatibility information
- Review and update links

### Quality Checks
```bash
# Style checking
make style-check

# Spell checking
make spell-check

# Link validation
make linkcheck
```

## Contributing to Documentation

### Adding New Content
1. Create new `.rst` files in appropriate directories
2. Add to relevant `toctree` directives
3. Follow existing formatting standards
4. Include working code examples
5. Test all examples

### Updating Existing Content
1. Maintain backward compatibility
2. Update cross-references
3. Test all code examples
4. Update table of contents if needed

### Documentation Review Process
1. Technical accuracy review
2. Language and style review
3. Example testing
4. Link validation
5. Final approval

## Integration with Project

### Automated Building
The documentation is integrated with the project's CI/CD pipeline through GitHub Actions:

#### Main Documentation Workflow (`.github/workflows/docs.yml`)
- **Triggers**: Push to main/develop, PRs, releases
- **Features**:
  - Builds HTML and PDF documentation
  - Runs quality checks (link validation, doctests)
  - Deploys to GitHub Pages (main branch only)
  - Uploads artifacts for download
  - Comprehensive error reporting

#### Documentation Check Workflow (`.github/workflows/docs-check.yml`)
- **Triggers**: Pull requests affecting documentation
- **Features**:
  - Quick build validation
  - RST syntax checking
  - Essential files verification
  - PR comments with build status

#### Workflow Features:
```yaml
# Automatic deployment to GitHub Pages
- name: Deploy to GitHub Pages
  if: github.ref == 'refs/heads/main'
  uses: actions/deploy-pages@v2

# Quality checks
- name: Run documentation tests
  run: |
    make doctest      # Test code examples
    make linkcheck    # Validate links
    make coverage     # Check API coverage
```

### Version Synchronization
Documentation versions are synchronized with project releases:
- Version numbers in `conf.py` auto-updated
- Changelog updates on each release
- API compatibility notes maintained
- GitHub Pages deployment on main branch updates

## Support

For documentation-related issues:
- Check the [GitHub Issues](https://github.com/stntg/gui-image-studio/issues)
- Review existing documentation
- Create new issues for improvements
- Contribute fixes and enhancements

## License

This documentation is licensed under the same terms as GUI Image Studio (MIT License).
