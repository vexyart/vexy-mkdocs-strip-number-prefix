# this_file: more/mkdocs-plugins/vexy-mkdocs-strip-number-prefix/src/mkdocs_strip_number_prefix/plugin.py
"""Plugin to strip numeric prefixes from page URLs while keeping them in source files."""

import logging
import re
from collections import defaultdict
from pathlib import Path
from re import Pattern
from typing import Optional

from mkdocs.config import config_options
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.exceptions import PluginError
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import File, Files
from mkdocs.structure.pages import Page

logger = logging.getLogger(__name__)


class StripNumberPrefixPlugin(BasePlugin):
    """Removes leading numeric prefixes from dest_path and page URLs.

    This plugin allows you to:
    - Keep numeric prefixes in your markdown filenames for natural sorting
    - Have clean URLs in the generated site without the prefixes
    - Maintain predictable file ordering without exposing prefixes to users
    """

    config_scheme = (
        ("pattern", config_options.Type(str, default=r"^\d+--")),
        ("verbose", config_options.Type(bool, default=False)),
        ("strict", config_options.Type(bool, default=True)),
        ("strip_links", config_options.Type(bool, default=False)),
    )

    def __init__(self):
        """Initialize the plugin."""
        self.prefix_pattern: Optional[Pattern[str]] = None
        self.processed_files: dict[str, str] = {}
        self.collisions: dict[str, list[str]] = defaultdict(list)

    def on_config(self, config: MkDocsConfig) -> MkDocsConfig:
        """Initialize the regex pattern from config."""
        try:
            self.prefix_pattern = re.compile(self.config["pattern"])
            if self.config["verbose"]:
                logger.info(f"StripNumberPrefix: Using pattern '{self.config['pattern']}'")
        except re.error as e:
            raise PluginError(f"Invalid regex pattern '{self.config['pattern']}': {e}")

        return config

    def on_files(self, files: Files, config: MkDocsConfig) -> Files:
        """Process files to strip numeric prefixes from paths and URLs."""
        if not self.prefix_pattern:
            return files

        # First pass: collect all transformations
        transformations: list[tuple[File, str, str]] = []

        for file in files:
            if not file.is_documentation_page():
                continue

            # Check if filename matches pattern
            filename = Path(file.src_path).name
            if not self.prefix_pattern.match(filename):
                continue

            # Strip prefix from filename
            new_filename = self.prefix_pattern.sub("", filename)

            # Build new paths
            parent = Path(file.src_path).parent
            if parent == Path("."):
                new_src_path = new_filename
            else:
                new_src_path = str(parent / new_filename)

            # Store transformation
            transformations.append((file, file.src_path, new_src_path))

            if self.config["verbose"]:
                logger.info(f"StripNumberPrefix: {file.src_path} -> {new_src_path}")

        # Check for collisions
        dest_counts: dict[str, list[str]] = defaultdict(list)
        for file, old_path, new_path in transformations:
            dest_counts[new_path].append(old_path)

        # Report collisions
        has_collision = False
        for dest, sources in dest_counts.items():
            if len(sources) > 1:
                has_collision = True
                self.collisions[dest] = sources
                msg = f"Multiple files would map to '{dest}': {', '.join(sources)}"

                if self.config["strict"]:
                    raise PluginError(f"StripNumberPrefix: {msg}")
                else:
                    logger.warning(f"StripNumberPrefix: {msg}")

        # Apply transformations only if no collisions, or in non-strict mode skip collision files
        if has_collision and self.config["strict"]:
            # In strict mode, we already raised an error, so this won't be reached
            pass
        else:
            # Apply transformations, but skip collision files in non-strict mode
            for file, old_path, new_path in transformations:
                # In non-strict mode, skip files that would cause collisions
                if has_collision and new_path in self.collisions:
                    continue
                # Update file paths
                file.src_path = new_path
                
                # For dest_path and url, we need to strip the prefix from the basename
                old_basename = Path(old_path).name
                new_basename = Path(new_path).name
                
                # Update dest_path by replacing the old basename with new basename
                file.dest_path = file.dest_path.replace(old_basename, new_basename)
                
                # Update URL by replacing the old basename (without .md) with new basename
                old_url_part = old_basename.replace(".md", "")
                new_url_part = new_basename.replace(".md", "")
                file.url = file.url.replace(old_url_part, new_url_part)

                # Store mapping for link rewriting
                self.processed_files[old_path] = new_path

        return files

    def on_page_markdown(
        self, markdown: str, page: Page, config: MkDocsConfig, files: Files
    ) -> str:
        """Optionally rewrite internal links to remove prefixes."""
        if not self.config["strip_links"] or not self.prefix_pattern:
            return markdown

        # Pattern to match markdown links
        link_pattern = re.compile(r"\[([^\]]+)\]\(([^)]+\.md(?:#[^)]*)?)\)")

        def replace_link(match: re.Match[str]) -> str:
            link_text = match.group(1)
            link_path = match.group(2)

            # Split path and anchor
            if "#" in link_path:
                path_part, anchor = link_path.split("#", 1)
                anchor = f"#{anchor}"
            else:
                path_part = link_path
                anchor = ""

            # Check if this is a processed file
            filename = Path(path_part).name
            if self.prefix_pattern.match(filename):
                # Strip prefix
                new_filename = self.prefix_pattern.sub("", filename)
                parent = Path(path_part).parent

                if parent == Path("."):
                    new_path = new_filename
                else:
                    new_path = str(parent / new_filename)

                if self.config["verbose"]:
                    logger.info(f"StripNumberPrefix: Rewriting link {path_part} -> {new_path}")

                return f"[{link_text}]({new_path}{anchor})"

            return match.group(0)

        # Replace all links
        return link_pattern.sub(replace_link, markdown)
