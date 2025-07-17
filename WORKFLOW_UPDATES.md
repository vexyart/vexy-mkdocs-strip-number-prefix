# GitHub Actions Workflow Updates

The GitHub App doesn't have `workflows` permission to modify GitHub Actions files. Please apply these updates manually:

## 1. Update `.github/workflows/ci.yml`

Replace the current content with:

```yaml
# this_file: .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

permissions:
  contents: read

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ["3.9", "3.10", "3.11", "3.12"]
        include:
          # Add Python 3.13 for Ubuntu only (faster feedback)
          - os: ubuntu-latest
            python-version: "3.13"

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Required for hatch-vcs

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Cache pip packages
        uses: actions/cache@v4
        with:
          path: |
            ~/.cache/pip
            ~\AppData\Local\pip\Cache
            ~/Library/Caches/pip
          key: ${{ matrix.os }}-pip-${{ hashFiles('**/pyproject.toml') }}
          restore-keys: |
            ${{ matrix.os }}-pip-

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -e .[dev]

      - name: Run pre-commit
        if: matrix.python-version == '3.11' && matrix.os == 'ubuntu-latest'
        run: pre-commit run --all-files

      - name: Run tests
        run: |
          pytest -v --cov=mkdocs_strip_number_prefix --cov-report=xml --cov-report=term

      - name: Upload coverage
        if: matrix.python-version == '3.11' && matrix.os == 'ubuntu-latest'
        uses: codecov/codecov-action@v4
        with:
          file: ./coverage.xml
          fail_ci_if_error: true
          token: ${{ secrets.CODECOV_TOKEN }}

  # Separate job for code quality to fail fast
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Cache pip packages
        uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ubuntu-latest-pip-lint-${{ hashFiles('**/pyproject.toml') }}
          restore-keys: |
            ubuntu-latest-pip-lint-

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -e .[dev]

      - name: Run ruff
        run: ruff check --output-format=github .

      - name: Run black
        run: black --check --diff .

      - name: Run mypy
        run: mypy src

  # Build job to ensure package builds correctly
  build:
    runs-on: ubuntu-latest
    needs: [test, lint]
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install build dependencies
        run: |
          python -m pip install --upgrade pip
          pip install build twine

      - name: Build package
        run: python -m build

      - name: Check package
        run: twine check dist/*

      - name: Upload build artifacts
        uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/
          retention-days: 30

  # Security scanning
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Bandit Security Scan
        uses: securecodewarrior/github-action-bandit@v1.0.1
        with:
          exit_zero: true

      - name: Run Safety Check
        run: |
          python -m pip install safety
          safety check --json || true
```

## 2. Update `.github/workflows/release.yml`

Replace the current content with:

```yaml
# this_file: .github/workflows/release.yml
name: Release

on:
  push:
    tags:
      - 'v*'

permissions:
  contents: write
  id-token: write  # Required for PyPI trusted publishing

jobs:
  # Run tests before release
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -e .[dev]

      - name: Run tests
        run: pytest -v --cov=mkdocs_strip_number_prefix

      - name: Run linting
        run: |
          ruff check .
          black --check .
          mypy src

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Required for hatch-vcs

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install build dependencies
        run: |
          python -m pip install --upgrade pip
          pip install build twine

      - name: Build package
        run: python -m build

      - name: Check package
        run: twine check dist/*

      - name: Upload artifacts
        uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/

  publish-pypi:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: pypi
      url: https://pypi.org/p/vexy-mkdocs-strip-number-prefix
    steps:
      - name: Download artifacts
        uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist/

      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          attestations: true  # Generate attestations for transparency
        # Trusted publishing configured in PyPI project settings

  create-release:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Download artifacts
        uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist/

      - name: Extract changelog section
        id: changelog
        run: |
          version=${GITHUB_REF#refs/tags/v}
          echo "version=$version" >> $GITHUB_OUTPUT
          
          # Extract release notes from CHANGELOG.md
          if [[ -f CHANGELOG.md ]]; then
            awk "/## \[$version\]/{flag=1; next} /## \[/{flag=0} flag" CHANGELOG.md > release_notes.md
            if [[ ! -s release_notes.md ]]; then
              echo "Release notes for version $version not found in CHANGELOG.md" > release_notes.md
            fi
          else
            echo "Release $version" > release_notes.md
          fi

      - name: Create Release
        uses: softprops/action-gh-release@v2
        with:
          name: v${{ steps.changelog.outputs.version }}
          body_path: release_notes.md
          files: dist/*
          draft: false
          prerelease: ${{ contains(steps.changelog.outputs.version, '-') }}
          generate_release_notes: true
          make_latest: true

  # Post-release notifications
  post-release:
    needs: [publish-pypi, create-release]
    runs-on: ubuntu-latest
    if: always()
    steps:
      - name: Extract version
        id: version
        run: echo "version=${GITHUB_REF#refs/tags/v}" >> $GITHUB_OUTPUT

      - name: Release Summary
        run: |
          echo "## Release Summary" >> $GITHUB_STEP_SUMMARY
          echo "- **Version**: ${{ steps.version.outputs.version }}" >> $GITHUB_STEP_SUMMARY
          echo "- **PyPI**: https://pypi.org/project/vexy-mkdocs-strip-number-prefix/${{ steps.version.outputs.version }}/" >> $GITHUB_STEP_SUMMARY
          echo "- **GitHub**: https://github.com/vexyart/vexy-mkdocs-strip-number-prefix/releases/tag/v${{ steps.version.outputs.version }}" >> $GITHUB_STEP_SUMMARY
```

## 3. Create `.github/dependabot.yml` (if it doesn't exist)

Create this file with:

```yaml
# this_file: .github/dependabot.yml
version: 2
updates:
  # Enable version updates for pip dependencies
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
      time: "09:00"
    open-pull-requests-limit: 10
    reviewers:
      - "vexyart"
    assignees:
      - "vexyart"
    commit-message:
      prefix: "chore(deps)"
      include: "scope"
    labels:
      - "dependencies"
      - "python"
    
  # Enable version updates for GitHub Actions
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
      time: "09:00"
    open-pull-requests-limit: 5
    reviewers:
      - "vexyart"
    assignees:
      - "vexyart"
    commit-message:
      prefix: "chore(deps)"
      include: "scope"
    labels:
      - "dependencies"
      - "github-actions"
```

## Key Changes Made:

1. **Enhanced CI workflow** with multiplatform testing (Ubuntu, Windows, macOS)
2. **Added Python 3.13 support** for Ubuntu
3. **Separate lint job** for fast-fail code quality checks
4. **Build validation** with artifact uploads
5. **Security scanning** with Bandit and Safety
6. **Enhanced release workflow** with pre-release testing
7. **PyPI attestations** for transparency
8. **Automated dependency updates** with Dependabot

## How to Apply:

1. Navigate to your repository on GitHub
2. Edit each workflow file directly in the GitHub interface
3. Copy and paste the respective content
4. Commit the changes

The system will then be fully functional with comprehensive CI/CD capabilities!