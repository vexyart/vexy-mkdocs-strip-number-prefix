# Links and navigation

## Link to the prefixed filename

Write internal links with the **source** filename, prefix included, relative
to the current page:

```markdown
See the [setup guide](030--guides/010--setup.md).
Jump to [installing](030--guides/010--setup.md#installing).
```

MkDocs looks up `030--guides/010--setup.md` among the source files, finds it,
and writes the URL that the plugin assigned to it, for example
`guides/setup/`. Anchors are kept. `mkdocs build --strict` reports no
warnings.

This is how the pages of this site link to each other. The link
[Configuration](030--configuration.md) on this page is written as
`030--configuration.md` and renders as `../configuration/`.

## Do not link to the clean name

A link to `guides/setup.md` does **not** work, because no source file has
that path:

```text
WARNING -  Doc file 'index.md' contains a link 'guides/setup.md', but the target is not found among documentation files.
```

`mkdocs build --strict` treats this warning as an error.

## Why `strip_links: true` breaks links

`strip_links: true` rewrites link targets in the Markdown **before** MkDocs
resolves them. Two things go wrong:

1. The rewritten filename no longer matches any source file.
   `[Intro](010--intro.md)` becomes `[Intro](intro.md)`, and MkDocs cannot
   find `intro.md`.
2. Only the filename is cleaned, not the folders.
   `030--guides/010--setup.md` becomes `030--guides/setup.md`, which matches
   neither the source path nor the clean URL.

A strict build of a page with such links stops:

```text
WARNING -  Doc file 'index.md' contains a link '020--guides/setup.md', but the target is not found among documentation files.

Aborted with 3 warnings in strict mode!
```

Keep `strip_links: false` (the default) and link to prefixed filenames.

## Links from outside the site

URLs that other people bookmark or that you put in a README use the clean
form, because that is what the built site serves:

```text
https://example.com/docs/guides/setup/
```

## Navigation

### Automatic navigation

Without a `nav:` key, MkDocs builds the navigation from the folder structure
and sorts entries by source filename. Prefixes therefore define the order.
`index.md` comes first in each folder.

- Section titles come from folder names. MkDocs turns `030--guides` into
  `030  guides`, and the plugin cleans it to `guides`. The plugin does not
  change the case, so the section appears in lower case.
- Page titles come from the first `#` heading of each page.

### Explicit navigation

With a `nav:` key you choose the titles yourself and refer to the source
paths:

```yaml
nav:
  - Home: index.md
  - Introduction: 010--introduction.md
  - Guides:
      - Setup: 030--guides/010--setup.md
```

The plugin still changes the URLs. Titles from `nav:` have no prefix, so the
title cleaning has nothing to do. This site uses an explicit `nav:`.
