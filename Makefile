# this_file: Makefile
# Makefile for vexy-mkdocs-strip-number-prefix

.PHONY: help setup install clean test lint format build docs coverage pre-commit release

# Default target
help:
	@echo "Available targets:"
	@echo "  setup       Set up development environment"
	@echo "  install     Install package in development mode"
	@echo "  clean       Clean build artifacts"
	@echo "  test        Run tests"
	@echo "  lint        Run linting checks"
	@echo "  format      Format code with ruff and black"
	@echo "  build       Build package"
	@echo "  docs        Build documentation"
	@echo "  coverage    Generate coverage report"
	@echo "  pre-commit  Set up pre-commit hooks"
	@echo "  release     Create a new release (requires VERSION=x.y.z)"
	@echo ""
	@echo "Examples:"
	@echo "  make setup"
	@echo "  make test"
	@echo "  make build"
	@echo "  make release VERSION=1.0.0"

# Development setup
setup:
	@scripts/dev.sh setup

# Install package in development mode
install:
	@scripts/dev.sh install

# Clean build artifacts
clean:
	@scripts/dev.sh clean

# Run tests
test:
	@scripts/test.sh

# Run linting
lint:
	@scripts/dev.sh lint

# Format code
format:
	@scripts/dev.sh format

# Build package
build:
	@scripts/build.sh

# Build documentation
docs:
	@scripts/dev.sh docs

# Generate coverage report
coverage:
	@scripts/dev.sh coverage

# Set up pre-commit hooks
pre-commit:
	@scripts/dev.sh pre-commit

# Create release (requires VERSION variable)
release:
	@if [ -z "$(VERSION)" ]; then \
		echo "Error: VERSION is required. Use: make release VERSION=x.y.z"; \
		exit 1; \
	fi
	@scripts/release.sh $(VERSION)

# Release with publishing
release-publish:
	@if [ -z "$(VERSION)" ]; then \
		echo "Error: VERSION is required. Use: make release-publish VERSION=x.y.z"; \
		exit 1; \
	fi
	@scripts/release.sh --publish $(VERSION)

# Dry run release
release-dry-run:
	@if [ -z "$(VERSION)" ]; then \
		echo "Error: VERSION is required. Use: make release-dry-run VERSION=x.y.z"; \
		exit 1; \
	fi
	@scripts/release.sh --dry-run $(VERSION)

# Combined development workflow
dev-check: format lint test
	@echo "Development checks completed successfully!"

# Full CI workflow
ci: clean install lint test build
	@echo "CI workflow completed successfully!"