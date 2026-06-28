# Edge Cases

This page documents known edge cases and how the plugin handles them.

## Zero-padded prefix `00--`

Files named with a `00--` prefix are valid and processed normally:

```
docs/
├── 00--preface.md    → URL: /preface/
├── 010--intro.md     → URL: /intro/
└── 020--guide.md     → URL: /guide/
```

The default pattern `^\d+--` matches one or more digits, so `00`, `000`, `0001` all match. Filesystem sort order places `00--` files before `010--` files, giving you a slot before your main numbered sequence.

## Filename collisions

A collision occurs when two source files produce the same clean URL after prefix removal:

```
docs/
├── 010--intro.md   → intro/
└── 020--intro.md   → intro/   ← COLLISION
```

### Strict mode (default: `strict: true`)

The build fails immediately with a clear error:

```
ERROR - Plugin error: StripNumberPrefix: Multiple files would map to 'intro.md': 010--intro.md, 020--intro.md
```

**Resolution**: Use unique base names:

```
docs/
├── 010--intro-basics.md    → intro-basics/
└── 020--intro-advanced.md  → intro-advanced/
```

### Non-strict mode (`strict: false`)

The plugin logs a warning and keeps the first file (in MkDocs filesystem order). The second file is left at its original prefixed URL:

```
WARNING - StripNumberPrefix: Multiple files would map to 'intro.md': 010--intro.md, 020--intro.md
```

Use non-strict mode only if you intentionally want some prefixed files to remain exposed at their original URLs.

## Directory prefix collisions

Collisions can also occur between directory names:

```
docs/
├── 010--guides/
│   └── index.md     → guides/
└── 020--guides/     ← COLLISION — both strip to "guides/"
    └── index.md
```

The same strict/non-strict rules apply.

## Empty result after stripping

If a prefix matches the entire filename stem (e.g. `010--.md`), the stripped filename becomes empty. The plugin passes an empty string to MkDocs, which may produce unpredictable URL behaviour. Use base names with content: `010--my-page.md`, never `010--.md`.

## Pattern matches path separators

The prefix pattern is applied **per path component**, not to the entire path. A file at `010--guides/020--setup.md` has two components: `010--guides` and `020--setup.md`. Each is processed independently.

## Links with anchors (`#section`)

When `strip_links: true`, anchor fragments are preserved:

```markdown
[See config](020--configuration.md#options)
→ [See config](configuration.md#options)
```

## External links are untouched

The link rewriter only processes `.md` links. HTTP/HTTPS URLs and other non-Markdown links are ignored:

```markdown
[External](https://example.com)   ← unchanged
[Download](asset.zip)             ← unchanged (not .md)
[Docs](010--docs.md)              ← rewritten to docs.md
```

## Strict mode failure message

The exact error text for collision failures (useful for `grep` in CI):

```
Plugin error: StripNumberPrefix: Multiple files would map to '<slug>': <file1>, <file2>
```

The build exits with a non-zero return code, blocking deployment.
