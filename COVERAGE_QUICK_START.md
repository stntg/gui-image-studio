# Coverage Quick Start Guide

## 🚀 Quick Commands

### Basic Coverage
```bash
# Run basic coverage report
python scripts/run_coverage.py --basic

# Or using pytest directly
pytest --cov=gui_image_studio --cov-report=term-missing
```

### Full Coverage with HTML Report
```bash
# Generate all coverage reports
python scripts/run_coverage.py --full

# Open HTML report in browser
python scripts/run_coverage.py --open
```

### Windows PowerShell
```powershell
# Basic coverage
.\scripts\run_coverage.ps1 -Basic

# Full coverage with HTML
.\scripts\run_coverage.ps1 -Full

# Open HTML report
.\scripts\run_coverage.ps1 -Open
```

### Using Makefile (Linux/macOS)
```bash
# Basic coverage
make coverage

# Full coverage with HTML
make coverage-html

# Open HTML report
make coverage-open
```

## 📊 Current Coverage Status

After running coverage, you'll see output like:
```
Name                                      Stmts   Miss Branch BrPart  Cover   Missing
-------------------------------------------------------------------------------------
src\gui_image_studio\__init__.py             46     17      6      3  61.5%   71-81, 89-90
src\gui_image_studio\generator.py            57     17     18      4  72.0%   50-54, 58
src\gui_image_studio\image_loader.py         99     54     26      2  37.6%   11-16, 72
src\gui_image_studio\sample_creator.py      153      4     24      1  97.2%   18-19
-------------------------------------------------------------------------------------
TOTAL                                       356     92     74     10  71.2%
```

## 🎯 Coverage Targets

- **Overall Project**: 70%+ ✅
- **Core Library**: 90%+
- **Image Processing**: 85%+
- **GUI Components**: 60%+ (limited by display requirements)

## 🔧 Troubleshooting

### GUI Tests Failing?
```bash
# Skip GUI-dependent tests
python scripts/run_coverage.py --no-gui
```

### Clean Coverage Files
```bash
# Remove all coverage files and start fresh
python scripts/run_coverage.py --clean
```

### View Coverage Summary
```bash
# Check what coverage files exist
python scripts/run_coverage.py --summary
```

## 📁 Coverage Files

After running coverage, you'll find:
- `htmlcov/index.html` - Interactive HTML report
- `coverage.xml` - XML report for CI/CD
- `coverage.json` - JSON data for custom tools
- `.coverage` - Raw coverage data

## 🔗 More Information

For detailed coverage documentation, see [docs/COVERAGE.md](docs/COVERAGE.md).

## 🚨 CI/CD Integration

Coverage runs automatically on:
- ✅ Push to main/develop branches
- ✅ Pull requests
- ✅ Weekly scheduled runs

View coverage reports on:
- [Codecov Dashboard](https://codecov.io) (when configured)
- GitHub Actions artifacts
- Local HTML reports