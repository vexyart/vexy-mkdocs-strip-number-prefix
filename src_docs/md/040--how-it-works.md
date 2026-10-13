# How it works

The plugin is a single class, `StripNumberPrefixPlugin`, in
`src/mkdocs_strip_number_prefix/plugin.py`. It subclasses MkDocs'
`BasePlugin` and implements four MkDocs events. This page follows one file,
`030--guides/010--setup.md`, through a build with the default options.

## The three paths of a page

MkDocs keeps three related values for every file:

| Attribute | Meaning | Example before | Changed by the plugin? |
|---|---|---|---|
| `src_path` | Where MkDocs reads the source on disk | `030--guides/010--setup.md` | No |
| `dest_path` | Where the HTML is written inside `site_dir` | `030--guides/010--setup/index.html` | Yes |
| `url` | The URL used in links, navigation and the sitemap | `030--guides/010--setup/` | Yes |

`src_path` must stay unchanged. If it were cleaned, MkDocs would look for
`guides/setup.md` on disk and fail with `FileNotFoundError`. An early version
of the plugin did exactly that; the changelog lists the fix.

## 1. `on_config`: compile the pattern

The value of `pattern` is compiled with `re.compile`. If compilation fails,
the plugin raises `PluginError("Invalid regex pattern ...")` and the build
stops before any file is read.

## 2. `on_files`: compute and apply clean paths

This is where the URLs change. The step has three passes.

**Pass 1: collect.** For each file where `is_documentation_page()` is true
(Markdown pages; images, CSS and other assets are skipped), the plugin
splits `src_path` into components and removes the prefix from each component
that the pattern matches:

```text
030--guides/010--setup.md
   │            │
   ▼            ▼
guides   /   setup.md        → virtual clean path: guides/setup.md
```

Only files whose clean path differs from `src_path` are kept for the next
passes. `index.md` and other unprefixed files are not touched.

**Pass 2: detect collisions.** The clean paths are grouped. If two or more
source files share one clean path, the plugin records a collision:

- with `strict: true` it raises
  `PluginError("StripNumberPrefix: Multiple files would map to ...")`;
- with `strict: false` it logs the same text as a warning.

**Pass 3: apply.** For every collected file that is not part of a collision
(and only when `dry_run` is off), the plugin rewrites `dest_path` and `url`
component by component. For a component with a file extension, the prefix is
removed from the stem and the extension is kept:

```text
dest_path  030--guides/010--setup/index.html  →  guides/setup/index.html
url        030--guides/010--setup/            →  guides/setup/
```

The trailing `/` that `use_directory_urls: true` adds to the URL is kept.
With `use_directory_urls: false` the same rules give
`guides/setup.html`.

## 3. `on_nav`: clean navigation titles

If `strip_nav_titles` is on, the plugin walks the navigation tree
recursively. Any item whose title starts with the prefix pattern, or with
digits followed by whitespace, gets a cleaned title. A folder named
`030--guides` arrives here as the section title `030  guides` and leaves as
`guides`.

Page titles that MkDocs takes from a page's first `#` heading are set later,
when the page is read, so they are not affected by this step. A page without
a heading and without a `nav:` title keeps a title derived from its filename,
for example `010  setup`. Give every page a first-level heading to avoid
this.

## 4. `on_page_markdown`: rewrite links (optional)

If `strip_links` is on, the plugin runs one regular expression over the
Markdown of each page:

```text
\[([^\]]+)\]\(([^)]+\.md(?:#[^)]*)?)\)
```

For each match, it removes the prefix from the filename part of the target
and keeps the folder part and any `#anchor`:

```text
[Setup](030--guides/010--setup.md#install)  →  [Setup](030--guides/setup.md#install)
```

This happens before MkDocs resolves links, which is why the option usually
breaks links. See [Links and navigation](050--links-and-navigation.md).

## Order relative to other plugins

MkDocs runs plugins in the order they are listed under `plugins:`. The
plugin changes `dest_path` and `url` in `on_files`, so plugins listed after
it see the clean values. If another plugin builds the navigation or copies
pages by path, test both orders.
