# Installation

Install the plugin using pip:

```bash
pip install mkdocs-strip-number-prefix
```

## Configuration

Add the plugin to your `mkdocs.yml`:

```yaml
plugins:
  - search
  - strip-number-prefix:
      pattern: '^\\d+--'
      strict: true
      strip_links: true
```

## Options Explained

| Option | Default | Description |
|--------|---------|-------------|
| `pattern` | `^\\d+--` | Regex pattern to match and strip |
| `strict` | `false` | Fail on URL collisions |
| `strip_links` | `false` | Rewrite internal markdown links |

## Next: [Configuration Details](030--configuration.md)