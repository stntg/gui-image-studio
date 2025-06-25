# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned Additions

- Planned features for future releases

### Changed

- Planned improvements for future releases

### Fixed

- Planned bug fixes for future releases


## [1.0.1] - 2025-06-25

### Security

- security: fix partial executable path vulnerability in Windows print function.
- Fix security issue and reduce method complexity in print_content.
- Fix security vulnerabilities in process execution.

### Changed

- refactor: reduce cyclomatic complexity in build-docs.py.
- Update docs.yml.
- Test pre-commit hooks.

### Fixed

- Fix Python code block syntax errors in documentation.
- Fix GitHub Actions workflow and documentation syntax errors.
- Complete pre-commit hooks fix.

### Removed

- Remove test file.

## [1.0.0] - 2024-12-19

### Added

- Initial release of gui-image-studio package
- **GUI Image Studio**: Visual image editor with drawing tools
- Core image embedding functionality with `embed_images_from_folder()`
- Advanced image loading with `get_image()` function
- Support for tkinter and customtkinter frameworks
- Image transformation features:
  - Resize, rotate operations
  - Color tinting with RGB values and intensity control
  - Contrast and saturation adjustments
  - Grayscale conversion
  - Transparency control
- Theme support (default, dark, light)
- Animated GIF support with frame processing
- Batch processing of image folders
- Command line interface with console scripts:
  - `gui-image-studio-generate`
  - `gui-image-studio-create-samples`
  - `gui-image-studio-designer`
- Sample image generation for testing
- High-quality compression options (JPEG/WebP)
- Comprehensive example collection
- Full documentation and API reference

### Feature Details

- **Image Loading**: Load images as PhotoImage objects for GUI frameworks
- **Batch Embedding**: Process entire folders and generate embedded Python
  modules
- **Transformations**: Apply various image transformations on-the-fly
- **Framework Support**: Native support for tkinter and customtkinter
- **CLI Tools**: Command-line utilities for common tasks
- **Quality Control**: Configurable compression and quality settings
- **Sample Generation**: Built-in sample image creator for testing

### Technical Details

- Python 3.8+ compatibility
- Cross-platform support (Windows, macOS, Linux)
- Dependencies: Pillow >= 8.0.0, customtkinter >= 5.0.0 (optional)
- Modular architecture with separate modules:
  - `image_studio.py`: GUI application
  - `image_loader.py`: Image loading with transformations
  - `generator.py`: Image embedding utilities
  - `sample_creator.py`: Sample image generation
  - `cli.py`: Command line interface
- Comprehensive error handling and fallbacks
- Memory-efficient image processing with caching
- Configuration-based image processing with `ImageConfig` dataclass

### Documentation

- Complete README with usage examples
- API reference documentation
- Deployment guide for releases and PyPI publishing
- GitHub Actions workflows for CI/CD
- Comprehensive example collection
- MIT License for open-source compatibility

### Examples Included

- Basic usage patterns
- Theme integration examples
- Image transformation demonstrations
- Animated GIF handling
- Advanced feature showcases
- Framework-specific implementations

---

## Release Notes Template

When creating new releases, use this template:

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- New features and functionality

### Changed
- Changes to existing functionality
- Performance improvements
- API modifications (with migration notes)

### Deprecated
- Features that will be removed in future versions

### Removed
- Features removed in this version

### Fixed
- Bug fixes and corrections

### Security
- Security-related changes and fixes
```

## Version History Summary

- **v1.0.0**: Initial release with core functionality
- **Future versions**: Will be documented here as they are released

## Migration Guides

### Upgrading to v1.0.0

- This is the initial release, no migration needed

### Future Migration Guides

- Will be added here for major version changes that require code updates
