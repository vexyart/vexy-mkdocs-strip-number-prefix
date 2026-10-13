# Development

## Repository layout

| Path | Contents |
|---|---|
| `src/mkdocs_strip_number_prefix/plugin.py` | The plugin class `StripNumberPrefixPlugin` |
| `src/mkdocs_strip_number_prefix/__init__.py` | Re-exports the class and `__version__` |
| `tests/test_plugin.py` | Unit tests and an end-to-end MkDocs build test |
| `src_docs/md/` | Source of this documentation (prefixed filenames) |
| `src_docs/mkdocs.yml` | Documentation configuration |
| `src_docs/build.sh` | Builds the documentation into `docs/` |
| `docs/` | Built documentation, served by GitHub Pages |
| `build.sh`, `publish.sh` | Build and release scripts |
| `scripts/` | Older helper scripts used by the `Makefile` |

## Set up

1. Clone the repository:

    ```bash
    git clone https://github.com/vexyart/vexy-mkdocs-strip-number-prefix
    cd vexy-mkdocs-strip-number-prefix
    ```

2. Install the package in editable mode with the development extras:

    ```bash
    python -m pip install -e ".[dev]"
    ```

    `make setup` and `./scripts/dev.sh setup` do the same through the helper
    scripts.

3. Optionally install the pre-commit hooks:

    ```bash
    pre-commit install
    ```

## Run the tests

```bash
python -m pytest
```

or, without a prepared environment:

```bash
uvx hatch test
```

`tests/test_plugin.py` covers pattern compilation, path cleaning in
subfolders, collision handling in both modes, link rewriting, navigation
title cleaning and a full MkDocs build. Coverage settings are in
`pyproject.toml` (`fail_under = 90` for `pytest --cov`).

## Lint and format

```bash
ruff check src tests
black src tests
mypy src
```

`make lint` and `make format` wrap these.

## Build the documentation

```bash
src_docs/build.sh          # strict build into docs/
src_docs/build.sh serve    # live preview on http://127.0.0.1:8000
./build.sh docs            # same as the first command
```

`src_docs/build.sh` runs ProperDocs with the MaterialX theme through `uvx`.
It installs the plugin from the repository checkout (`--with ..`), so the
documentation is always built with the current source of the plugin. The
build is strict: any warning, such as a broken link, fails it.

On every push to `main` that changes `src_docs/`, the GitHub workflow
`.github/workflows/docs.yml` runs the same script and commits the rebuilt
`docs/` folder. GitHub Pages serves it at
<https://vexy.dev/vexy-mkdocs-strip-number-prefix/>.

## Build the package

```bash
./build.sh package
```

This removes `dist/`, runs `uv build` and checks the result with
`uvx twine check dist/*`. `./build.sh` without an argument builds both the
documentation and the package.

## Versions

The version is not written in `pyproject.toml`. `hatch-vcs` derives it from
the latest git tag at build time and writes it to
`src/mkdocs_strip_number_prefix/_version.py`, which is not committed. A build
from the tag `v1.0.13` produces version `1.0.13`; a build from a later commit
produces a development version such as `1.0.14.dev2+g1a2b3c4`.

## Release

1. Make sure the tests pass and `CHANGELOG.md` describes the changes.
2. Set a PyPI token for `uv publish`, for example in `UV_PUBLISH_TOKEN`.
3. Run:

    ```bash
    ./publish.sh
    ```

    `publish.sh` runs `uvx gitnextver`, which commits pending changes, creates
    the next `vX.Y.Z` tag and pushes it. It then builds the package from that
    tag with `./build.sh package` and uploads `dist/*` with `uv publish`.

Pushing a `v*` tag also starts `.github/workflows/release.yml`, which builds
the package, uploads it to PyPI with trusted publishing
(`skip-existing: true`, so a version already uploaded by `publish.sh` does not
fail the job) and creates a GitHub release.

## Contributing

1. Fork the repository and create a branch.
2. Add tests for new behaviour in `tests/test_plugin.py`.
3. Run the tests and linters.
4. If the change affects users, update `CHANGELOG.md` and the pages in
   `src_docs/md/`, and run `src_docs/build.sh`.
5. Open a pull request.
