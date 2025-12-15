"""Tests for the release script."""

import subprocess
import sys
import tempfile
from pathlib import Path
from unittest import mock

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.release import (
    ReleaseError,
    Version,
    generate_release_notes_template,
    is_valid_semver,
    parse_release_notes,
    read_pyproject_version,
    write_pyproject_version,
    write_release_notes,
)


class TestVersion:
    """Tests for Version class."""

    def test_parse_valid_version(self):
        v = Version.parse("1.2.3")
        assert v.major == 1
        assert v.minor == 2
        assert v.patch == 3

    def test_parse_with_whitespace(self):
        v = Version.parse(" 1.2.3 ")
        assert v == Version(1, 2, 3)

    def test_parse_invalid_format(self):
        with pytest.raises(ReleaseError, match="Invalid version format"):
            Version.parse("1.2")

    def test_parse_invalid_non_numeric(self):
        with pytest.raises(ReleaseError, match="Invalid version format"):
            Version.parse("1.2.x")

    def test_str_representation(self):
        v = Version(1, 2, 3)
        assert str(v) == "1.2.3"

    def test_bump_patch(self):
        v = Version(1, 2, 3)
        assert v.bump("patch") == Version(1, 2, 4)

    def test_bump_minor(self):
        v = Version(1, 2, 3)
        assert v.bump("minor") == Version(1, 3, 0)

    def test_bump_major(self):
        v = Version(1, 2, 3)
        assert v.bump("major") == Version(2, 0, 0)

    def test_bump_invalid_type(self):
        v = Version(1, 2, 3)
        with pytest.raises(ReleaseError, match="Invalid bump type"):
            v.bump("invalid")

    def test_bump_patch_from_zero(self):
        v = Version(0, 0, 0)
        assert v.bump("patch") == Version(0, 0, 1)

    def test_bump_minor_resets_patch(self):
        v = Version(1, 5, 9)
        bumped = v.bump("minor")
        assert bumped.patch == 0
        assert bumped.minor == 6

    def test_bump_major_resets_minor_and_patch(self):
        v = Version(1, 5, 9)
        bumped = v.bump("major")
        assert bumped.patch == 0
        assert bumped.minor == 0
        assert bumped.major == 2


class TestIsValidSemver:
    """Tests for semver validation."""

    def test_valid_semver(self):
        assert is_valid_semver("1.2.3")
        assert is_valid_semver("0.0.0")
        assert is_valid_semver("100.200.300")

    def test_invalid_semver(self):
        assert not is_valid_semver("1.2")
        assert not is_valid_semver("1.2.3.4")
        assert not is_valid_semver("v1.2.3")
        assert not is_valid_semver("1.2.x")
        assert not is_valid_semver("")


class TestReadPyprojectVersion:
    """Tests for reading pyproject.toml version."""

    def test_read_version_double_quotes(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir)
            pyproject = project_dir / "pyproject.toml"
            pyproject.write_text("""
[project]
name = "test"
version = "1.2.3"
""")
            assert read_pyproject_version(project_dir) == "1.2.3"

    def test_read_version_single_quotes(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir)
            pyproject = project_dir / "pyproject.toml"
            pyproject.write_text("""
[project]
name = "test"
version = '0.1.0'
""")
            assert read_pyproject_version(project_dir) == "0.1.0"

    def test_missing_pyproject(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with pytest.raises(ReleaseError, match="pyproject.toml not found"):
                read_pyproject_version(Path(tmpdir))

    def test_missing_version_field(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir)
            pyproject = project_dir / "pyproject.toml"
            pyproject.write_text("""
[project]
name = "test"
""")
            with pytest.raises(ReleaseError, match="No version field found"):
                read_pyproject_version(project_dir)


class TestWritePyprojectVersion:
    """Tests for writing pyproject.toml version."""

    def test_write_preserves_formatting(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir)
            pyproject = project_dir / "pyproject.toml"
            original_content = """[project]
name = "test"
version = "1.2.3"
description = "A test project"
"""
            pyproject.write_text(original_content)
            write_pyproject_version(project_dir, "2.0.0")

            new_content = pyproject.read_text()
            assert 'version = "2.0.0"' in new_content
            assert 'name = "test"' in new_content
            assert 'description = "A test project"' in new_content

    def test_write_with_single_quotes(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir)
            pyproject = project_dir / "pyproject.toml"
            pyproject.write_text("version = '1.0.0'")
            write_pyproject_version(project_dir, "2.0.0")

            new_content = pyproject.read_text()
            assert "version = '2.0.0'" in new_content


class TestParseReleaseNotes:
    """Tests for release notes parsing."""

    def test_parse_single_version(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir)
            release_md = project_dir / "RELEASE.md"
            release_md.write_text("""# Release Notes

## v1.0.0 (2025-01-01)

- Initial release
- Added feature A
""")
            notes = parse_release_notes(project_dir)
            assert "1.0.0" in notes
            assert "Initial release" in notes["1.0.0"]
            assert "Added feature A" in notes["1.0.0"]

    def test_parse_multiple_versions(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir)
            release_md = project_dir / "RELEASE.md"
            release_md.write_text("""# Release Notes

## v2.0.0 (2025-02-01)

- Major update

## v1.0.0 (2025-01-01)

- Initial release
""")
            notes = parse_release_notes(project_dir)
            assert "2.0.0" in notes
            assert "1.0.0" in notes
            assert "Major update" in notes["2.0.0"]
            assert "Initial release" in notes["1.0.0"]

    def test_parse_version_without_v_prefix(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir)
            release_md = project_dir / "RELEASE.md"
            release_md.write_text("""# Release Notes

## 1.0.0 (2025-01-01)

- No v prefix
""")
            notes = parse_release_notes(project_dir)
            assert "1.0.0" in notes

    def test_parse_missing_file_returns_empty(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            notes = parse_release_notes(Path(tmpdir))
            assert notes == {}


class TestGenerateReleaseNotesTemplate:
    """Tests for release notes template generation."""

    def test_generate_from_commits(self):
        commits = [
            "abc123 feat: add new feature",
            "def456 fix: correct bug",
        ]
        template = generate_release_notes_template(commits)
        assert "- feat: add new feature" in template
        assert "- fix: correct bug" in template

    def test_generate_empty_commits(self):
        template = generate_release_notes_template([])
        assert "No changes since last release" in template

    def test_generate_limits_to_20(self):
        commits = [f"hash{i} Commit message {i}" for i in range(25)]
        template = generate_release_notes_template(commits)
        lines = template.strip().split("\n")
        assert len(lines) == 20


class TestWriteReleaseNotes:
    """Tests for writing release notes to RELEASE.md."""

    def test_write_to_existing_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir)
            release_md = project_dir / "RELEASE.md"
            release_md.write_text("""# Release Notes

## v1.0.0 (2025-01-01)

- Initial release
""")
            write_release_notes(project_dir, "2.0.0", "- Major update")

            content = release_md.read_text()
            # New version should appear before the old one
            v2_pos = content.find("v2.0.0")
            v1_pos = content.find("v1.0.0")
            assert v2_pos < v1_pos
            assert "- Major update" in content

    def test_write_to_new_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir)
            release_md = project_dir / "RELEASE.md"
            write_release_notes(project_dir, "1.0.0", "- Initial release")

            assert release_md.exists()
            content = release_md.read_text()
            assert "v1.0.0" in content
            assert "- Initial release" in content


