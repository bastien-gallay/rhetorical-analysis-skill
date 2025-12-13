#!/usr/bin/env python3
"""Package a Claude skill for distribution.

This script validates the skill structure and creates a distributable .skill archive.
It validates SKILL.md (frontmatter, line count), extracts version from pyproject.toml,
and generates a ZIP archive excluding development files.

Usage:
    uv run python scripts/package_skill.py [--dry-run] [--output DIR] [SKILL_DIR]

Examples:
    uv run python scripts/package_skill.py                    # Package current directory
    uv run python scripts/package_skill.py --dry-run          # Preview without creating archive
    uv run python scripts/package_skill.py --output dist/     # Output to specific directory
"""

from __future__ import annotations

import argparse
import re
import sys
import zipfile
from pathlib import Path
from typing import NamedTuple

# Default patterns to exclude from the archive
# These are development/IDE files that shouldn't be distributed with the skill
DEFAULT_EXCLUSIONS = [
    # Version control
    ".git/",
    ".git",
    ".gitignore",
    # Python
    ".venv/",
    "__pycache__/",
    ".pytest_cache/",
    "*.egg-info/",
    "*.pyc",
    "*.pyo",
    # Testing
    "tests/",
    # Locking/build
    "uv.lock",
    # IDE/editor configs
    ".claude/",
    ".cursor/",
    ".agent/",
    ".opencode/",
    ".github/",
    ".vscode/",
    ".idea/",
    # Linters/type checkers
    ".ruff_cache/",
    ".mypy_cache/",
    ".markdownlint.json",
    # OS files
    ".DS_Store",
    # OpenSpec (development proposals)
    "openspec/",
    # Documentation not needed in distribution
    "docs/",
    "AGENTS.md",
    "CLAUDE.md",
    # Benchmark data (may contain copyrighted content)
    "benchmark/",
]


class ValidationError(Exception):
    """Raised when skill validation fails."""


class SkillMetadata(NamedTuple):
    """Extracted skill metadata."""

    name: str
    description: str
    version: str


def parse_yaml_frontmatter(content: str) -> dict[str, str]:
    """Extract YAML frontmatter from markdown content.

    Args:
        content: Markdown file content

    Returns:
        Dictionary of frontmatter key-value pairs

    Raises:
        ValidationError: If frontmatter is missing or malformed
    """
    if not content.startswith("---"):
        raise ValidationError("SKILL.md must start with YAML frontmatter (---)")

    # Find the closing ---
    end_match = re.search(r"\n---\s*\n", content[3:])
    if not end_match:
        raise ValidationError("SKILL.md frontmatter is not properly closed (missing ---)")

    frontmatter_text = content[4 : end_match.start() + 3]
    result = {}

    for line in frontmatter_text.strip().split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            # Remove quotes from value
            value = value.strip().strip('"').strip("'")
            result[key.strip()] = value

    return result


def validate_skill_md(skill_dir: Path, max_lines: int = 500) -> dict[str, str]:
    """Validate SKILL.md file.

    Args:
        skill_dir: Path to skill directory
        max_lines: Maximum allowed lines in SKILL.md

    Returns:
        Frontmatter dictionary with name and description

    Raises:
        ValidationError: If validation fails
    """
    skill_md = skill_dir / "SKILL.md"

    if not skill_md.exists():
        raise ValidationError(f"SKILL.md not found in {skill_dir}")

    content = skill_md.read_text(encoding="utf-8")
    lines = content.splitlines()

    if len(lines) > max_lines:
        raise ValidationError(
            f"SKILL.md exceeds {max_lines} lines (current: {len(lines)} lines)"
        )

    frontmatter = parse_yaml_frontmatter(content)

    if "name" not in frontmatter:
        raise ValidationError("SKILL.md frontmatter must contain 'name' field")
    if "description" not in frontmatter:
        raise ValidationError("SKILL.md frontmatter must contain 'description' field")

    return frontmatter


def get_version_from_pyproject(skill_dir: Path) -> str:
    """Extract version from pyproject.toml.

    Args:
        skill_dir: Path to skill directory

    Returns:
        Version string, or 'dev' if not found
    """
    pyproject = skill_dir / "pyproject.toml"

    if not pyproject.exists():
        return "dev"

    content = pyproject.read_text(encoding="utf-8")

    # Simple regex to find version in [project] section
    match = re.search(r'^\s*version\s*=\s*["\']([^"\']+)["\']', content, re.MULTILINE)
    if match:
        return match.group(1)

    return "dev"


