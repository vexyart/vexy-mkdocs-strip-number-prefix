# Code Blocks

## Fenced Code Blocks

```python
def strip_prefix(filename: str, pattern: str = r'^\d+--') -> str:
    """Remove numeric prefix from filename."""
    import re
    return re.sub(pattern, '', filename)
```

## Language Highlighting

```javascript
// JavaScript example
const stripPrefix = (filename, pattern = /^\d+--/) => {
    return filename.replace(pattern, '');
};
```

```yaml
# YAML configuration
plugins:
  - strip-number-prefix:
      pattern: '^\d+--'
      strict: true
```

## Line Numbers

```python linenums="1"
def process_files(files):
    for file in files:
        # Strip the prefix
        clean_name = strip_prefix(file.name)
        # Update the file
        file.url = clean_name
```

## Highlighting Lines

```python hl_lines="2 4"
def important_function():
    # This line is highlighted
    result = calculate_something()
    # This line is also highlighted
    return result * 2
```

[Next: Tables](020--tables.md)