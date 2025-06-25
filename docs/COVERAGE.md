# Coverage Documentation

This document explains the coverage setup and usage for the GUI Image Studio project.

## Overview

Code coverage is set up using `pytest-cov` with comprehensive reporting in multiple
formats:

- Terminal output with missing line numbers
- HTML reports for detailed browsing
- XML reports for CI/CD integration
- JSON reports for programmatic access

## Coverage Configuration

Coverage is configured in multiple places:

### 1. pyproject.toml

Main configuration with pytest integration and tool settings.

### 2. .coveragerc

Additional coverage-specific settings including:

- Branch coverage enabled
- Exclusion patterns for untestable code
- Report formatting options
- Minimum coverage thresholds

## Running Coverage

### Quick Start

```bash
# Basic coverage report
pytest --cov=gui_image_studio

# Full coverage with all reports
pytest --cov=gui_image_studio --cov-report=html --cov-report=xml
```

### Using Coverage Scripts

#### Python Script (Cross-platform)

```bash
# Basic coverage
python scripts/run_coverage.py --basic

# Full coverage with all formats
python scripts/run_coverage.py --full

# Coverage excluding GUI components
python scripts/run_coverage.py --no-gui

# Open HTML report in browser
python scripts/run_coverage.py --open

# Clean coverage files
python scripts/run_coverage.py --clean
```

#### PowerShell Script (Windows)

```powershell
# Basic coverage
.\scripts\run_coverage.ps1 -Basic

# Full coverage with all formats
.\scripts\run_coverage.ps1 -Full

# Coverage excluding GUI components
.\scripts\run_coverage.ps1 -NoGui

# Open HTML report in browser
.\scripts\run_coverage.ps1 -Open

# Clean coverage files
.\scripts\run_coverage.ps1 -Clean
```

## Coverage Reports

### Terminal Report

Shows coverage percentage and missing line numbers directly in the terminal.

### HTML Report

- Generated in `htmlcov/` directory
- Interactive browsing of coverage
- Line-by-line coverage visualization
- Branch coverage details

### XML Report

- Generated as `coverage.xml`
- Used by CI/CD systems and coverage services
- Compatible with Codecov, Coveralls, etc.

### JSON Report

- Generated as `coverage.json`
- Programmatic access to coverage data
- Useful for custom reporting tools

## Coverage Targets

| Component | Target Coverage | Notes |
|-----------|----------------|-------|
| Core Library | 90%+ | High coverage for stable APIs |
| Image Processing | 85%+ | Critical functionality |
| GUI Components | 60%+ | Limited by display requirements |
| CLI Tools | 70%+ | Command-line interfaces |
| Overall Project | 70%+ | Minimum acceptable coverage |

## Exclusions

The following are excluded from coverage:

### Code Patterns

- `pragma: no cover` comments
- Debug-only code (`if self.debug:`)
- Abstract methods
- Platform-specific code
- Type checking imports

### Files/Directories

- Test files (`test_*.py`)
- Development files (`dev_files/`)
- CLI entry points (`cli.py`)
- Main modules (`__main__.py`)

### GUI-Specific Exclusions

- Event handlers (`def on_*`, `def handle_*`, `def callback_*`)
- GUI initialization code requiring display
- Platform-specific GUI code

## CI/CD Integration

### GitHub Actions

Coverage runs automatically on:

- Push to main/develop branches
- Pull requests
- Weekly scheduled runs

### Coverage Services

- **Codecov**: Automatic upload of XML reports
- **Coveralls**: Alternative coverage service
- **Coverage Comments**: PR comments with coverage changes

## Troubleshooting

### Common Issues

#### GUI Tests Failing

```bash
# Skip GUI-dependent tests
pytest --ignore=tests/test_tint_visibility.py
```

#### Low Coverage Warnings

```bash
# Check which lines are missing
pytest --cov=gui_image_studio --cov-report=term-missing
```

#### Coverage Files Not Found

```bash
# Clean and regenerate
python scripts/run_coverage.py --clean
python scripts/run_coverage.py --full
```

### Platform-Specific Issues

#### Linux (Headless)

```bash
# Use xvfb for GUI tests
xvfb-run -a pytest --cov=gui_image_studio
```

#### Windows

```powershell
# Use PowerShell script for better Windows support
.\scripts\run_coverage.ps1 -Full
```

#### macOS

```bash
# Standard pytest should work
pytest --cov=gui_image_studio --cov-report=html
```

## Best Practices

### Writing Testable Code

1. Separate business logic from GUI code
2. Use dependency injection for external dependencies
3. Create mock objects for GUI components
4. Use factory patterns for complex objects

### Improving Coverage

1. Focus on critical paths first
2. Add unit tests for new features
3. Use parametrized tests for multiple scenarios
4. Mock external dependencies

### Coverage Analysis

1. Review HTML reports regularly
2. Focus on branch coverage, not just line coverage
3. Identify untested error paths
4. Document intentionally excluded code

## Coverage Metrics

### Current Status

Run `python scripts/run_coverage.py --summary` to see current coverage files.

### Historical Tracking

Coverage trends are tracked in CI/CD and can be viewed on:

- Codecov dashboard
- GitHub Actions artifacts
- Local HTML reports

## Integration with Development Workflow

### Pre-commit Hooks

Coverage can be integrated with pre-commit hooks:

```yaml
# .pre-commit-config.yaml
- repo: local
  hooks:
    - id: coverage-check
      name: coverage-check
      entry: python scripts/run_coverage.py --basic
      language: system
      pass_filenames: false
```

### IDE Integration

Most IDEs support coverage visualization:

- VS Code: Coverage Gutters extension
- PyCharm: Built-in coverage runner
- Vim/Neovim: Coverage plugins

## Future Enhancements

### Planned Improvements

1. Differential coverage for PRs
2. Coverage regression detection
3. Automated coverage reports in documentation
4. Integration with code quality metrics

### Advanced Features

1. Mutation testing integration
2. Performance impact analysis
3. Coverage-guided test generation
4. Custom coverage metrics for GUI components