def should_exclude(path: Path, exclusions: list[str]) -> bool:
    """Check if a path should be excluded from the archive.

    Args:
        path: Path to check (relative to skill_dir)
        exclusions: List of exclusion patterns

    Returns:
        True if the path should be excluded
    """
    path_str = str(path)
    path_parts = path.parts

    for pattern in exclusions:
        # Directory pattern with glob (e.g., *.egg-info/)
        if pattern.startswith("*") and pattern.endswith("/"):
            suffix = pattern[1:-1]  # e.g., ".egg-info"
            for part in path_parts:
                if part.endswith(suffix):
                    return True
        # Check if pattern matches directory prefix
        elif pattern.endswith("/"):
            dir_name = pattern.rstrip("/")
            if dir_name in path_parts or path_str.startswith(dir_name + "/"):
                return True
        # Check glob-style patterns for file extensions
        elif pattern.startswith("*"):
            suffix = pattern[1:]
            if path_str.endswith(suffix):
                return True
        # Exact match
        elif pattern in path_parts or path_str == pattern:
            return True

    return False


def collect_files(skill_dir: Path, exclusions: list[str]) -> list[Path]:
    """Collect files to include in the archive.

    Args:
        skill_dir: Path to skill directory
        exclusions: List of exclusion patterns

    Returns:
        List of relative paths to include
    """
    files = []

    for path in skill_dir.rglob("*"):
        if path.is_dir():
            continue

        rel_path = path.relative_to(skill_dir)

        if not should_exclude(rel_path, exclusions):
            files.append(rel_path)

    return sorted(files)


def create_archive(
    skill_dir: Path, output_path: Path, files: list[Path]
) -> None:
    """Create the .skill archive.

    Args:
        skill_dir: Path to skill directory
        output_path: Path for output archive
        files: List of relative paths to include
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for rel_path in files:
            full_path = skill_dir / rel_path
            zf.write(full_path, rel_path)


def package_skill(
    skill_dir: Path,
    output_dir: Path | None = None,
    dry_run: bool = False,
    exclusions: list[str] | None = None,
) -> Path | None:
    """Package a skill for distribution.

    Args:
        skill_dir: Path to skill directory
        output_dir: Output directory (defaults to skill_dir)
        dry_run: If True, only preview without creating archive
        exclusions: Custom exclusion patterns (defaults to DEFAULT_EXCLUSIONS)

    Returns:
        Path to created archive, or None if dry_run

    Raises:
        ValidationError: If skill validation fails
    """
    skill_dir = skill_dir.resolve()
    exclusions = exclusions or DEFAULT_EXCLUSIONS

    # Validate SKILL.md
    print(f"Validating {skill_dir / 'SKILL.md'}...")
    frontmatter = validate_skill_md(skill_dir)
    print(f"  name: {frontmatter['name']}")
    print(f"  description: {frontmatter['description'][:50]}...")

    # Get version
    version = get_version_from_pyproject(skill_dir)
    print(f"  version: {version}")

    # Collect files
    files = collect_files(skill_dir, exclusions)
    print(f"\nFiles to include ({len(files)}):")

    if dry_run:
        for f in files:
            print(f"  {f}")
        print("\n[dry-run] No archive created.")
        return None

    # Generate output path
    output_dir = output_dir or skill_dir
    archive_name = f"{frontmatter['name']}-{version}.skill"
    output_path = output_dir / archive_name

    # Create archive
    print(f"\nCreating archive: {output_path}")
    create_archive(skill_dir, output_path, files)

    # Report size
    size_kb = output_path.stat().st_size / 1024
    print(f"Archive size: {size_kb:.1f} KB")
    print(f"\nPackage created successfully: {output_path}")

    return output_path


def main() -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Package a Claude skill for distribution.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    %(prog)s                      Package current directory
    %(prog)s --dry-run            Preview files without creating archive
    %(prog)s --output dist/       Output to specific directory
    %(prog)s /path/to/skill       Package a specific skill directory

Excluded patterns by default:
    .git/, .venv/, __pycache__/, .pytest_cache/, tests/,
    *.egg-info/, .claude/, *.pyc, *.pyo, .DS_Store, openspec/
        """,
    )
    parser.add_argument(
        "skill_dir",
        nargs="?",
        default=".",
        help="Path to skill directory (default: current directory)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview files to include without creating archive",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        help="Output directory for the archive",
    )

    args = parser.parse_args()

    try:
        package_skill(
            skill_dir=Path(args.skill_dir),
            output_dir=args.output,
            dry_run=args.dry_run,
        )
        return 0
    except ValidationError as e:
        print(f"Validation error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
