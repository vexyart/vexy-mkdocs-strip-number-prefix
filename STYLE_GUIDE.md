# this_file: STYLE_GUIDE.md

# Documentation Style Guide

Guidelines for writing documentation and code in this repository.

## File naming convention

Source files use `NNN--slug.md` where `NNN` is a zero-padded integer and `slug` is a lowercase kebab-case description:

```
010--introduction.md
020--getting-started.md
030--configuration.md
```

- Use multiples of 10 to leave room for insertions.
- Directory names follow the same convention: `010--guides/`.
- Never use `00--` for the primary first file; reserve it for preamble/preface material.

## Prose style

- **Lead with the outcome**, not the mechanism. Say "Clean URLs appear automatically" before explaining how.
- **Active voice**. "The plugin strips the prefix" not "The prefix is stripped by the plugin."
- **Short sentences**. One idea per sentence. Split compound sentences.
- **Code examples first**. Show the `mkdocs.yml` snippet before explaining each option in prose.
- **No hype**. Describe what the plugin does; let the reader judge whether it is useful.

## Code examples

All `mkdocs.yml` snippets must include a `plugins:` block context:

```yaml
# good
plugins:
  - strip-number-prefix:
      pattern: '^\d+--'

# avoid — no context
strip-number-prefix:
  pattern: '^\d+--'
```

Python code examples use `f-strings`, `pathlib.Path`, and type hints.

## Option documentation

Every configuration option must appear in three places:
1. The option table in `README.md` with type, default, and one-line description.
2. The reference page in `src_docs/` with a full explanation and example.
3. The docstring in `plugin.py` (in the `config_scheme` tuple comment).

## Changelog entries

Follow [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format:

- `Added` — new features.
- `Changed` — changes to existing behaviour.
- `Fixed` — bug fixes.
- `Deprecated` — soon-to-be-removed features.
- `Removed` — now-removed features.
- `Security` — vulnerability fixes.

Do not describe *how* something was fixed; describe *what changed* for the user.

## Source file header

Every Python file must start with:

```python
# this_file: src/mkdocs_strip_number_prefix/plugin.py
"""One-line module docstring."""
```

The `this_file` comment uses the path relative to the repository root, with no leading `./`.

## Type hints

All public functions and methods carry full type annotations. Private helpers
(prefixed `_`) should also be annotated where the type is non-obvious. Use
`from __future__ import annotations` only if needed for forward references.
