# Best Practices

## File Naming Conventions

### Do's ✅

- Use consistent padding: `010--`, `020--`, not `10--`, `20--`
- Leave gaps for future files: `010--`, `020--`, `030--`
- Use descriptive names after prefix: `010--getting-started.md`
- Group related content with similar prefixes

### Don'ts ❌

- Don't mix patterns in same project
- Don't use same numbers in same directory
- Don't rely on prefixes for security
- Don't use special characters in prefixes

## Organization Tips

### Recommended Structure

```
010--basics/
  010--introduction.md
  020--quickstart.md
  030--installation.md
020--features/
  010--core-features.md
  020--advanced-features.md
030--api/
  010--rest-api.md
  020--graphql-api.md
```

### Navigation Alignment

Keep your `mkdocs.yml` nav aligned with file structure:

```yaml
nav:
  - Basics:
    - Introduction: 010--basics/010--introduction.md
    - Quick Start: 010--basics/020--quickstart.md
  - Features:
    - Core: 020--features/010--core-features.md
```

## Performance Considerations

- The plugin processes files once during build
- Regex compilation is cached
- No runtime performance impact
- Compatible with MkDocs caching

## Summary

The strip-number-prefix plugin helps maintain organized documentation with clean URLs. Follow these practices for best results!

[Previous: Common Patterns](020--common-patterns.md) | [Back to Examples](../040--examples/) | [Home](../)