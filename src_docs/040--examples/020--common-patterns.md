# Common Patterns

## Different Prefix Formats

### Three-Digit Prefixes
```yaml
pattern: '^\d{3}--'  # Matches: 001--file.md, 010--file.md
```

### Underscore Separator
```yaml
pattern: '^\d+_'     # Matches: 01_file.md, 10_file.md
```

### Dot Notation
```yaml
pattern: '^\d+\.'    # Matches: 1.file.md, 10.file.md
```

### Complex Patterns
```yaml
pattern: '^[0-9]{2,4}-'  # Matches: 01-file.md, 0001-file.md
```

## Migration Strategy

When migrating existing docs:

1. **Add prefixes gradually**:
   ```bash
   mv introduction.md 010--introduction.md
   mv installation.md 020--installation.md
   ```

2. **Enable link rewriting**:
   ```yaml
   strip_links: true  # Automatically updates internal links
   ```

3. **Test with strict mode**:
   ```yaml
   strict: true  # Catches any URL collisions
   ```

## Troubleshooting

### URL Collisions

If you get collision errors:
```
Error: URL collision detected
- 010--setup.md -> setup/
- 020--setup.md -> setup/  # Collision!
```

Solution: Use unique names after the prefix.

[Previous: Real-World Usage](010--real-world-usage.md) | [Next: Best Practices](030--best-practices.md)