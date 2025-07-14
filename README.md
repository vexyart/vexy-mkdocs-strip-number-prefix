# vexy-mkdocs-strip-number-prefix

[![PyPI version](https://badge.fury.io/py/vexy-mkdocs-strip-number-prefix.svg)](https://pypi.org/project/vexy-mkdocs-strip-number-prefix/)
[![CI](https://github.com/vexyart/vexy-mkdocs-strip-number-prefix/workflows/CI/badge.svg)](https://github.com/vexyart/vexy-mkdocs-strip-number-prefix/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/vexyart/vexy-mkdocs-strip-number-prefix/branch/main/graph/badge.svg)](https://codecov.io/gh/vexyart/vexy-mkdocs-strip-number-prefix)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python versions](https://img.shields.io/pypi/pyversions/vexy-mkdocs-strip-number-prefix.svg)](https://pypi.org/project/vexy-mkdocs-strip-number-prefix/)

A lightweight MkDocs plugin that strips numeric prefixes from page URLs while preserving them in source filenames for natural sorting.

## Features

- ✅ **Clean URLs**: Remove numeric prefixes from generated URLs
- ✅ **Natural Sorting**: Keep prefixes in source files for predictable ordering
- ✅ **Collision Detection**: Prevent duplicate URLs with configurable strictness
- ✅ **Link Rewriting**: Automatically update internal markdown links
- ✅ **Flexible Patterns**: Customize prefix matching with regex patterns
- ✅ **Debug Support**: Verbose logging for troubleshooting

## Installation

Install from PyPI:

```bash
uv pip install --system --upgrade vexy-mkdocs-strip-number-prefix
```

or from source: 

```
pip install git+https://github.com/vexyart/vexy-mkdocs-strip-number-prefix
```

## Quick Start

Add the plugin to your `mkdocs.yml`:

```yaml
plugins:
  - search
  - strip-number-prefix
```

Name your files with numeric prefixes:

```
docs/
├── 010--introduction.md
├── 020--getting-started.md
├── 030--configuration.md
└── 999--faq.md
```

Build your site:

```bash
mkdocs build
```

Generated URLs will be clean:
- `/introduction/`
- `/getting-started/`
- `/configuration/`
- `/faq/`

## Configuration

All configuration options with their defaults:

```yaml
plugins:
  - strip-number-prefix:
      pattern: '^\\d+--'     # Regex pattern for prefix (default: '^\\d+--')
      verbose: false         # Enable debug logging (default: false)
      strict: true           # Fail on slug collisions (default: true)
      strip_links: false     # Strip prefixes from markdown links (default: false)
```

### Pattern Examples

| Pattern | Matches | Example |
|---------|---------|---------|
| `^\\d+--` | Any digits + `--` | `123--file.md` |
| `^\\d{3}--` | Exactly 3 digits + `--` | `001--file.md` |
| `^\\d+-` | Any digits + `-` | `42-file.md` |
| `^\\d+\\.` | Any digits + `.` | `1.file.md` |

### Collision Handling

When multiple files would generate the same URL after prefix removal:

```yaml
plugins:
  - strip-number-prefix:
      strict: true   # Fail build (recommended)
      # strict: false  # Log warning and continue
```

### Link Rewriting

Automatically update internal markdown links:

```yaml
plugins:
  - strip-number-prefix:
      strip_links: true
```

Before:
```markdown
[Setup Guide](020--setup.md)
```

After:
```markdown
[Setup Guide](setup.md)
```

## Examples

### Basic Usage

```yaml
# mkdocs.yml
site_name: My Documentation
plugins:
  - strip-number-prefix
```

### With Material Theme

```yaml
# mkdocs.yml
site_name: My Documentation
theme:
  name: material
  features:
    - navigation.instant
    - navigation.sections

plugins:
  - search
  - strip-number-prefix:
      pattern: '^\\d{3}--'
      verbose: true
```

### With Awesome Nav

```yaml
# mkdocs.yml
site_name: My Documentation
plugins:
  - search
  - awesome-nav
  - strip-number-prefix:
      pattern: '^\\d+--'
      strip_links: true
```

### Custom Pattern

```yaml
# mkdocs.yml
plugins:
  - strip-number-prefix:
      pattern: '^\\d{2}\\.'  # Matches: 01.file.md, 99.file.md
      strict: false
```

## File Organization Strategies

### Sequential Numbering

```
docs/
├── 010--introduction.md
├── 020--installation.md
├── 030--configuration.md
├── 040--advanced.md
└── 999--troubleshooting.md
```

### Hierarchical Numbering

```
docs/
├── 100--getting-started.md
├── 110--installation.md
├── 120--first-steps.md
├── 200--configuration.md
├── 210--basic-config.md
├── 220--advanced-config.md
└── 900--appendix.md
```

### Category Prefixes

```
docs/
├── 01--intro/
│   ├── 010--overview.md
│   └── 020--quickstart.md
├── 02--guides/
│   ├── 010--setup.md
│   └── 020--deployment.md
└── 99--reference/
    └── 010--api.md
```

## Compatibility

- **MkDocs**: >= 1.5.0
- **Python**: >= 3.9
- **Works with**:
  - [Material for MkDocs](https://squidfunk.github.io/vexy-mkdocs-material/)
  - [vexy-mkdocs-awesome-nav](https://github.com/lukasgeiter/vexy-mkdocs-awesome-nav)
  - [vexy-mkdocs-nav-weight](https://github.com/shu307/vexy-mkdocs-nav-weight)
  - Most other MkDocs plugins

## Troubleshooting

### Duplicate URLs

```
ERROR: Multiple files would map to 'intro.md': 010--intro.md, 020--intro.md
```

**Solution**: Use unique base names:
- `010--intro-basics.md`
- `020--intro-advanced.md`

### Broken Links

When `strip_links: false` (default), use clean slugs in links:

```markdown
✅ [Next page](configuration.md)
❌ [Next page](030--configuration.md)
```

When `strip_links: true`, both forms work:

```markdown
✅ [Next page](configuration.md)
✅ [Next page](030--configuration.md)  # Auto-converted
```

### Debug Mode

Enable verbose logging:

```yaml
plugins:
  - strip-number-prefix:
      verbose: true
```

This shows:
- File transformations
- URL mappings
- Collision warnings
- Link rewriting

## Development

### Setup

```bash
git clone https://github.com/vexyart/vexy-mkdocs-strip-number-prefix
cd vexy-mkdocs-strip-number-prefix
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .[dev]
pre-commit install
```

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=mkdocs_strip_number_prefix --cov-report=html

# Run specific test
pytest tests/test_plugin.py::TestStripNumberPrefixPlugin::test_default_pattern
```

### Code Quality

```bash
# Format and lint
black src tests
ruff check --fix src tests
mypy src
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Support

- 🐛 **Issues**: [GitHub Issues](https://github.com/vexyart/vexy-mkdocs-strip-number-prefix/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/vexyart/vexy-mkdocs-strip-number-prefix/discussions)
- 📖 **Documentation**: [Project Documentation](https://vexyart.github.io/vexy-mkdocs-strip-number-prefix/)