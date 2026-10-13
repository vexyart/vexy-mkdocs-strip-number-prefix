# Installation

The plugin is published on PyPI as `vexy-mkdocs-strip-number-prefix`. The
import package is `mkdocs_strip_number_prefix`, and the MkDocs plugin name is
`strip-number-prefix`.

## Prerequisites

- Python 3.9 or later.
- MkDocs 1.5.0 or later. Installing the plugin pulls in `mkdocs>=1.5.0` if it
  is missing.

## Install from PyPI

=== "uv"

    ```bash
    uv pip install --upgrade vexy-mkdocs-strip-number-prefix
    ```

=== "pip"

    ```bash
    python -m pip install --upgrade vexy-mkdocs-strip-number-prefix
    ```

=== "uvx (no install)"

    Run MkDocs with the plugin in a throwaway environment:

    ```bash
    uvx --from mkdocs --with vexy-mkdocs-strip-number-prefix mkdocs build
    ```

## Install from source

To use the latest commit from the `main` branch:

```bash
python -m pip install git+https://github.com/vexyart/vexy-mkdocs-strip-number-prefix
```

To work on the plugin itself, clone the repository and install it in editable
mode with the development extras:

```bash
git clone https://github.com/vexyart/vexy-mkdocs-strip-number-prefix
cd vexy-mkdocs-strip-number-prefix
python -m pip install -e ".[dev]"
```

The `dev` extra installs `pytest`, `pytest-cov`, `pytest-mock`, `pyyaml`,
`ruff`, `black`, `mypy` and `pre-commit`. See [Development](090--development.md).

## Check the installation

1. Print the installed version:

    ```bash
    python -c "import mkdocs_strip_number_prefix as m; print(m.__version__)"
    ```

    The version comes from the git tag the package was built from. A source
    checkout without the generated `_version.py` file reports `0.0.0+unknown`.

2. Confirm that MkDocs can find the plugin. The package registers this entry
   point in the `mkdocs.plugins` group:

    ```toml
    [project.entry-points."mkdocs.plugins"]
    strip-number-prefix = "mkdocs_strip_number_prefix.plugin:StripNumberPrefixPlugin"
    ```

    If MkDocs reports `The "strip-number-prefix" plugin is not installed`, the
    plugin is installed in a different Python environment from the one that
    runs `mkdocs`. Install both into the same environment.

## Next step

Continue with the [Quickstart](020--quickstart.md).
