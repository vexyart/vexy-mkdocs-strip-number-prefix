
# TODO

## Note

@external/ref/mkdocs-awesome-nav and @external/ref/mkdocs-nav-weight are two plugins that deal with the MkDocs nav system. You may find their codebase useful. @external/ref is a single-file snapshot of these. 

## Recently

We have created a `src_docs` with several subfolders and short Markdown files. They showcase basic features of the Markdown language. We uses the numbers (both in the Markdown files AND in the folder names) to control the sorting, and then we wrote a `build_docs.py` that uses MkDocs and a MkDocs config (in the main folder) to build into `docs`, utilizing our plugin and the MkDocs Material theme. 

## Phase

### Background / Problem Statement

Building the demo documentation (`src_docs`) with MkDocs **failed** because the
`vexy-mkdocs-strip-number-prefix` plugin modified the `src_path` attribute of
`mkdocs.structure.files.File` objects.  When MkDocs subsequently tried to read
the source files via `abs_src_path` it raised a `FileNotFoundError` because the
physical files on disk still contained their numeric prefixes.

### Goal

1. Provide clean, prefix-free URLs and HTML output directories.
2. Keep the on-disk source tree untouched so that MkDocs can read files
   correctly.
3. Detect collisions, handle optional link rewriting and maintain the existing
   public API/test-suite.

### Fix Strategy

1. **Do not touch `src_path`.** Leave it pointing to the real file on disk.
2. **Generate a *virtual* clean path** (all prefixes removed) that will be used
   exclusively to update `dest_path` and `url`.
3. **Perform collision detection** on that virtual path.
4. **Update `dest_path`/`url`** by stripping prefixes from every component but
   preserving file extensions and trailing slashes.
5. **Update test-suite** to reflect the new, correct behaviour (source path
   remains unchanged).
6. **Re-run MkDocs build** to ensure the docs build without errors.

### Implementation Steps

1. Refactor `StripNumberPrefixPlugin.on_files`:
   * Compute `cleaned_virtual_src`.
   * Store `(file, cleaned_virtual_src)` for later processing.
   * Collision detection now uses `cleaned_virtual_src`.
   * New helper `_clean_component` strips prefix while preserving extension.
   * Only `dest_path` and `url` are modified.
2. Adjust verbose logging to reflect new behaviour.
3. Update unit-tests:
   * Expectations for `src_path` changed.
   * Keep coverage ≥ 90 %.
4. Confirm `pytest` and `mkdocs build` both succeed.

### Verification

* `pytest -q` → 14 / 14 tests pass, 94 % coverage.
* `mkdocs build` successfully creates the `docs/` site with clean URLs.

### Future Improvements

* Add end-to-end test that spins up a minimal MkDocs build to catch regressions
  like this automatically.
* Add Windows CI job to ensure path separator handling remains correct (`Path`
  vs `/`).
* Consider exposing a `dry-run` mode that just logs transformations without
  mutating objects (useful for debugging large projects).

