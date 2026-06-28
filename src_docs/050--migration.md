# Migration Guide

## Migrating from mkdocs-awesome-pages-plugin

The [`mkdocs-awesome-pages-plugin`](https://github.com/lukasgeiter/mkdocs-awesome-pages-plugin) and `vexy-mkdocs-strip-number-prefix` solve related but distinct problems. This guide covers the differences and how to switch.

### What awesome-pages does

`awesome-pages` reads a `.pages` YAML file in each directory to control navigation order and titles:

```
docs/
├── .pages          # order: [intro.md, guide.md]
├── intro.md
└── guide.md
```

It does **not** change URLs.

### What strip-number-prefix does

`strip-number-prefix` derives ordering from numeric filename prefixes and strips those prefixes from generated URLs — no sidecar `.pages` files required:

```
docs/
├── 010--intro.md   → URL: /intro/
└── 020--guide.md   → URL: /guide/
```

It does **not** need extra per-directory config files.

### Side-by-side comparison

| Feature | awesome-pages | strip-number-prefix |
|---|---|---|
| Control navigation order | Yes (`.pages` file) | Yes (numeric prefix) |
| Strip prefix from URL | No | Yes |
| Requires sidecar files | Yes (`.pages`) | No |
| Works with subdirectories | Yes | Yes |
| Collision detection | No | Yes (`strict` mode) |
| Rewrite internal links | No | Yes (`strip_links: true`) |
| Strip prefix from nav titles | No | Yes (`strip_nav_titles: true`) |

### Migration steps

1. Remove all `.pages` files from your `docs/` tree.
2. Rename each file by prepending a numeric prefix that matches your desired order:

   ```
   intro.md         → 010--intro.md
   getting-started/ → 020--getting-started/
   ```

3. Replace the plugin in `mkdocs.yml`:

   ```yaml
   # Before
   plugins:
     - search
     - awesome-pages

   # After
   plugins:
     - search
     - strip-number-prefix:
         strip_links: true   # rewrite internal cross-references
   ```

4. Run `mkdocs build` and verify the output URLs are clean.

### Using both plugins together

The plugins are compatible. If you use `awesome-pages` for complex nav re-ordering and `strip-number-prefix` for URL cleaning, load them in this order:

```yaml
plugins:
  - search
  - awesome-pages          # resolves nav order first
  - strip-number-prefix    # then strips prefixes from URLs
```
