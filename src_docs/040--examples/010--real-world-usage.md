# Real-World Usage Examples

## Documentation Structure

Here's how you might structure a real project:

```
docs/
├── 010--getting-started/
│   ├── 010--quickstart.md
│   ├── 020--installation.md
│   └── 030--first-steps.md
├── 020--user-guide/
│   ├── 010--basics.md
│   ├── 020--configuration.md
│   └── 030--advanced.md
└── 030--reference/
    ├── 010--api.md
    └── 020--cli.md
```

Results in URLs:
- `/getting-started/quickstart/`
- `/getting-started/installation/`
- `/user-guide/basics/`
- etc.

## Complete Configuration Example

```yaml
site_name: My Documentation
site_url: https://example.com
theme:
  name: material
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.expand

plugins:
  - search
  - strip-number-prefix:
      pattern: '^\d+--'
      strict: true
      strip_links: true

nav:
  - Home: index.md
  - Getting Started:
    - Introduction: 010--getting-started/010--introduction.md
    - Installation: 010--getting-started/020--installation.md
  - User Guide:
    - Basics: 020--user-guide/010--basics.md
```

[Next: Common Patterns](020--common-patterns.md)