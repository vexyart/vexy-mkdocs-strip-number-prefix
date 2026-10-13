# Prefix patterns

The `pattern` option takes any Python regular expression. It is tested with
`re.match` against each path component, so it only has to describe the start
of a name. Starting it with `^` makes that explicit.

Write patterns in single-quoted YAML strings with single backslashes.

## Common formats

| Pattern | Matches | Example source → URL |
|---|---|---|
| `'^\d+--'` (default) | Any number of digits, then `--` | `123--file.md` → `file/` |
| `'^\d{3}--'` | Exactly three digits, then `--` | `001--file.md` → `file/` |
| `'^\d+-'` | Digits, then one `-` | `42-file.md` → `file/` |
| `'^\d+_'` | Digits, then `_` | `01_file.md` → `file/` |
| `'^[0-9]{2,4}-'` | Two to four digits, then `-` | `0001-file.md` → `file/` |

## Three-digit prefixes only

```yaml
plugins:
  - strip-number-prefix:
      pattern: '^\d{3}--'
```

`010--intro.md` becomes `intro/`. `10--intro.md` does not match and keeps
its prefix in the URL. Use this to make sure all names use the same width.

## Single-dash prefixes

```yaml
plugins:
  - strip-number-prefix:
      pattern: '^\d+-'
```

`01-intro.md` becomes `intro/`. Be careful with names that start with a
number as part of the title, such as `2024-review.md`: it becomes `review/`.
The double dash in the default pattern avoids that.

## Patterns that end in a dot do not work

```yaml
plugins:
  - strip-number-prefix:
      pattern: '^\d+\.'   # does not clean URLs
```

With `1.intro.md`, the plugin detects the prefix, but the URLs stay
`1.intro/`. When the plugin cleans `dest_path` and `url`, it treats the text
after the last dot of a component as a file extension and applies the pattern
to the part before it. For the URL component `1.intro`, that part is `1`,
which does not match `^\d+\.`. Use a separator other than `.`, such as `--`,
`-` or `_`.

## Choosing a pattern

- Keep one pattern for the whole project. The plugin has one `pattern`
  option and applies it everywhere.
- Prefer a separator that does not occur naturally at the start of names.
  `--` is a good choice.
- After changing the pattern, run `mkdocs build --strict`. A pattern that
  is too broad can make two pages collide, and strict mode reports it.
