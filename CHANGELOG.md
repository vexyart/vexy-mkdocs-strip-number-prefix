# Changelog

All notable changes to vexy-mkdocs-strip-number-prefix will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed
- **CRITICAL**: Fixed src_path modification issue that caused FileNotFoundError during MkDocs builds
- Fixed navigation title display to strip numeric prefixes from tab and sidebar navigation
- Fixed test configuration to properly initialize plugin config defaults
- Fixed file path transformation logic to correctly update dest_path and URL
- Fixed collision detection logic in non-strict mode
- Updated GitHub URLs from placeholder to actual repository URLs
- Added proper type annotations and resolved mypy warnings
- Ensured git-tag-based VCS versioning with hatch-vcs works correctly

### Added
- **NEW**: Navigation title stripping via `strip_nav_titles` configuration option (enabled by default)
- **NEW**: `on_nav` hook to clean navigation titles in both tab and sidebar navigation
- Virtual path strategy for collision detection without modifying source paths
- Support for both file format (`010--title`) and navigation format (`010 title`) patterns
- Demo documentation with MkDocs Material theme showcasing plugin functionality
- Pre-commit configuration file with proper project path
- Type ignore comments for MkDocs base plugin inheritance

### Changed
- **BREAKING**: Plugin no longer modifies `src_path` - preserves original file paths on disk
- Enhanced collision detection to use virtual clean paths instead of modified source paths
- Improved file path replacement to use stem-based matching for MkDocs URL structure
- Updated logging to reflect virtual path transformations
- Improved test fixtures to include required src_uri attribute for mock files

## [0.2.0] - 2025-01-14

### Changed
- **BREAKING**: Migrated to src-layout package structure
- **BREAKING**: Minimum Python version is now 3.9
- **BREAKING**: Improved type safety with strict typing
- Modernized packaging with PEP 621 compliant pyproject.toml
- Switched to standard library logging for better integration

### Added
- Comprehensive test suite with >90% coverage
- Pre-commit hooks for code quality
- GitHub Actions CI/CD workflows
- Support for Python 3.9, 3.10, 3.11, and 3.12
- Automated release process with trusted PyPI publishing
- Enhanced documentation with examples and troubleshooting
- Better error messages for collision detection
- Improved link rewriting with anchor support

### Fixed
- Better handling of subdirectory paths
- Improved regex pattern validation
- More robust collision detection
- Enhanced link rewriting for complex markdown structures

## [0.1.0] - 2025-01-10

### Added
- Initial release of vexy-mkdocs-strip-number-prefix plugin
- Core functionality to strip numeric prefixes from URLs while preserving source filenames
- Configurable regex pattern for matching prefixes (default: `^\\d+--`)
- Collision detection with strict/non-strict modes
- Optional internal link rewriting (`strip_links` option)
- Verbose logging mode for debugging
- Comprehensive error handling with helpful messages
- Support for MkDocs 1.5.0+

### Features
- **Pattern Matching**: Flexible regex-based prefix detection
- **Collision Detection**: Prevents duplicate URLs with configurable strictness
- **Link Rewriting**: Automatically updates internal markdown links
- **Debug Mode**: Detailed logging for troubleshooting
- **Type Safety**: Full type hints for better IDE support

[Unreleased]: https://github.com/vexyart/vexy-mkdocs-strip-number-prefix/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/vexyart/vexy-mkdocs-strip-number-prefix/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/vexyart/vexy-mkdocs-strip-number-prefix/releases/tag/v0.1.0