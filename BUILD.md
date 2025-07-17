# Build System Documentation

This document describes the comprehensive build, test, and release system for `vexy-mkdocs-strip-number-prefix`.

## Overview

The project uses a modern Python packaging setup with:
- **Git-tag-based semversioning** using `hatch-vcs`
- **Comprehensive test suite** with 95%+ coverage
- **Local development scripts** for build/test/release workflows
- **GitHub Actions** for CI/CD with multiplatform testing
- **Automated dependency updates** with Dependabot
- **Trusted PyPI publishing** with attestations

## Quick Start

### Prerequisites

- Python 3.9+
- Git
- Make (optional, for convenience)

### Setup Development Environment

```bash
# Using make (recommended)
make setup

# Or using scripts directly
./scripts/dev.sh setup

# Or manually
pip install -e .[dev]
```

### Common Development Tasks

```bash
# Run tests
make test

# Format code
make format

# Run linting
make lint

# Build package
make build

# Full development check
make dev-check
```

## Local Scripts

### Build Script (`scripts/build.sh`)

Builds the Python package and verifies it:

```bash
./scripts/build.sh
```

**Features:**
- Cleans previous builds
- Installs build dependencies
- Builds wheel and source distributions
- Validates package with `twine check`
- Extracts version from built artifacts

### Test Script (`scripts/test.sh`)

Runs comprehensive test suite:

```bash
./scripts/test.sh
```

**Features:**
- Installs test dependencies
- Runs code quality checks (ruff, black, mypy)
- Executes tests with coverage reporting
- Generates HTML and XML coverage reports
- Runs pre-commit hooks (if available)

### Release Script (`scripts/release.sh`)

Creates git-tag-based releases:

```bash
# Create release
./scripts/release.sh 1.0.0

# Dry run (preview changes)
./scripts/release.sh --dry-run 1.0.0

# Create and publish to PyPI
./scripts/release.sh --publish 1.0.0
```

**Features:**
- Validates semantic versioning
- Ensures clean working directory
- Runs tests before release
- Updates CHANGELOG.md automatically
- Creates git tags
- Optionally publishes to PyPI

### Development Helper (`scripts/dev.sh`)

Provides various development utilities:

```bash
# Available commands
./scripts/dev.sh setup       # Set up development environment
./scripts/dev.sh format      # Format code
./scripts/dev.sh lint        # Run linting
./scripts/dev.sh test        # Run tests
./scripts/dev.sh docs        # Build documentation
./scripts/dev.sh clean       # Clean build artifacts
./scripts/dev.sh coverage    # Generate coverage report
./scripts/dev.sh pre-commit  # Set up pre-commit hooks
```

## Makefile Targets

The Makefile provides convenient shortcuts:

```bash
make help           # Show available targets
make setup          # Set up development environment
make install        # Install in development mode
make clean          # Clean build artifacts
make test           # Run tests
make lint           # Run linting
make format         # Format code
make build          # Build package
make docs           # Build documentation
make coverage       # Generate coverage report
make pre-commit     # Set up pre-commit hooks
make release VERSION=1.0.0        # Create release
make release-publish VERSION=1.0.0 # Create and publish release
make release-dry-run VERSION=1.0.0 # Dry run release
make dev-check      # Run format, lint, test
make ci             # Full CI workflow
```

## GitHub Actions

### CI Workflow (`.github/workflows/ci.yml`)

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop`

**Jobs:**
- **test**: Runs tests on multiple OS/Python combinations
  - Ubuntu, Windows, macOS
  - Python 3.9, 3.10, 3.11, 3.12, 3.13
- **lint**: Code quality checks (ruff, black, mypy)
- **build**: Package building and validation
- **security**: Security scanning (Bandit, Safety)

**Features:**
- Multiplatform testing
- Comprehensive coverage reporting
- Artifact uploading
- Fast-fail for code quality issues

### Release Workflow (`.github/workflows/release.yml`)

**Triggers:**
- Git tags matching `v*` pattern

**Jobs:**
- **test**: Pre-release testing
- **build**: Package building
- **publish-pypi**: PyPI publishing with trusted publishing
- **create-release**: GitHub release creation
- **post-release**: Summary and notifications

**Features:**
- Automated changelog extraction
- PyPI attestations for transparency
- Prerelease detection
- Release summaries

### Dependabot Configuration

Automatic dependency updates:
- **Python dependencies**: Weekly updates on Mondays
- **GitHub Actions**: Weekly updates on Mondays
- Pull request limits and auto-assignment
- Consistent commit message formatting

## Git-Tag-Based Semversioning

The project uses `hatch-vcs` for automatic version management:

### Version Derivation

Version is automatically derived from git tags:
- `v1.0.0` → `1.0.0`
- `v1.0.1` → `1.0.1`
- Development versions include commit hash

### Creating Releases

1. **Prepare release:**
   ```bash
   # Run tests and build
   make dev-check
   make build
   ```

2. **Create release:**
   ```bash
   # Using script
   ./scripts/release.sh 1.0.0
   
   # Or using make
   make release VERSION=1.0.0
   ```

3. **Automated process:**
   - Updates CHANGELOG.md
   - Creates git tag
   - Pushes to remote
   - Triggers GitHub Actions release workflow

## Package Distribution

### PyPI Publishing

**Automated (recommended):**
- Push git tag → GitHub Actions → PyPI
- Uses trusted publishing (no tokens needed)
- Generates attestations for transparency

**Manual:**
```bash
# Build and publish
make build
python -m twine upload dist/*
```

### Package Artifacts

Built packages include:
- **Wheel** (`.whl`): Binary distribution
- **Source distribution** (`.tar.gz`): Source code
- **Attestations**: Transparency metadata

## Testing

### Test Coverage

Current test coverage: 95%+

### Test Types

1. **Unit tests**: Individual function testing
2. **Integration tests**: Plugin integration with MkDocs
3. **End-to-end tests**: Full MkDocs build testing
4. **Edge case tests**: Error handling and boundary conditions

### Running Tests

```bash
# Basic test run
pytest

# With coverage
pytest --cov=mkdocs_strip_number_prefix

# Specific test
pytest tests/test_plugin.py::test_specific_function

# Using scripts
./scripts/test.sh
```

## Code Quality

### Tools Used

- **ruff**: Fast Python linter and formatter
- **black**: Code formatting
- **mypy**: Type checking
- **pre-commit**: Git hooks

### Standards

- **PEP 8**: Style guide compliance
- **Type hints**: Full type annotation
- **Docstrings**: Comprehensive documentation
- **Test coverage**: 90%+ required

## Troubleshooting

### Common Issues

1. **Build fails:**
   ```bash
   make clean
   make setup
   make build
   ```

2. **Tests fail:**
   ```bash
   # Update dependencies
   pip install -e .[dev]
   
   # Run specific test
   pytest tests/test_plugin.py -v
   ```

3. **Version issues:**
   ```bash
   # Check git tags
   git tag -l
   
   # Check version
   python -c "import mkdocs_strip_number_prefix; print(mkdocs_strip_number_prefix.__version__)"
   ```

4. **Release issues:**
   ```bash
   # Dry run first
   ./scripts/release.sh --dry-run 1.0.0
   
   # Check working directory
   git status
   ```

### Getting Help

- Check the [README.md](README.md) for usage instructions
- Review [CHANGELOG.md](CHANGELOG.md) for recent changes
- Create an issue on GitHub for bugs or feature requests

## Contributing

1. Fork the repository
2. Set up development environment: `make setup`
3. Make changes
4. Run tests: `make dev-check`
5. Create pull request

The CI system will automatically test your changes across multiple platforms and Python versions.