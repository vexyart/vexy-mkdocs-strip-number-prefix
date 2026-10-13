# vexy-mkdocs-strip-number-prefix

`vexy-mkdocs-strip-number-prefix` is an MkDocs plugin. It lets you keep numeric
prefixes such as `010--` in your Markdown filenames and folder names, so the
files sort in the order you want, and removes those prefixes from the URLs and
output paths of the built site.

## What it does

You write your sources like this:

```text
docs/
├── index.md
├── 010--introduction.md
├── 020--getting-started.md
└── 030--guides/
    ├── 010--setup.md
    └── 020--deployment.md
```

The plugin is registered under the name `strip-number-prefix`. With it enabled,
MkDocs writes the site like this:

```text
site/
├── index.html
├── introduction/index.html
├── getting-started/index.html
└── guides/
    ├── setup/index.html
    └── deployment/index.html
```

The source files on disk are not renamed. Only the output path (`dest_path`)
and the page URL (`url`) that MkDocs uses for each page change.

## Features

- **Clean URLs.** A regular expression (default `^\d+--`) is removed from
  every path component of every documentation page.
- **Ordering stays in the filenames.** Prefixes still control the order in
  which MkDocs discovers files and sorts the automatic navigation.
- **Collision detection.** If two files would end up at the same clean path,
  the build stops (`strict: true`, the default) or the plugin logs a warning
  and leaves both files at their prefixed paths (`strict: false`).
- **Navigation titles.** Section titles derived from prefixed folder names,
  such as `030  guides`, are cleaned to `guides` (`strip_nav_titles`, on by
  default).
- **Optional link rewriting.** `strip_links: true` rewrites `.md` link targets
  in the Markdown before MkDocs renders it. Read
  [Links and navigation](050--links-and-navigation.md) before turning it on.

## This site uses the plugin

The source of this documentation lives in `src_docs/md/` of the repository,
and every page except this one has a numeric prefix, for example
`src_docs/md/010--installation.md`. The page is published at
`installation/`, not at `010--installation/`. The configuration is in
`src_docs/mkdocs.yml`.

## Where to go next

| If you want to | Read |
|---|---|
| Install the package | [Installation](010--installation.md) |
| Get a working site in five minutes | [Quickstart](020--quickstart.md) |
| Look up an option | [Configuration](030--configuration.md) |
| Understand what happens during a build | [How it works](040--how-it-works.md) |
| Write links between prefixed pages | [Links and navigation](050--links-and-navigation.md) |
| Fix a collision or a broken link | [Edge cases and troubleshooting](060--edge-cases.md) |
| Replace `mkdocs-awesome-pages-plugin` | [Migrating from awesome-pages](070--migration.md) |

## Requirements

- Python 3.9 or later (`requires-python = ">=3.9"` in `pyproject.toml`).
- MkDocs 1.5.0 or later (the only runtime dependency is `mkdocs>=1.5.0`).
  CI tests the plugin against MkDocs 1.5.x and 1.6.x. This documentation site
  is built with ProperDocs 1.6.7, which loads MkDocs plugins unchanged.

## License

MIT. The source is at
[github.com/vexyart/vexy-mkdocs-strip-number-prefix](https://github.com/vexyart/vexy-mkdocs-strip-number-prefix).
