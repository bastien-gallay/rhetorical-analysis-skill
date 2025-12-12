"""Tests pour le packaging du skill."""

import sys
import tempfile
import zipfile
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.package_skill import (
    ValidationError,
    collect_files,
    get_version_from_pyproject,
    package_skill,
    parse_yaml_frontmatter,
    should_exclude,
    validate_skill_md,
)


class TestParseYamlFrontmatter:
    """Tests pour l'extraction du frontmatter YAML."""

    def test_valid_frontmatter(self):
        content = """---
name: test-skill
description: "A test skill"
---

# Content here
"""
        result = parse_yaml_frontmatter(content)
        assert result["name"] == "test-skill"
        assert result["description"] == "A test skill"

    def test_missing_frontmatter(self):
        content = "# Just markdown\nNo frontmatter"
        with pytest.raises(ValidationError, match="must start with YAML frontmatter"):
            parse_yaml_frontmatter(content)

    def test_unclosed_frontmatter(self):
        content = """---
name: test
description: test
# No closing ---
"""
        with pytest.raises(ValidationError, match="not properly closed"):
            parse_yaml_frontmatter(content)

    def test_frontmatter_with_quotes(self):
        content = """---
name: "quoted-name"
description: 'single quoted'
---

Content
"""
        result = parse_yaml_frontmatter(content)
        assert result["name"] == "quoted-name"
        assert result["description"] == "single quoted"


