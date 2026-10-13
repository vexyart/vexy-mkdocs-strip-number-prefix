# Quickstart

This walk-through builds a small MkDocs site with prefixed filenames and
checks that the output URLs are clean.

## Prerequisites

- The plugin and MkDocs are installed in the same environment. See
  [Installation](010--installation.md).
- An empty working folder.

## Steps

1. Create the source folder and three pages:

    ```bash
    mkdir -p docs/030--guides
    printf '# Home\n\nRead the [introduction](010--introduction.md).\n' > docs/index.md
    printf '# Introduction\n\nNext: [setup](030--guides/010--setup.md).\n' > docs/010--introduction.md
    printf '# Setup\n\nBack to the [introduction](../010--introduction.md).\n' > docs/030--guides/010--setup.md
    ```

2. Create `mkdocs.yml` next to the `docs` folder:

    ```yaml
    site_name: Prefix demo
    plugins:
      - search
      - strip-number-prefix
    ```

    Listing `strip-number-prefix` without options uses the defaults:
    `pattern: '^\d+--'`, `strict: true`, `strip_links: false`,
    `strip_nav_titles: true`, `verbose: false`, `dry_run: false`.

3. Build the site:

    ```bash
    mkdocs build --strict
    ```

    The build finishes without warnings. The links in step 1 point at the
    prefixed source files, and MkDocs resolves them to the clean URLs.

4. List the generated pages:

    ```bash
    find site -name index.html | sort
    ```

    Result:

    ```text
    site/guides/setup/index.html
    site/index.html
    site/introduction/index.html
    ```

    No `010--` or `030--` appears in the output paths.

5. Look at a link in the home page:

    ```bash
    grep -o 'href="introduction/"' site/index.html
    ```

    The link written as `010--introduction.md` was rendered as
    `introduction/`.

## What happened

- MkDocs collected `index.md`, `010--introduction.md` and
  `030--guides/010--setup.md` from `docs/`.
- In its `on_files` step, the plugin removed `010--` and `030--` from each
  path component and set the new `dest_path` and `url` of each file.
- MkDocs converted each Markdown link that names a source file into the URL
  of that file, so the links follow the clean URLs automatically.
- In the navigation, the folder `030--guides` became the section `guides`.

## Next steps

- Change the prefix format or turn on collision warnings:
  [Configuration](030--configuration.md).
- Learn the link rules: [Links and navigation](050--links-and-navigation.md).
