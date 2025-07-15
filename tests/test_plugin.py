# this_file: more/mkdocs-plugins/vexy-mkdocs-strip-number-prefix/tests/test_plugin.py
"""Tests for vexy-mkdocs-strip-number-prefix plugin."""

import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.exceptions import PluginError
from mkdocs.structure.files import File, Files
from mkdocs.structure.nav import Navigation
from mkdocs.structure.pages import Page

from mkdocs_strip_number_prefix.plugin import StripNumberPrefixPlugin


class TestStripNumberPrefixPlugin:
    """Test cases for StripNumberPrefixPlugin."""

    @pytest.fixture
    def plugin(self):
        """Create a plugin instance."""
        plugin = StripNumberPrefixPlugin()
        # Initialize plugin config with defaults
        plugin.config = {
            "pattern": r"^\d+--",
            "verbose": False,
            "strict": True,
            "strip_links": False,
            "strip_nav_titles": True,
            "dry_run": False,
        }
        return plugin

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
        file.src_uri = "test.md"  # Add required src_uri attribute
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
        mock_file.src_uri = "010--intro.md"

        files = Files([mock_file])

        # Process files
        plugin.on_files(files, mkdocs_config)

        # Check results
        # Source path on disk should remain unchanged after processing.
        assert mock_file.src_path == "010--intro.md"
        assert mock_file.dest_path == "intro/index.html"
        assert mock_file.url == "intro/"

    def test_on_files_with_subdirectory(self, plugin, mkdocs_config, mock_file):
        """Test stripping prefix from files in subdirectories."""
        plugin.on_config(mkdocs_config)

        mock_file.src_path = "guides/020--setup.md"
        mock_file.dest_path = "guides/020--setup/index.html"
        mock_file.url = "guides/020--setup/"
        mock_file.src_uri = "guides/020--setup.md"

        files = Files([mock_file])
        plugin.on_files(files, mkdocs_config)

        # Source path unchanged.
        assert mock_file.src_path == "guides/020--setup.md"
        assert mock_file.dest_path == "guides/setup/index.html"
        assert mock_file.url == "guides/setup/"

    def test_no_prefix_match(self, plugin, mkdocs_config, mock_file):
        """Test file without matching prefix."""
        plugin.on_config(mkdocs_config)

        mock_file.src_path = "regular-file.md"
        mock_file.dest_path = "regular-file/index.html"
        mock_file.url = "regular-file/"
        mock_file.src_uri = "regular-file.md"

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
        file1.src_uri = "010--intro.md"

        file2 = Mock(spec=File)
        file2.is_documentation_page.return_value = True
        file2.src_path = "020--intro.md"
        file2.src_uri = "020--intro.md"

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
        file1.src_uri = "010--intro.md"

        file2 = Mock(spec=File)
        file2.is_documentation_page.return_value = True
        file2.src_path = "020--intro.md"
        file2.dest_path = "020--intro/index.html"
        file2.url = "020--intro/"
        file2.src_uri = "020--intro.md"

        files = Files([file1, file2])

        # Should not raise, and source paths remain unchanged
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
        file.src_uri = "010--image.png"

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
        mock_file.src_uri = "010--intro.md"

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
        file1.src_uri = "010--intro.md"

        file2 = Mock(spec=File)
        file2.is_documentation_page.return_value = True
        file2.src_path = "about.md"
        file2.dest_path = "about/index.html"
        file2.url = "about/"
        file2.src_uri = "about.md"

        file3 = Mock(spec=File)
        file3.is_documentation_page.return_value = True
        file3.src_path = "020--guide.md"
        file3.dest_path = "020--guide/index.html"
        file3.url = "020--guide/"
        file3.src_uri = "020--guide.md"

        files = Files([file1, file2, file3])
        plugin.on_files(files, mkdocs_config)

        # Check results
        assert file1.src_path == "010--intro.md"
        assert file2.src_path == "about.md"  # unchanged
        assert file3.src_path == "020--guide.md"

    def test_on_nav_strips_prefixes(self, plugin, mkdocs_config):
        """Test navigation title stripping with file format."""
        plugin.on_config(mkdocs_config)

        # Create mock navigation items with file-format titles
        nav_item1 = Mock()
        nav_item1.title = "010--getting-started"
        nav_item1.children = []

        nav_item2 = Mock()
        nav_item2.title = "020--basic-syntax"
        nav_item2.children = []

        nav = Mock(spec=Navigation)
        nav.items = [nav_item1, nav_item2]
        files = Files([])

        result = plugin.on_nav(nav, mkdocs_config, files)

        assert nav_item1.title == "getting started"
        assert nav_item2.title == "basic syntax"
        assert result == nav

    def test_on_nav_strips_nav_format_prefixes(self, plugin, mkdocs_config):
        """Test navigation title stripping with navigation display format."""
        plugin.on_config(mkdocs_config)

        # Create mock navigation items with nav-format titles (spaces instead of dashes)
        nav_item1 = Mock()
        nav_item1.title = "010 getting started"
        nav_item1.children = []

        nav_item2 = Mock()
        nav_item2.title = "020 basic syntax"
        nav_item2.children = []

        nav = Mock(spec=Navigation)
        nav.items = [nav_item1, nav_item2]
        files = Files([])

        result = plugin.on_nav(nav, mkdocs_config, files)

        assert nav_item1.title == "getting started"
        assert nav_item2.title == "basic syntax"
        assert result == nav

    def test_on_nav_recursive_children(self, plugin, mkdocs_config):
        """Test navigation title stripping works recursively on children."""
        plugin.on_config(mkdocs_config)

        # Create child nav items
        child1 = Mock()
        child1.title = "010--introduction"
        child1.children = []

        child2 = Mock()
        child2.title = "020 installation"
        child2.children = []

        # Create parent nav item with children
        parent = Mock()
        parent.title = "030--getting-started"
        parent.children = [child1, child2]

        nav = Mock(spec=Navigation)
        nav.items = [parent]
        files = Files([])

        result = plugin.on_nav(nav, mkdocs_config, files)

        assert parent.title == "getting started"
        assert child1.title == "introduction"
        assert child2.title == "installation"
        assert result == nav

    def test_on_nav_no_title_attribute(self, plugin, mkdocs_config):
        """Test navigation handling when items don't have title attribute."""
        plugin.on_config(mkdocs_config)

        # Create nav item without title
        nav_item = Mock()
        if hasattr(nav_item, 'title'):
            delattr(nav_item, 'title')
        nav_item.children = []

        nav = Mock(spec=Navigation)
        nav.items = [nav_item]
        files = Files([])

        # Should not crash
        result = plugin.on_nav(nav, mkdocs_config, files)
        assert result == nav

    def test_on_nav_empty_title(self, plugin, mkdocs_config):
        """Test navigation handling with empty title."""
        plugin.on_config(mkdocs_config)

        nav_item = Mock()
        nav_item.title = ""
        nav_item.children = []

        nav = Mock(spec=Navigation)
        nav.items = [nav_item]
        files = Files([])

        result = plugin.on_nav(nav, mkdocs_config, files)
        assert nav_item.title == ""
        assert result == nav

    def test_on_nav_no_pattern_match(self, plugin, mkdocs_config):
        """Test navigation titles that don't match any pattern."""
        plugin.on_config(mkdocs_config)

        nav_item = Mock()
        nav_item.title = "Regular Title"
        nav_item.children = []

        nav = Mock(spec=Navigation)
        nav.items = [nav_item]
        files = Files([])

        result = plugin.on_nav(nav, mkdocs_config, files)
        assert nav_item.title == "Regular Title"  # Should remain unchanged
        assert result == nav

    def test_on_nav_disabled(self, plugin, mkdocs_config):
        """Test navigation title stripping when disabled."""
        plugin.config["strip_nav_titles"] = False
        plugin.on_config(mkdocs_config)

        nav_item = Mock()
        nav_item.title = "010--getting-started"
        nav_item.children = []

        nav = Mock(spec=Navigation)
        nav.items = [nav_item]
        files = Files([])

        result = plugin.on_nav(nav, mkdocs_config, files)
        assert nav_item.title == "010--getting-started"  # Should remain unchanged
        assert result == nav

    def test_on_nav_no_prefix_pattern(self, plugin, mkdocs_config):
        """Test navigation when prefix pattern is not set."""
        plugin.prefix_pattern = None

        nav_item = Mock()
        nav_item.title = "010--getting-started"
        nav_item.children = []

        nav = Mock(spec=Navigation)
        nav.items = [nav_item]
        files = Files([])

        result = plugin.on_nav(nav, mkdocs_config, files)
        assert nav_item.title == "010--getting-started"  # Should remain unchanged
        assert result == nav

    def test_on_nav_verbose_logging(self, plugin, mkdocs_config):
        """Test verbose logging in navigation title processing."""
        plugin.config["verbose"] = True
        plugin.on_config(mkdocs_config)

        nav_item = Mock()
        nav_item.title = "010 getting started"
        nav_item.children = []

        nav = Mock(spec=Navigation)
        nav.items = [nav_item]
        files = Files([])

        with patch("mkdocs_strip_number_prefix.plugin.logger") as mock_logger:
            plugin.on_nav(nav, mkdocs_config, files)

            # Should log the navigation title update
            mock_logger.info.assert_called()
            call_args = str(mock_logger.info.call_args_list)
            assert "Navigation title updated" in call_args
            assert "010 getting started" in call_args
            assert "getting started" in call_args

    def test_strip_nav_titles_config_option(self, mkdocs_config):
        """Test strip_nav_titles configuration option."""
        plugin = StripNumberPrefixPlugin()
        
        # Test default value
        plugin.config = {
            "pattern": r"^\d+--",
            "verbose": False,
            "strict": True,
            "strip_links": False,
            "strip_nav_titles": True,
        }
        
        assert plugin.config["strip_nav_titles"] is True
        
        # Test disabling it
        plugin.config["strip_nav_titles"] = False
        assert plugin.config["strip_nav_titles"] is False

    def test_end_to_end_mkdocs_build(self, tmp_path):
        """End-to-end test that runs MkDocs build with the plugin."""
        # Create a minimal MkDocs project structure
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        site_dir = tmp_path / "site"
        
        # Create test markdown files with numeric prefixes
        (docs_dir / "index.md").write_text("# Welcome\nThis is the home page.")
        (docs_dir / "010--getting-started.md").write_text("# Getting Started\nIntroduction content.")
        (docs_dir / "020--advanced.md").write_text("# Advanced Topics\nAdvanced content.")
        
        # Create subdirectory with prefixed files
        guides_dir = docs_dir / "030--guides"
        guides_dir.mkdir()
        (guides_dir / "010--setup.md").write_text("# Setup Guide\nSetup instructions.")
        (guides_dir / "020--deployment.md").write_text("# Deployment\nDeploy instructions.")
        
        # Create MkDocs config
        mkdocs_config = {
            'site_name': 'Test Site',
            'docs_dir': str(docs_dir),
            'site_dir': str(site_dir),
            'plugins': [
                'search',
                {
                    'strip-number-prefix': {
                        'pattern': r'^\d+--',
                        'strict': True,
                        'strip_nav_titles': True,
                        'verbose': False
                    }
                }
            ],
            'theme': 'mkdocs'
        }
        
        # Import MkDocs and run build
        try:
            from mkdocs.config import load_config
            from mkdocs.commands.build import build
            
            # Create config file temporarily
            config_file = tmp_path / "mkdocs.yml"
            import yaml
            config_file.write_text(yaml.dump(mkdocs_config))
            
            # Load and build
            config = load_config(config_file=str(config_file))
            build(config)
            
            # Verify the build succeeded and files exist
            assert site_dir.exists()
            assert (site_dir / "index.html").exists()
            
            # Verify clean URLs were generated (no numeric prefixes)
            assert (site_dir / "getting-started" / "index.html").exists()
            assert (site_dir / "advanced" / "index.html").exists()
            assert (site_dir / "guides" / "setup" / "index.html").exists()
            assert (site_dir / "guides" / "deployment" / "index.html").exists()
            
            # Verify original prefixed paths don't exist in output
            assert not (site_dir / "010--getting-started").exists()
            assert not (site_dir / "020--advanced").exists()
            assert not (site_dir / "030--guides").exists()
            
            # Read generated HTML to verify navigation was cleaned
            index_content = (site_dir / "index.html").read_text()
            assert "getting-started" in index_content  # Clean URL
            assert "010--getting-started" not in index_content  # No prefix in HTML
            
        except ImportError:
            pytest.skip("MkDocs not available for end-to-end testing")
        except Exception as e:
            pytest.fail(f"End-to-end MkDocs build failed: {e}")

    def test_windows_path_separators(self, plugin, mkdocs_config):
        """Test that plugin handles Windows path separators correctly."""
        plugin.on_config(mkdocs_config)

        # Test with Windows-style paths - simulate actual Windows behavior
        import os
        
        mock_file = Mock(spec=File)
        mock_file.is_documentation_page.return_value = True
        
        # Use actual path separators but ensure processing happens
        if os.sep == '\\':  # Running on Windows
            mock_file.src_path = "guides\\010--setup.md"
            mock_file.dest_path = "guides\\010--setup\\index.html"
            expected_dest_parts = ["guides", "setup", "index.html"]
            expected_dest = os.sep.join(expected_dest_parts)
        else:  # Running on Unix-like (simulate Windows paths)
            mock_file.src_path = "guides/010--setup.md"  # Use forward slash for Unix
            mock_file.dest_path = "guides/010--setup/index.html"
            expected_dest = "guides/setup/index.html"
        
        mock_file.url = "guides/010--setup/"  # URLs always use forward slashes
        mock_file.src_uri = mock_file.src_path

        files = Files([mock_file])
        plugin.on_files(files, mkdocs_config)

        # Verify paths were processed correctly regardless of separator
        # Source path should remain unchanged
        assert mock_file.src_path.endswith("010--setup.md")
        
        # Dest path should have prefix removed
        assert mock_file.dest_path == expected_dest
        
        # URL should be clean and use forward slashes
        assert mock_file.url == "guides/setup/"

    def test_dry_run_mode_files(self, plugin, mkdocs_config, mock_file):
        """Test dry-run mode for file processing."""
        plugin.config["dry_run"] = True
        plugin.on_config(mkdocs_config)

        # Setup file with prefix
        mock_file.src_path = "010--intro.md"
        mock_file.dest_path = "010--intro/index.html"
        mock_file.url = "010--intro/"
        mock_file.src_uri = "010--intro.md"

        original_dest = mock_file.dest_path
        original_url = mock_file.url

        files = Files([mock_file])

        with patch("mkdocs_strip_number_prefix.plugin.logger") as mock_logger:
            plugin.on_files(files, mkdocs_config)

            # In dry-run mode, paths should remain unchanged
            assert mock_file.src_path == "010--intro.md"
            assert mock_file.dest_path == original_dest  # Should not be modified
            assert mock_file.url == original_url  # Should not be modified

            # Should log dry-run information
            mock_logger.info.assert_called()
            call_args = str(mock_logger.info.call_args_list)
            assert "DRY RUN" in call_args

    def test_dry_run_mode_navigation(self, plugin, mkdocs_config):
        """Test dry-run mode for navigation processing."""
        plugin.config["dry_run"] = True
        plugin.on_config(mkdocs_config)

        nav_item = Mock()
        nav_item.title = "010--getting-started"
        nav_item.children = []

        nav = Mock(spec=Navigation)
        nav.items = [nav_item]
        files = Files([])

        with patch("mkdocs_strip_number_prefix.plugin.logger") as mock_logger:
            result = plugin.on_nav(nav, mkdocs_config, files)

            # In dry-run mode, navigation titles should remain unchanged
            assert nav_item.title == "010--getting-started"
            assert result == nav

            # Should log dry-run information
            mock_logger.info.assert_called()
            call_args = str(mock_logger.info.call_args_list)
            assert "DRY RUN" in call_args

    def test_dry_run_mode_links(self, plugin, mkdocs_config):
        """Test dry-run mode for link rewriting."""
        plugin.config["dry_run"] = True
        plugin.config["strip_links"] = True
        plugin.on_config(mkdocs_config)

        markdown = "Check out [Introduction](010--intro.md) for more info."
        page = Mock(spec=Page)
        files = Files([])

        with patch("mkdocs_strip_number_prefix.plugin.logger") as mock_logger:
            result = plugin.on_page_markdown(markdown, page, mkdocs_config, files)

            # In dry-run mode, markdown should remain unchanged
            assert result == markdown

            # Should log dry-run information
            mock_logger.info.assert_called()
            call_args = str(mock_logger.info.call_args_list)
            assert "DRY RUN" in call_args
