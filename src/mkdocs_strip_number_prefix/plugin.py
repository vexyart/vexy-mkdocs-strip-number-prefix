# this_file: more/mkdocs-plugins/vexy-mkdocs-strip-number-prefix/src/mkdocs_strip_number_prefix/plugin.py  # noqa: E501
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
from mkdocs.structure.nav import Navigation
from mkdocs.structure.pages import Page

logger = logging.getLogger(__name__)


class StripNumberPrefixPlugin(BasePlugin):  # type: ignore[no-untyped-call,type-arg]
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
        ("strip_nav_titles", config_options.Type(bool, default=True)),
    )

    def __init__(self) -> None:
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
            raise PluginError(f"Invalid regex pattern '{self.config['pattern']}': {e}") from e

        return config

    def on_files(self, files: Files, config: MkDocsConfig) -> Files:  # noqa: PLR0912, ARG002
        """Process files to strip numeric prefixes from paths and URLs."""
        if not self.prefix_pattern:
            return files

        # First pass: collect all transformations
        transformations: list[tuple[File, str, str]] = []

        for file in files:
            if not file.is_documentation_page():
                continue

            # Build *clean* path parts (without prefixes) for URL / dest_path generation.
            # We intentionally DO NOT change ``file.src_path`` because that path must
            # remain a valid path on disk for MkDocs to read the source markdown file.
            # Changing it would break the `abs_src_path` property and ultimately raise
            # ``FileNotFoundError`` during the build phase.  Instead, we derive the
            # *virtual* cleaned path that will be exposed to the final site and store
            # the required information so we can later update ``dest_path`` and
            # ``url``.

            src_parts = Path(file.src_path).parts

            clean_parts: list[str] = []
            for part in src_parts:
                clean_parts.append(self.prefix_pattern.sub("", part) if self.prefix_pattern.match(part) else part)

            cleaned_virtual_src = str(Path(*clean_parts))

            # Only act when something actually changes (avoid needless work).
            if cleaned_virtual_src != file.src_path:
                transformations.append((file, cleaned_virtual_src))

                if self.config["verbose"]:
                    logger.info(
                        "StripNumberPrefix: virtual clean path %s -> %s", file.src_path, cleaned_virtual_src
                    )

        # ------------------------------------------------------------------
        # Collision detection: two different *source* files mapping to the
        # same *clean* (virtual) path would override each other in the final
        # site.  We use the cleaned virtual path as the key and store the
        # original ``src_path`` values for reporting.
        # ------------------------------------------------------------------

        dest_counts: dict[str, list[str]] = defaultdict(list)
        for file_obj, new_virtual_path in transformations:
            dest_counts[new_virtual_path].append(file_obj.src_path)

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
            for file_obj, new_virtual_path in transformations:
                # In non-strict mode, skip files that would cause collisions
                if has_collision and new_virtual_path in self.collisions:
                    continue
                # ------------------------------------------------------------------
                # ``dest_path`` and ``url`` should present the cleaned structure to
                # the outside world.  We build new versions by applying the prefix
                # removal to every path component while preserving the file
                # extension (if any) and the trailing slash semantics used by
                # MkDocs (``use_directory_urls``).
                # ------------------------------------------------------------------

                # Helper for stripping a single component (keeps file extension).
                def _clean_component(component: str) -> str:
                    if self.prefix_pattern.match(component):
                        # Split filename and extension (if there is one)
                        p = Path(component)
                        if p.suffix:
                            cleaned = self.prefix_pattern.sub("", p.stem) + p.suffix
                        else:
                            cleaned = self.prefix_pattern.sub("", component)
                        return cleaned
                    return component

                # Build cleaned dest_path
                dest_parts = [_clean_component(part) for part in Path(file_obj.dest_path).parts]
                file_obj.dest_path = str(Path(*dest_parts))

                # Build cleaned url (keep trailing slash if present in original)
                url_parts = [_clean_component(part) for part in Path(file_obj.url).parts]
                file_obj.url = "/".join(url_parts) + ("/" if file_obj.url.endswith("/") else "")

                # Store mapping for link rewriting if needed later
                self.processed_files[file_obj.src_path] = new_virtual_path

        return files

    def on_nav(self, nav: Navigation, config: MkDocsConfig, files: Files) -> Navigation:  # noqa: ARG002
        """Strip numeric prefixes from navigation titles."""
        if not self.config["strip_nav_titles"] or not self.prefix_pattern:
            return nav

        def clean_navigation_titles(nav_items: list) -> None:
            """Recursively clean titles in navigation items."""
            for item in nav_items:
                if hasattr(item, "title") and item.title:
                    original_title = item.title
                    
                    # Strip the numeric prefix from the title
                    # Handle both file format (010--title) and navigation format (010 title)
                    nav_pattern = re.compile(r"^\d+\s+")
                    if self.prefix_pattern.match(original_title) or nav_pattern.match(original_title):
                        # Use the navigation pattern if the original pattern doesn't match
                        if nav_pattern.match(original_title):
                            cleaned_title = nav_pattern.sub("", original_title).strip()
                        else:
                            cleaned_title = self.prefix_pattern.sub("", original_title)
                            # Convert dashes to spaces and clean up formatting
                            cleaned_title = cleaned_title.replace("--", "").replace("-", " ").strip()
                        
                        # Capitalize appropriately
                        if cleaned_title:
                            item.title = cleaned_title

                            if self.config["verbose"]:
                                logger.info(
                                    f"StripNumberPrefix: Navigation title updated: {original_title} -> {cleaned_title}"
                                )

                # Recursively process children (for sections)
                if hasattr(item, "children") and item.children:
                    clean_navigation_titles(item.children)

        # Process all navigation items
        clean_navigation_titles(nav.items)

        return nav

    def on_page_markdown(
        self, markdown: str, page: Page, config: MkDocsConfig, files: Files  # noqa: ARG002
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
            if self.prefix_pattern and self.prefix_pattern.match(filename):
                # Strip prefix
                new_filename = self.prefix_pattern.sub("", filename) if self.prefix_pattern else filename
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
