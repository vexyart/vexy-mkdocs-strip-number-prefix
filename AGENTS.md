# `https://github.com/vexyart/vexy-mkdocs-strip-number-prefix`

## Project Overview

This is **vexy-mkdocs-strip-number-prefix**, a lightweight MkDocs plugin that strips numeric prefixes from documentation files to create clean URLs while maintaining file ordering.

## Development Commands

### Setup
```bash
# Install in development mode with all dependencies
pip install -e .[dev]

# Install pre-commit hooks
pre-commit install
```

### Testing
```bash
# Run all tests
python -m pytest

# Run tests with coverage report
python -m pytest --cov=mkdocs_strip_number_prefix --cov-report=html

# Run a specific test
python -m pytest tests/test_plugin.py::test_specific_function
```

### Code Quality
```bash
# Run all pre-commit checks
pre-commit run --all-files

# Individual checks
ruff check --output-format=github .
black --check --diff .
mypy src

# Auto-fix issues
ruff check --fix .
black .
```

### Post-Edit Commands
```bash
# Run after making changes to Python files
fd -e py -x uvx autoflake -i {}; fd -e py -x uvx pyupgrade --py312-plus {}; fd -e py -x uvx ruff check --output-format=github --fix --unsafe-fixes {}; fd -e py -x uvx ruff format --respect-gitignore --target-version py312 {}; python -m pytest;
```

## Architecture

### Core Components

1. **`src/mkdocs_strip_number_prefix/plugin.py`**: Main plugin implementation
   - `StripNumberPrefixPlugin` class that extends `BasePlugin`
   - `on_files` method processes all files during MkDocs build
   - Strips prefixes from `src_path`, `dest_path`, and `url` attributes
   - Optionally rewrites internal markdown links

2. **Pattern Matching Logic**:
   - Default pattern: `^\d+--` (matches patterns like `010--filename.md`)
   - Configurable via `pattern` option in mkdocs.yml
   - Uses compiled regex for performance

3. **Collision Detection**:
   - Tracks URL mappings to prevent conflicts
   - `strict` mode: Fails build on collision
   - Non-strict mode: Logs warning and keeps first file

### Key Design Decisions

- **Prefix Convention**: Uses double dash (`--`) after numbers for clarity
- **URL Preservation**: Only strips prefixes, maintains rest of URL structure
- **Link Rewriting**: Optional feature (`strip_links`) to update internal references
- **Error Handling**: Graceful failures with helpful error messages

## Development Workflow

### File Management
Every source file must include a `this_file` comment near the top:
```python
# this_file: src/mkdocs_strip_number_prefix/plugin.py
```

### Python Guidelines
- Python 3.9+ with modern syntax (f-strings, type hints, pathlib)
- Strict type checking with MyPy
- Follow PEP 8, PEP 20, PEP 257
- Use loguru for verbose logging when appropriate

### Testing Approach
- Test edge cases (empty patterns, invalid regex, URL collisions)
- Mock MkDocs File objects for unit testing
- Maintain >90% code coverage
- Test both strict and non-strict modes

## Special Commands

### `/report` Command
Analyzes recent changes and updates project documentation:
1. Reads TODO.md and PLAN.md
2. Documents changes in CHANGELOG.md
3. Removes completed items
4. Ensures PLAN.md has detailed plans

### `/work` Command
Iterative development workflow:
1. Reads TODO.md and PLAN.md
2. Works on immediate items
3. Updates WORK.md with progress
4. Reflects and improves implementation
5. Continues to next items

## Project Documentation Structure

- **README.md**: User-facing documentation with examples
- **CHANGELOG.md**: Version history and release notes
- **PLAN.md**: Detailed future development plans
- **TODO.md**: Simplified task list (checkbox format)
- **WORK.md**: Current work progress tracking

## Important Notes

- This is a beta project (Development Status :: 4)
- Follows semantic versioning via hatch-vcs
- Uses GitHub Actions for CI/CD
- Published to PyPI as `mkdocs-strip-number-prefix`