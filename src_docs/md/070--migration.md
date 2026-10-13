# Migrating from awesome-pages

[`mkdocs-awesome-pages-plugin`](https://github.com/lukasgeiter/mkdocs-awesome-pages-plugin)
and `vexy-mkdocs-strip-number-prefix` solve related problems in different
ways. This page compares them and shows how to switch.

## What each plugin does

`awesome-pages` reads a `.pages` YAML file in each folder to set the order
and titles of navigation entries. It does not change URLs:

```text
docs/
├── .pages          # lists intro.md, then guide.md
├── intro.md        → /intro/
└── guide.md        → /guide/
```

`strip-number-prefix` takes the order from numeric prefixes in the filenames,
which MkDocs already sorts by, and removes the prefixes from the URLs. No
extra files are needed:

```text
docs/
├── 010--intro.md   → /intro/
└── 020--guide.md   → /guide/
```

## Comparison

| Feature | awesome-pages | strip-number-prefix |
|---|---|---|
| Control navigation order | Yes, in `.pages` files | Yes, through filename prefixes |
| Remove prefixes from URLs | No | Yes |
| Needs a file per folder | Yes (`.pages`) | No |
| Works in subfolders | Yes | Yes |
| Detects URL collisions | No | Yes (`strict`) |
| Cleans section titles from folder names | Not applicable | Yes (`strip_nav_titles`) |

## Migration steps

1. Note the order that each `.pages` file defines.
2. Rename the files and folders with numeric prefixes in that order. Leave
   gaps so you can insert pages later:

    ```bash
    git mv docs/intro.md docs/010--intro.md
    git mv docs/getting-started docs/020--getting-started
    ```

3. Update internal links to the new filenames, for example
   `[Intro](intro.md)` becomes `[Intro](010--intro.md)`. MkDocs resolves them
   to the clean URLs. See [Links and navigation](050--links-and-navigation.md).
4. Delete the `.pages` files.
5. Replace the plugin in `mkdocs.yml`:

    ```yaml
    # Before
    plugins:
      - search
      - awesome-pages

    # After
    plugins:
      - search
      - strip-number-prefix
    ```

6. Build with `mkdocs build --strict` and check that the URLs in `site/` have
   no prefixes and that there are no link warnings.

The URLs of renamed pages are the same as before, because the prefix is
removed again. `docs/intro.md` was served at `/intro/`, and
`docs/010--intro.md` is also served at `/intro/`.

## Using both plugins

You can keep `awesome-pages` for features such as custom titles or
collapsing, and add `strip-number-prefix` for the URLs:

```yaml
plugins:
  - search
  - awesome-pages
  - strip-number-prefix
```

The two plugins have not been tested together in this repository's test
suite. Build with `--strict` and check the navigation and URLs after adding
both.
