# this_file: more/mkdocs-plugins/vexy-mkdocs-strip-number-prefix/tests/test_plugin.py
"""Tests for vexy-mkdocs-strip-number-prefix plugin."""

from unittest.mock import Mock, patch

import pytest
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.exceptions import PluginError
from mkdocs.structure.files import File, Files
from mkdocs.structure.pages import Page

from mkdocs_strip_number_prefix.plugin import StripNumberPrefixPlugin


class TestStripNumberPrefixPlugin:
    """Test cases for StripNumberPrefixPlugin."""

    @pytest.fixture
    def plugin(self):
        """Create a plugin instance."""
        return StripNumberPrefixPlugin()

    @pytest.fixture
    def mkdocs_config(self):
        """Create a mock MkDocs config."""
        config = MkDocsConfig()
        config["site_dir"] = "site"
        config["docs_dir"] = "docs"
        return config

    @pytest.fixture
    def mock_file(self):
        """Create a mock file."""
        file = Mock(spec=File)
        file.is_documentation_page.return_value = True
        return file

    def test_default_pattern(self, plugin, mkdocs_config):
        """Test with default pattern."""
        plugin.on_config(mkdocs_config)

        # Test pattern matches
        assert plugin.prefix_pattern.match("123--file.md")
        assert plugin.prefix_pattern.match("01--intro.md")
        assert plugin.prefix_pattern.match("999--appendix.md")

        # Test pattern doesn't match
        assert not plugin.prefix_pattern.match("file.md")
        assert not plugin.prefix_pattern.match("123-file.md")
        assert not plugin.prefix_pattern.match("abc--file.md")

    def test_custom_pattern(self, plugin, mkdocs_config):
        """Test with custom pattern."""
        plugin.config["pattern"] = r"^\d{3}--"
        plugin.on_config(mkdocs_config)

        # Test exact 3 digits
        assert plugin.prefix_pattern.match("123--file.md")
        assert plugin.prefix_pattern.match("001--file.md")
        assert not plugin.prefix_pattern.match("1--file.md")
        assert not plugin.prefix_pattern.match("1234--file.md")

    def test_invalid_regex_pattern(self, plugin, mkdocs_config):
        """Test invalid regex pattern handling."""
        plugin.config["pattern"] = r"[invalid"

        with pytest.raises(PluginError) as exc_info:
            plugin.on_config(mkdocs_config)

        assert "Invalid regex pattern" in str(exc_info.value)

    def test_on_files_strips_prefix(self, plugin, mkdocs_config, mock_file):
        """Test stripping prefix from files."""
        # Setup
        plugin.on_config(mkdocs_config)

        mock_file.src_path = "010--intro.md"
        mock_file.dest_path = "010--intro/index.html"
        mock_file.url = "010--intro/"

        files = Files([mock_file])

        # Process files
        plugin.on_files(files, mkdocs_config)

        # Check results
        assert mock_file.src_path == "intro.md"
        assert mock_file.dest_path == "intro/index.html"
        assert mock_file.url == "intro/"

    def test_on_files_with_subdirectory(self, plugin, mkdocs_config, mock_file):
        """Test stripping prefix from files in subdirectories."""
        plugin.on_config(mkdocs_config)

        mock_file.src_path = "guides/020--setup.md"
        mock_file.dest_path = "guides/020--setup/index.html"
        mock_file.url = "guides/020--setup/"

        files = Files([mock_file])
        plugin.on_files(files, mkdocs_config)

        assert mock_file.src_path == "guides/setup.md"
        assert mock_file.dest_path == "guides/setup/index.html"
        assert mock_file.url == "guides/setup/"

    def test_no_prefix_match(self, plugin, mkdocs_config, mock_file):
        """Test file without matching prefix."""
        plugin.on_config(mkdocs_config)

        mock_file.src_path = "regular-file.md"
        mock_file.dest_path = "regular-file/index.html"
        mock_file.url = "regular-file/"

        files = Files([mock_file])
        plugin.on_files(files, mkdocs_config)

        # Should remain unchanged
        assert mock_file.src_path == "regular-file.md"
        assert mock_file.dest_path == "regular-file/index.html"
        assert mock_file.url == "regular-file/"

    def test_collision_detection_strict(self, plugin, mkdocs_config):
        """Test collision detection in strict mode."""
        plugin.config["strict"] = True
        plugin.on_config(mkdocs_config)

        # Create two files that would have same destination
        file1 = Mock(spec=File)
        file1.is_documentation_page.return_value = True
        file1.src_path = "010--intro.md"

        file2 = Mock(spec=File)
        file2.is_documentation_page.return_value = True
        file2.src_path = "020--intro.md"

        files = Files([file1, file2])

        with pytest.raises(PluginError) as exc_info:
            plugin.on_files(files, mkdocs_config)

        assert "Multiple files would map to 'intro.md'" in str(exc_info.value)

    def test_collision_detection_non_strict(self, plugin, mkdocs_config):
        """Test collision detection in non-strict mode."""
        plugin.config["strict"] = False
        plugin.on_config(mkdocs_config)

        # Create two files that would have same destination
        file1 = Mock(spec=File)
        file1.is_documentation_page.return_value = True
        file1.src_path = "010--intro.md"
        file1.dest_path = "010--intro/index.html"
        file1.url = "010--intro/"

        file2 = Mock(spec=File)
        file2.is_documentation_page.return_value = True
        file2.src_path = "020--intro.md"
        file2.dest_path = "020--intro/index.html"
        file2.url = "020--intro/"

        files = Files([file1, file2])

        # Should not raise, but files should remain unchanged
        plugin.on_files(files, mkdocs_config)

        assert file1.src_path == "010--intro.md"
        assert file2.src_path == "020--intro.md"

    def test_link_rewriting_enabled(self, plugin, mkdocs_config):
        """Test markdown link rewriting when enabled."""
        plugin.config["strip_links"] = True
        plugin.on_config(mkdocs_config)

        markdown = """
        Check out [Introduction](010--intro.md) for more info.
        Also see [Setup Guide](020--setup.md#installation).
        And [Regular Link](regular.md) should not change.
        External [link](https://example.com) is ignored.
        """

        page = Mock(spec=Page)
        files = Files([])

        result = plugin.on_page_markdown(markdown, page, mkdocs_config, files)

        assert "[Introduction](intro.md)" in result
        assert "[Setup Guide](setup.md#installation)" in result
        assert "[Regular Link](regular.md)" in result
        assert "[link](https://example.com)" in result

    def test_link_rewriting_disabled(self, plugin, mkdocs_config):
        """Test that link rewriting can be disabled."""
        plugin.config["strip_links"] = False
        plugin.on_config(mkdocs_config)

        markdown = "Check out [Introduction](010--intro.md) for more info."

        page = Mock(spec=Page)
        files = Files([])

        result = plugin.on_page_markdown(markdown, page, mkdocs_config, files)

        # Should remain unchanged
        assert result == markdown

    def test_link_rewriting_with_subdirectory(self, plugin, mkdocs_config):
        """Test link rewriting with subdirectories."""
        plugin.config["strip_links"] = True
        plugin.on_config(mkdocs_config)

        markdown = "See [Guide](guides/010--quickstart.md) for details."

        page = Mock(spec=Page)
        files = Files([])

        result = plugin.on_page_markdown(markdown, page, mkdocs_config, files)

        assert "[Guide](guides/quickstart.md)" in result

    def test_non_markdown_files_ignored(self, plugin, mkdocs_config):
        """Test that non-markdown files are ignored."""
        plugin.on_config(mkdocs_config)

        # Create non-documentation file
        file = Mock(spec=File)
        file.is_documentation_page.return_value = False
        file.src_path = "010--image.png"

        files = Files([file])
        plugin.on_files(files, mkdocs_config)

        # Should remain unchanged
        assert file.src_path == "010--image.png"

    def test_verbose_logging(self, plugin, mkdocs_config, mock_file):
        """Test verbose logging mode."""
        plugin.config["verbose"] = True
        plugin.on_config(mkdocs_config)

        mock_file.src_path = "010--intro.md"
        mock_file.dest_path = "010--intro/index.html"
        mock_file.url = "010--intro/"

        files = Files([mock_file])

        # Should log transformations
        with patch("mkdocs_strip_number_prefix.plugin.logger") as mock_logger:
            plugin.on_files(files, mkdocs_config)

            mock_logger.info.assert_called()
            call_args = str(mock_logger.info.call_args)
            assert "010--intro.md" in call_args
            assert "intro.md" in call_args

    def test_mixed_files(self, plugin, mkdocs_config):
        """Test processing mix of prefixed and non-prefixed files."""
        plugin.on_config(mkdocs_config)

        # Create mix of files
        file1 = Mock(spec=File)
        file1.is_documentation_page.return_value = True
        file1.src_path = "010--intro.md"
        file1.dest_path = "010--intro/index.html"
        file1.url = "010--intro/"

        file2 = Mock(spec=File)
        file2.is_documentation_page.return_value = True
        file2.src_path = "about.md"
        file2.dest_path = "about/index.html"
        file2.url = "about/"

        file3 = Mock(spec=File)
        file3.is_documentation_page.return_value = True
        file3.src_path = "020--guide.md"
        file3.dest_path = "020--guide/index.html"
        file3.url = "020--guide/"

        files = Files([file1, file2, file3])
        plugin.on_files(files, mkdocs_config)

        # Check results
        assert file1.src_path == "intro.md"
        assert file2.src_path == "about.md"  # unchanged
        assert file3.src_path == "guide.md"
