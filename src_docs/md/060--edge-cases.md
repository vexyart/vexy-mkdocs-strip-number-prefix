# Edge cases and troubleshooting

This page lists situations where the result is not obvious, and what to do
about them.

## Filename collisions

A collision happens when two source files have the same path after the
prefix is removed:

```text
docs/
├── 010--intro.md   → intro.md
└── 020--intro.md   → intro.md   ← collision
```

### With `strict: true` (default)

The build stops:

```text
ERROR   -  StripNumberPrefix: Multiple files would map to 'intro.md': 010--intro.md, 020--intro.md

Aborted with a BuildError!
```

The command exits with a non-zero status, so a CI job fails before
deployment. To fix it, give the files different names after the prefix:

```text
docs/
├── 010--intro-basics.md     → intro-basics/
└── 020--intro-advanced.md   → intro-advanced/
```

### With `strict: false`

The plugin prints the same message as a warning and continues. **Neither**
colliding file is cleaned; both stay at their prefixed URLs:

```text
site/010--intro/index.html
site/020--intro/index.html
```

All other pages are cleaned normally. Use this mode only when you accept
prefixed URLs for the colliding pages.

### Folder collisions

Folders are cleaned the same way, so `010--guides/index.md` and
`020--guides/index.md` both become `guides/index.md` and collide. The same
`strict` rules apply.

## A link warns "target is not found"

```text
WARNING -  Doc file 'index.md' contains a link 'guides/setup.md', but the target is not found among documentation files.
```

The link uses a clean name. Link to the source filename instead:
`030--guides/010--setup.md`. If the link was written with a prefix and the
warning shows it without one, `strip_links: true` rewrote it; set
`strip_links: false`. See [Links and navigation](050--links-and-navigation.md).

## Nothing is stripped

Check, in this order:

1. The plugin is listed under `plugins:`. A `plugins:` key replaces MkDocs'
   default list, so also list `search` if you want search.
2. The pattern is written in single quotes with one backslash:
   `pattern: '^\d+--'`. The form `'^\\d+--'` matches nothing in normal
   filenames.
3. The pattern matches from the **start** of each path component. `^\d+--`
   does not match `intro--010.md`.
4. `dry_run` is `false`.
5. The file is a Markdown page. Images, stylesheets and other assets keep
   their prefixes. Link to them by their real, prefixed path.

## A navigation entry still shows digits

A page with no `#` heading and no title in `nav:` gets a title from its
filename, for example `010  setup`. The plugin cleans titles before MkDocs
reads the pages, so this title is not cleaned. Add a first-level heading to
the page, or set the title in `nav:`.

## Section titles are in lower case

MkDocs builds a section title such as `030  guides` from the folder name
`030--guides`. The plugin removes `030  ` but does not change the case, so the
section is shown as `guides`. Set the title in `nav:` to control it.

## `verbose` or `dry_run` print nothing

The plugin logs through the Python logger
`mkdocs_strip_number_prefix.plugin`. MkDocs only shows messages from the
`mkdocs` logger tree, so the plugin's `INFO` messages are not shown, even
with `mkdocs build -v`. Warnings are shown, without the `WARNING -` prefix.
To see what `dry_run` would change, compare the output folder of a build with
and without the plugin instead.

## Zero-padded prefixes such as `00--`

`^\d+--` matches one or more digits, so `00--`, `000--` and `0001--` are all
stripped. Files sort by name, so `00--preface.md` comes before
`010--intro.md`. This gives you a slot before the main sequence.

## A filename that is only a prefix

`010--.md` has the stem `010--`. After stripping, the name is empty and is
dropped from the output path, so the page is written to the `index.html` of
its folder. At the top level that overwrites the home page. Always put a name
after the prefix: `010--overview.md`.

## The pattern applies per component

The pattern is applied to each folder name and the filename separately, never
to the whole path. In `010--guides/020--setup.md`, the components
`010--guides` and `020--setup.md` are cleaned independently, giving
`guides/setup.md`. A pattern that contains `/` cannot match.

## External and non-Markdown links

With `strip_links: true`, only link targets that end in `.md` (optionally
followed by `#anchor`) are rewritten. `https://` links and links to other file
types, such as `asset.zip`, are not touched.
