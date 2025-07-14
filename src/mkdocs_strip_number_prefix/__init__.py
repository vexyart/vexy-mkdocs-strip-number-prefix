# this_file: more/mkdocs-plugins/vexy-mkdocs-strip-number-prefix/src/mkdocs_strip_number_prefix/__init__.py  # noqa: E501
"""MkDocs Strip Number Prefix Plugin."""

from mkdocs_strip_number_prefix.plugin import StripNumberPrefixPlugin

try:
    from mkdocs_strip_number_prefix._version import __version__
except ImportError:
    __version__ = "0.0.0+unknown"

__all__ = ["StripNumberPrefixPlugin"]