class TestValidateSkillMd:
    """Tests pour la validation du SKILL.md."""

    @pytest.fixture
    def valid_skill_dir(self):
        """Crée un répertoire skill valide temporaire."""
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir)
            skill_md = skill_dir / "SKILL.md"
            skill_md.write_text("""---
name: test-skill
description: "A valid test skill for testing purposes"
---

# Test Skill

This is a valid skill.
""")
            yield skill_dir

    def test_valid_skill_md(self, valid_skill_dir):
        result = validate_skill_md(valid_skill_dir)
        assert result["name"] == "test-skill"
        assert "valid test skill" in result["description"]

    def test_missing_skill_md(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with pytest.raises(ValidationError, match="SKILL.md not found"):
                validate_skill_md(Path(tmpdir))

    def test_skill_md_too_long(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir)
            skill_md = skill_dir / "SKILL.md"
            # Create a SKILL.md with 501 lines
            content = """---
name: too-long
description: "Too many lines"
---

"""
            content += "\n".join([f"Line {i}" for i in range(500)])
            skill_md.write_text(content)

            with pytest.raises(ValidationError, match="exceeds 500 lines"):
                validate_skill_md(skill_dir)

    def test_skill_md_missing_name(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir)
            skill_md = skill_dir / "SKILL.md"
            skill_md.write_text("""---
description: "No name field"
---

Content
""")
            with pytest.raises(ValidationError, match="must contain 'name'"):
                validate_skill_md(skill_dir)

    def test_skill_md_missing_description(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir)
            skill_md = skill_dir / "SKILL.md"
            skill_md.write_text("""---
name: no-description
---

Content
""")
            with pytest.raises(ValidationError, match="must contain 'description'"):
                validate_skill_md(skill_dir)


class TestGetVersionFromPyproject:
    """Tests pour l'extraction de version."""

    def test_version_present(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir)
            pyproject = skill_dir / "pyproject.toml"
            pyproject.write_text("""
[project]
name = "test-skill"
version = "1.2.3"
""")
            assert get_version_from_pyproject(skill_dir) == "1.2.3"

    def test_version_absent(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir)
            pyproject = skill_dir / "pyproject.toml"
            pyproject.write_text("""
[project]
name = "test-skill"
""")
            assert get_version_from_pyproject(skill_dir) == "dev"

    def test_no_pyproject(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            assert get_version_from_pyproject(Path(tmpdir)) == "dev"

    def test_version_with_double_quotes(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir)
            pyproject = skill_dir / "pyproject.toml"
            pyproject.write_text('version = "0.1.0"')
            assert get_version_from_pyproject(skill_dir) == "0.1.0"

    def test_version_with_single_quotes(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir)
            pyproject = skill_dir / "pyproject.toml"
            pyproject.write_text("version = '0.2.0'")
            assert get_version_from_pyproject(skill_dir) == "0.2.0"


class TestShouldExclude:
    """Tests pour les exclusions de fichiers."""

    def test_exclude_git_directory(self):
        assert should_exclude(Path(".git/config"), [".git/"])
        assert should_exclude(Path(".git/objects/abc"), [".git/"])

    def test_exclude_pycache(self):
        assert should_exclude(Path("__pycache__/module.pyc"), ["__pycache__/"])
        assert should_exclude(Path("src/__pycache__/foo.pyc"), ["__pycache__/"])

    def test_exclude_by_extension(self):
        assert should_exclude(Path("module.pyc"), ["*.pyc"])
        assert should_exclude(Path("src/module.pyc"), ["*.pyc"])

    def test_include_regular_file(self):
        assert not should_exclude(Path("SKILL.md"), [".git/", "__pycache__/"])
        assert not should_exclude(Path("scripts/main.py"), [".git/", "*.pyc"])

    def test_exclude_tests_directory(self):
        assert should_exclude(Path("tests/test_main.py"), ["tests/"])

    def test_exclude_exact_match(self):
        assert should_exclude(Path(".DS_Store"), [".DS_Store"])

    def test_exclude_glob_directory_pattern(self):
        """Test *.egg-info/ pattern."""
        assert should_exclude(Path("foo.egg-info/PKG-INFO"), ["*.egg-info/"])
        assert should_exclude(Path("my_package.egg-info/SOURCES.txt"), ["*.egg-info/"])
        assert not should_exclude(Path("src/main.py"), ["*.egg-info/"])


class TestCollectFiles:
    """Tests pour la collecte de fichiers."""

    @pytest.fixture
    def sample_skill_dir(self):
        """Crée une structure de skill typique."""
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir)

            # Create structure
            (skill_dir / "SKILL.md").write_text("---\nname: test\n---")
            (skill_dir / "scripts").mkdir()
            (skill_dir / "scripts/main.py").write_text("# main")
            (skill_dir / "__pycache__").mkdir()
            (skill_dir / "__pycache__/cache.pyc").write_text("")
            (skill_dir / "tests").mkdir()
            (skill_dir / "tests/test_main.py").write_text("# test")

            yield skill_dir

    def test_excludes_pycache(self, sample_skill_dir):
        files = collect_files(sample_skill_dir, ["__pycache__/"])
        paths = [str(f) for f in files]
        assert not any("__pycache__" in p for p in paths)

    def test_excludes_tests(self, sample_skill_dir):
        files = collect_files(sample_skill_dir, ["tests/"])
        paths = [str(f) for f in files]
        assert not any("tests" in p for p in paths)

    def test_includes_skill_md(self, sample_skill_dir):
        files = collect_files(sample_skill_dir, [])
        assert Path("SKILL.md") in files

    def test_includes_scripts(self, sample_skill_dir):
        files = collect_files(sample_skill_dir, ["tests/", "__pycache__/"])
        paths = [str(f) for f in files]
        assert any("scripts/main.py" in p for p in paths)


class TestPackageSkill:
    """Tests d'intégration pour le packaging complet."""

    @pytest.fixture
    def complete_skill_dir(self):
        """Crée un skill complet pour les tests."""
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir)

            # SKILL.md
            (skill_dir / "SKILL.md").write_text("""---
name: integration-test-skill
description: "A skill for integration testing"
---

# Integration Test Skill

This skill is for testing.
""")

            # pyproject.toml
            (skill_dir / "pyproject.toml").write_text("""
[project]
name = "integration-test-skill"
version = "2.0.0"
""")

            # scripts
            (skill_dir / "scripts").mkdir()
            (skill_dir / "scripts/main.py").write_text("print('hello')")

            # references
            (skill_dir / "references").mkdir()
            (skill_dir / "references/doc.md").write_text("# Documentation")

            # Files to exclude
            (skill_dir / "__pycache__").mkdir()
            (skill_dir / "__pycache__/cache.pyc").write_text("")
            (skill_dir / "tests").mkdir()
            (skill_dir / "tests/test_main.py").write_text("# tests")
            (skill_dir / ".DS_Store").write_text("")

            yield skill_dir

    def test_dry_run_returns_none(self, complete_skill_dir):
        result = package_skill(complete_skill_dir, dry_run=True)
        assert result is None

    def test_creates_archive(self, complete_skill_dir):
        result = package_skill(complete_skill_dir)
        assert result is not None
        assert result.exists()
        assert result.name == "integration-test-skill-2.0.0.skill"

    def test_archive_excludes_tests(self, complete_skill_dir):
        result = package_skill(complete_skill_dir)
        with zipfile.ZipFile(result, "r") as zf:
            names = zf.namelist()
            assert not any("tests/" in n for n in names)
            assert not any("__pycache__" in n for n in names)
            assert not any(".DS_Store" in n for n in names)

    def test_archive_includes_required_files(self, complete_skill_dir):
        result = package_skill(complete_skill_dir)
        with zipfile.ZipFile(result, "r") as zf:
            names = zf.namelist()
            assert "SKILL.md" in names
            assert "scripts/main.py" in names
            assert "references/doc.md" in names

    def test_custom_output_dir(self, complete_skill_dir):
        with tempfile.TemporaryDirectory() as output_tmpdir:
            output_dir = Path(output_tmpdir) / "dist"
            result = package_skill(complete_skill_dir, output_dir=output_dir)
            assert result.parent == output_dir
            assert result.exists()

    def test_validation_failure_raises(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir)
            # No SKILL.md -> should fail
            with pytest.raises(ValidationError):
                package_skill(skill_dir)
