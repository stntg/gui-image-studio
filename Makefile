# Makefile for GUI Image Studio
# Provides convenient commands for development tasks

.PHONY: help install test coverage coverage-html coverage-open clean lint format docs

# Default target
help:
	@echo "GUI Image Studio - Available Commands"
	@echo "====================================="
	@echo ""
	@echo "Setup:"
	@echo "  install          Install package in development mode"
	@echo "  install-dev      Install with development dependencies"
	@echo ""
	@echo "Testing:"
	@echo "  test             Run all tests"
	@echo "  test-fast        Run tests excluding slow ones"
	@echo "  test-gui         Run GUI-specific tests"
	@echo ""
	@echo "Coverage:"
	@echo "  coverage         Run basic coverage report"
	@echo "  coverage-html    Run coverage with HTML report"
	@echo "  coverage-full    Run full coverage with all reports"
	@echo "  coverage-open    Open HTML coverage report"
	@echo "  coverage-clean   Clean coverage files"
	@echo ""
	@echo "Code Quality:"
	@echo "  lint             Run linting checks"
	@echo "  format           Format code with black and isort"
	@echo "  type-check       Run type checking with mypy"
	@echo ""
	@echo "Documentation:"
	@echo "  docs             Build documentation"
	@echo "  docs-serve       Serve documentation locally"
	@echo ""
	@echo "Maintenance:"
	@echo "  clean            Clean build artifacts and cache files"
	@echo "  clean-all        Clean everything including coverage"

# Installation
install:
	pip install -e .

install-dev:
	pip install -e .[dev,test,docs]

# Testing
test:
	pytest

test-fast:
	pytest -m "not slow"

test-gui:
	pytest -m "gui"

# Coverage
coverage:
	python scripts/run_coverage.py --basic

coverage-html:
	python scripts/run_coverage.py --full

coverage-full:
	python scripts/run_coverage.py --full

coverage-open:
	python scripts/run_coverage.py --open

coverage-clean:
	python scripts/run_coverage.py --clean

# Code Quality
lint:
	flake8 src/gui_image_studio tests
	mypy src/gui_image_studio
	bandit -r src/gui_image_studio/

format:
	black .
	isort .

type-check:
	mypy src/gui_image_studio

# Documentation
docs:
	sphinx-build -W -b html docs docs/_build/html

docs-serve:
	python -m http.server 8000 --directory docs/_build/html

# Maintenance
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/

clean-all: clean coverage-clean
	rm -rf docs/_build/
	rm -rf .tox/
	rm -rf .pytest_cache/
