# Configuration Details

## Basic Setup

The simplest configuration just enables the plugin:

```yaml
plugins:
  - strip-number-prefix
```

## Advanced Configuration

### Custom Patterns

You can customize the prefix pattern:

```yaml
plugins:
  - strip-number-prefix:
      pattern: '^\\d{3}_'  # Matches 001_filename.md
```

### Strict Mode

Enable strict mode to catch URL collisions:

```yaml
plugins:
  - strip-number-prefix:
      strict: true  # Build fails if two files map to same URL
```

### Link Rewriting

Automatically update internal links:

```yaml
plugins:
  - strip-number-prefix:
      strip_links: true  # Rewrites [text](010--file.md) to [text](file.md)
```

---

[Back to Getting Started](./) | [Next: Basic Syntax](../020--basic-syntax/)