class TestGitOperations:
    """Tests for git operations using mocks."""

    def test_tag_exists_check_local(self):
        """Test tag existence check uses correct git commands."""
        from scripts.release import tag_exists

        with mock.patch("subprocess.run") as mock_run:
            # Mock local tag check returns the tag
            mock_run.side_effect = [
                mock.Mock(stdout="v1.0.0\n", returncode=0),  # local check
                mock.Mock(stdout="", returncode=0),  # remote check
            ]

            local, remote = tag_exists("v1.0.0")
            assert local is True
            assert remote is False

    def test_tag_exists_neither(self):
        """Test when tag doesn't exist anywhere."""
        from scripts.release import tag_exists

        with mock.patch("subprocess.run") as mock_run:
            mock_run.return_value = mock.Mock(stdout="", returncode=0)

            local, remote = tag_exists("v1.0.0")
            assert local is False
            assert remote is False

    def test_get_commits_since_tag(self):
        """Test commit retrieval since a tag."""
        from scripts.release import get_commits_since

        with mock.patch("subprocess.run") as mock_run:
            mock_run.return_value = mock.Mock(
                stdout="abc123 First commit\ndef456 Second commit\n",
                returncode=0,
            )

            commits = get_commits_since("v1.0.0")
            assert len(commits) == 2
            assert "abc123 First commit" in commits

    def test_clean_working_directory_check_passes(self):
        """Test clean directory check with clean status."""
        from scripts.release import check_clean_working_directory

        with mock.patch("subprocess.run") as mock_run:
            mock_run.return_value = mock.Mock(stdout="", returncode=0)
            # Should not raise
            check_clean_working_directory()

    def test_clean_working_directory_check_fails(self):
        """Test clean directory check with uncommitted changes."""
        from scripts.release import check_clean_working_directory

        with mock.patch("subprocess.run") as mock_run:
            mock_run.return_value = mock.Mock(
                stdout=" M modified_file.py\n",
                returncode=0,
            )
            with pytest.raises(ReleaseError, match="Working directory is not clean"):
                check_clean_working_directory()


class TestIntegrationDryRun:
    """Integration tests using --dry-run mode."""

    @pytest.fixture
    def mock_git_repo(self):
        """Create a mock project directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir)

            # Create pyproject.toml
            (project_dir / "pyproject.toml").write_text("""
[project]
name = "test-project"
version = "1.0.0"
""")

            # Create RELEASE.md
            (project_dir / "RELEASE.md").write_text("""# Release Notes

## v1.0.0 (2025-01-01)

- Initial release
""")

            yield project_dir

    def test_dry_run_shows_preview(self, mock_git_repo, capsys):
        """Test that dry-run mode shows preview without making changes."""
        from scripts.release import do_release

        with (
            mock.patch("scripts.release.tag_exists", return_value=(False, False)),
            mock.patch("scripts.release.get_last_tag", return_value="v1.0.0"),
            mock.patch(
                "scripts.release.get_commits_since",
                return_value=["abc123 feat: new feature"],
            ),
        ):
            do_release(mock_git_repo, "patch", dry_run=True)

        # Verify pyproject.toml was not changed
        content = (mock_git_repo / "pyproject.toml").read_text()
        assert 'version = "1.0.0"' in content

        # Check output shows preview
        captured = capsys.readouterr()
        assert "dry-run" in captured.out.lower()
        assert "1.0.1" in captured.out  # Target version
