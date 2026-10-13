# Configuration

All options go under the plugin entry in `mkdocs.yml`. This is the full list
with the defaults defined in `StripNumberPrefixPlugin.config_scheme`:

```yaml
plugins:
  - strip-number-prefix:
      pattern: '^\d+--'
      strict: true
      strip_links: false
      strip_nav_titles: true
      verbose: false
      dry_run: false
```

| Option | Type | Default | Effect |
|---|---|---|---|
| `pattern` | string | `^\d+--` | Regular expression that marks the prefix. |
| `strict` | boolean | `true` | Stop the build when two pages map to the same clean path. |
| `strip_links` | boolean | `false` | Rewrite `.md` link targets in the Markdown source. |
| `strip_nav_titles` | boolean | `true` | Remove prefixes from navigation titles. |
| `verbose` | boolean | `false` | Log each transformation at `INFO` level. |
| `dry_run` | boolean | `false` | Log what would change and leave paths, titles and links untouched. |

## `pattern`

A Python regular expression. It is compiled once, in the `on_config` step.
For every documentation page, the plugin splits the source path into its
components (folders and the filename) and, for each component that the
pattern matches **at the start** (`re.match`), removes the matched text.

Example with the default `^\d+--`:

| Source path | Output URL |
|---|---|
| `010--intro.md` | `intro/` |
| `030--guides/020--deploy.md` | `guides/deploy/` |
| `guides/020--deploy.md` | `guides/deploy/` |
| `faq.md` | `faq/` |

!!! warning "Quote the pattern in single quotes"
    In YAML, write `pattern: '^\d+--'`. Inside single quotes a backslash is a
    literal character, so the regular expression receives `^\d+--`. If you
    write `'^\\d+--'`, the regular expression receives two backslashes and
    matches a literal backslash followed by `d`, so nothing is stripped.

An invalid expression stops the build with a `PluginError`:

```text
Invalid regex pattern '<pattern>': <reason>
```

More formats are in [Prefix patterns](080--examples/020--prefix-patterns.md).

## `strict`

Two pages collide when they have the same path after the prefix is removed,
for example `010--intro.md` and `020--intro.md` (both become `intro.md`).

- `strict: true` (default): the build stops with
  `StripNumberPrefix: Multiple files would map to 'intro.md': 010--intro.md, 020--intro.md`.
- `strict: false`: the plugin logs the same message as a warning and does
  **not** clean the colliding pages. They stay at `010--intro/` and
  `020--intro/`. Pages that do not collide are cleaned as usual.

See [Edge cases and troubleshooting](060--edge-cases.md#filename-collisions).

## `strip_links`

When `true`, the plugin rewrites Markdown links of the form `[text](path.md)`
or `[text](path.md#anchor)` before MkDocs renders the page. It removes the
prefix from the **filename only**, not from folder names.

!!! danger "Leave `strip_links` off in most projects"
    MkDocs resolves a link by matching it against the source path of a file,
    which still contains the prefix. A rewritten link such as `intro.md` no
    longer matches `010--intro.md`, so MkDocs reports
    `the target is not found among documentation files` and leaves the link
    unresolved. With the default `strip_links: false`, links to the prefixed
    filenames work and point at the clean URLs.

    Details: [Links and navigation](050--links-and-navigation.md).

## `strip_nav_titles`

When `true` (default), the plugin walks the navigation in its `on_nav` step
and cleans titles that start with a prefix. It recognises two forms:

- A title that matches `pattern`, such as `010--intro`. The prefix is removed,
  `--` is removed and each remaining `-` becomes a space: `intro`.
- A title that starts with digits followed by whitespace, such as
  `030  guides`. This is the form MkDocs produces from a folder named
  `030--guides`. The digits and spaces are removed: `guides`.

Titles you set yourself in `nav:` and titles taken from a page's first
heading normally contain no prefix and are left as they are.

## `verbose`

When `true`, the plugin logs each path change, title change and rewritten
link at `INFO` level through the Python logger
`mkdocs_strip_number_prefix.plugin`.

!!! note
    MkDocs only prints messages from loggers under the `mkdocs` namespace.
    The plugin's own logger is outside it, so in a normal `mkdocs build` these
    `INFO` messages are not printed, even with `mkdocs build -v`. Warnings
    from the plugin (non-strict collisions) are printed without the usual
    `WARNING -` prefix.

## `dry_run`

When `true`, the plugin still detects collisions, but for every page it would
change it logs a `DRY RUN: Would transform ...` message instead of changing
`dest_path` and `url`. Navigation titles and links are also left unchanged.
The site is built with the prefixed URLs. The same logging limitation as for
`verbose` applies.

## A complete example

```yaml
site_name: My documentation
theme:
  name: material
plugins:
  - search
  - strip-number-prefix:
      pattern: '^\d{3}--'
      strict: true
nav:
  - Home: index.md
  - Introduction: 010--introduction.md
  - Guides:
      - Setup: 020--guides/010--setup.md
```

`nav:` entries always name the **source** paths, including prefixes.
