#!/usr/bin/env python3
"""Release management script for version bumping and tagging.

This script automates the release process by:
- Bumping version in pyproject.toml (patch/minor/major or explicit)
- Validating/generating release notes in RELEASE.md
- Creating annotated git tags
- Pushing tags with user confirmation

Usage:
    uv run python scripts/release.py [--dry-run] [patch|minor|major|X.Y.Z]

Examples:
    uv run python scripts/release.py patch           # 0.1.3 -> 0.1.4
    uv run python scripts/release.py minor           # 0.1.3 -> 0.2.0
    uv run python scripts/release.py major           # 0.1.3 -> 1.0.0
    uv run python scripts/release.py 2.0.0           # Set explicit version
    uv run python scripts/release.py --dry-run patch # Preview without changes
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from datetime import date
from pathlib import Path
from typing import NamedTuple


class ReleaseError(Exception):
    """Raised when release process fails."""


class Version(NamedTuple):
    """Semantic version representation."""

    major: int
    minor: int
    patch: int

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"

    @classmethod
    def parse(cls, version_str: str) -> Version:
        """Parse a version string into a Version object.

        Args:
            version_str: Version string in X.Y.Z format

        Returns:
            Version object

        Raises:
            ReleaseError: If version string is invalid
        """
        match = re.match(r"^(\d+)\.(\d+)\.(\d+)$", version_str.strip())
        if not match:
            raise ReleaseError(
                f"Invalid version format: '{version_str}'. Expected X.Y.Z (e.g., 1.2.3)"
            )
        return cls(int(match.group(1)), int(match.group(2)), int(match.group(3)))

    def bump(self, bump_type: str) -> Version:
        """Create a new version with the specified bump.

        Args:
            bump_type: One of 'patch', 'minor', 'major'

        Returns:
            New bumped Version
        """
        if bump_type == "patch":
            return Version(self.major, self.minor, self.patch + 1)
        elif bump_type == "minor":
            return Version(self.major, self.minor + 1, 0)
        elif bump_type == "major":
            return Version(self.major + 1, 0, 0)
        else:
            raise ReleaseError(f"Invalid bump type: {bump_type}")


def is_valid_semver(version_str: str) -> bool:
    """Check if a string is a valid semantic version.

    Args:
        version_str: String to validate

    Returns:
        True if valid semver format
    """
    return bool(re.match(r"^\d+\.\d+\.\d+$", version_str.strip()))


# --- Pyproject Management ---


def read_pyproject_version(project_dir: Path) -> str:
    """Read version from pyproject.toml.

    Args:
        project_dir: Project root directory

    Returns:
        Current version string

    Raises:
        ReleaseError: If pyproject.toml or version not found
    """
    pyproject = project_dir / "pyproject.toml"
    if not pyproject.exists():
        raise ReleaseError(f"pyproject.toml not found in {project_dir}")

    content = pyproject.read_text(encoding="utf-8")
    match = re.search(r'^\s*version\s*=\s*["\']([^"\']+)["\']', content, re.MULTILINE)
    if not match:
        raise ReleaseError("No version field found in pyproject.toml")

    return match.group(1)


def write_pyproject_version(project_dir: Path, new_version: str) -> None:
    """Update version in pyproject.toml, preserving formatting.

    Args:
        project_dir: Project root directory
        new_version: New version string to write
    """
    pyproject = project_dir / "pyproject.toml"
    content = pyproject.read_text(encoding="utf-8")

    # Replace version while preserving surrounding formatting
    new_content = re.sub(
        r'^(\s*version\s*=\s*["\'])([^"\']+)(["\'])',
        rf"\g<1>{new_version}\g<3>",
        content,
        count=1,
        flags=re.MULTILINE,
    )

    if new_content == content:
        raise ReleaseError("Failed to update version in pyproject.toml")

    pyproject.write_text(new_content, encoding="utf-8")


# --- Git Operations ---


def run_git(args: list[str], check: bool = True, capture: bool = True) -> str:
    """Run a git command.

    Args:
        args: Git command arguments
        check: Raise on non-zero exit
        capture: Capture and return output

    Returns:
        Command output (if capture=True)

    Raises:
        ReleaseError: If command fails and check=True
    """
    try:
        result = subprocess.run(
            ["git"] + args,
            capture_output=capture,
            text=True,
            check=check,
        )
        return result.stdout.strip() if capture else ""
    except subprocess.CalledProcessError as e:
        stderr = e.stderr.strip() if e.stderr else "Unknown error"
        raise ReleaseError(f"Git command failed: git {' '.join(args)}\n{stderr}") from e


def check_clean_working_directory() -> None:
    """Verify working directory is clean.

    Raises:
        ReleaseError: If there are uncommitted changes
    """
    status = run_git(["status", "--porcelain"])
    if status:
        raise ReleaseError(
            "Working directory is not clean. Commit or stash changes first.\n"
            f"Uncommitted changes:\n{status}"
        )


def get_current_branch() -> str:
    """Get the current git branch name.

    Returns:
        Branch name
    """
    return run_git(["branch", "--show-current"])


def tag_exists(tag: str) -> tuple[bool, bool]:
    """Check if a tag exists locally and/or remotely.

    Args:
        tag: Tag name to check

    Returns:
        Tuple of (exists_locally, exists_remotely)
    """
    # Check local
    local_result = subprocess.run(
        ["git", "tag", "-l", tag],
        capture_output=True,
        text=True,
    )
    exists_locally = bool(local_result.stdout.strip())

    # Check remote
    exists_remotely = False
    try:
        remote_result = subprocess.run(
            ["git", "ls-remote", "--tags", "origin", tag],
            capture_output=True,
            text=True,
        )
        exists_remotely = bool(remote_result.stdout.strip())
    except subprocess.CalledProcessError:
        pass  # Remote might not be configured

    return exists_locally, exists_remotely


def get_last_tag() -> str | None:
    """Get the most recent tag.

    Returns:
        Tag name or None if no tags exist
    """
    try:
        return run_git(["describe", "--tags", "--abbrev=0"])
    except ReleaseError:
        return None


def get_commits_since(ref: str | None = None) -> list[str]:
    """Get commit messages since a reference.

    Args:
        ref: Git reference (tag/commit), or None for all commits

    Returns:
        List of commit messages (one line each)
    """
    if ref:
        commits = run_git(["log", f"{ref}..HEAD", "--oneline", "--no-decorate"])
    else:
        commits = run_git(["log", "--oneline", "--no-decorate"])

    return [line for line in commits.split("\n") if line.strip()]


def create_tag(tag: str, message: str) -> None:
    """Create an annotated git tag.

    Args:
        tag: Tag name
        message: Tag message (release notes)
    """
    run_git(["tag", "-a", tag, "-m", message])


def push_tag(tag: str) -> None:
    """Push a tag to origin.

    Args:
        tag: Tag name to push

    Raises:
        ReleaseError: If push fails
    """
    try:
        run_git(["push", "origin", tag])
    except ReleaseError as e:
        raise ReleaseError(f"Failed to push tag {tag}: {e}") from e


# --- Release Notes ---


def parse_release_notes(project_dir: Path) -> dict[str, str]:
    """Parse RELEASE.md to extract version sections.

    Args:
        project_dir: Project root directory

    Returns:
        Dict mapping version strings to their release notes content
    """
    release_md = project_dir / "RELEASE.md"
    if not release_md.exists():
        return {}

    content = release_md.read_text(encoding="utf-8")
    sections: dict[str, str] = {}

    # Match version headers like "## v0.1.0" or "## 0.1.0"
    pattern = r"^##\s+v?(\d+\.\d+\.\d+)\s*(?:\([^)]*\))?\s*\n(.*?)(?=^##\s+v?\d+\.\d+\.\d+|\Z)"
    matches = re.finditer(pattern, content, re.MULTILINE | re.DOTALL)

    for match in matches:
        version = match.group(1)
        notes = match.group(2).strip()
        sections[version] = notes

    return sections


def generate_release_notes_template(commits: list[str]) -> str:
    """Generate release notes template from commits.

    Args:
        commits: List of commit messages

    Returns:
        Formatted release notes template
    """
    if not commits:
        return "- No changes since last release"

    lines = []
    for commit in commits[:20]:  # Limit to 20 most recent
        # Extract just the message part (after commit hash)
        parts = commit.split(" ", 1)
        if len(parts) > 1:
            lines.append(f"- {parts[1]}")
        else:
            lines.append(f"- {commit}")

    return "\n".join(lines)


def write_release_notes(project_dir: Path, version: str, notes: str) -> None:
    """Add a new release section to RELEASE.md.

    Args:
        project_dir: Project root directory
        version: Version string
        notes: Release notes content
    """
    release_md = project_dir / "RELEASE.md"
    today = date.today().isoformat()

    new_section = f"## v{version} ({today})\n\n{notes}\n\n"

    if release_md.exists():
        content = release_md.read_text(encoding="utf-8")
        # Insert after header section
        header_end = content.find("\n## ")
        if header_end > 0:
            new_content = content[:header_end] + "\n" + new_section + content[header_end + 1 :]
        else:
            new_content = content.rstrip() + "\n\n" + new_section
    else:
        new_content = f"# Release Notes\n\n{new_section}"

    release_md.write_text(new_content, encoding="utf-8")


def create_initial_release_md(project_dir: Path) -> None:
    """Create initial RELEASE.md with format documentation.

    Args:
        project_dir: Project root directory
    """
    release_md = project_dir / "RELEASE.md"
    if release_md.exists():
        return

    content = """# Release Notes

This file documents all notable changes to this project.
Format: Each version section contains a list of changes.

<!-- Versions are added automatically by scripts/release.py -->
"""
    release_md.write_text(content, encoding="utf-8")


# --- Pre-flight Checks ---


def preflight_checks(project_dir: Path, warn_branch: bool = True) -> None:
    """Run all pre-flight checks before release.

    Args:
        project_dir: Project root directory
        warn_branch: Whether to warn about non-main branches

    Raises:
        ReleaseError: If any check fails
    """
    # Check pyproject.toml exists and has version
    read_pyproject_version(project_dir)

    # Check working directory is clean
    check_clean_working_directory()

    # Warn about branch
    if warn_branch:
        branch = get_current_branch()
        if branch not in ("main", "master"):
            print(f"Warning: You are on branch '{branch}', not main/master.")


# --- Main Release Logic ---


def do_release(
    project_dir: Path,
    bump_or_version: str,
    dry_run: bool = False,
    skip_push: bool = False,
) -> None:
    """Execute the release process.

    Args:
        project_dir: Project root directory
        bump_or_version: 'patch', 'minor', 'major', or explicit version
        dry_run: If True, preview actions without making changes
        skip_push: If True, skip pushing the tag
    """
    # Determine target version
    current_version_str = read_pyproject_version(project_dir)
    current_version = Version.parse(current_version_str)

    if bump_or_version in ("patch", "minor", "major"):
        target_version = current_version.bump(bump_or_version)
    else:
        if not is_valid_semver(bump_or_version):
            raise ReleaseError(
                f"Invalid version: '{bump_or_version}'. "
                "Use patch/minor/major or explicit X.Y.Z format."
            )
        target_version = Version.parse(bump_or_version)

    tag_name = f"v{target_version}"
    print(f"Current version: {current_version}")
    print(f"Target version:  {target_version}")
    print(f"Tag name:        {tag_name}")
    print()

    # Check tag doesn't already exist
    local_exists, remote_exists = tag_exists(tag_name)
    if local_exists:
        raise ReleaseError(f"Tag {tag_name} already exists locally")
    if remote_exists:
        raise ReleaseError(f"Tag {tag_name} already exists on remote")

    # Check/generate release notes
    existing_notes = parse_release_notes(project_dir)
    if str(target_version) in existing_notes:
        notes = existing_notes[str(target_version)]
        print(f"Found existing release notes for v{target_version}")
    else:
        # Generate from commits
        last_tag = get_last_tag()
        commits = get_commits_since(last_tag)
        proposed_notes = generate_release_notes_template(commits)

        print("Proposed release notes (from git log):")
        print("-" * 40)
        print(proposed_notes)
        print("-" * 40)

        if dry_run:
            notes = proposed_notes
            print("[dry-run] Would prompt for release notes confirmation")
        else:
            response = input("Accept these notes? [Y/n/edit]: ").strip().lower()
            if response in ("", "y", "yes"):
                notes = proposed_notes
            elif response in ("n", "no"):
                raise ReleaseError("Release cancelled. Add notes manually to RELEASE.md first.")
            elif response in ("e", "edit"):
                print("Enter release notes (end with empty line):")
                lines = []
                while True:
                    line = input()
                    if not line:
                        break
                    lines.append(line)
                notes = "\n".join(lines)
            else:
                raise ReleaseError(f"Unknown response: {response}")

    # Preview actions
    print("\nActions to perform:")
    print(f"  1. Update pyproject.toml version to {target_version}")
    print("  2. Add release notes to RELEASE.md")
    print(f"  3. Create annotated tag {tag_name}")
    if not skip_push:
        print(f"  4. Push tag {tag_name} to origin")
    print()

    if dry_run:
        print("[dry-run] No changes made.")
        return

    # Execute
    print("Updating pyproject.toml...")
    write_pyproject_version(project_dir, str(target_version))

    print("Updating RELEASE.md...")
    create_initial_release_md(project_dir)
    write_release_notes(project_dir, str(target_version), notes)

    # Commit changes
    print("Committing version bump...")
    run_git(["add", "pyproject.toml", "RELEASE.md"])
    run_git(["commit", "-m", f"chore: release v{target_version}"])

    print(f"Creating tag {tag_name}...")
    create_tag(tag_name, notes)

    if skip_push:
        print(f"\nTag {tag_name} created locally. Push manually with:")
        print(f"  git push origin {tag_name}")
    else:
        response = input(f"Push tag {tag_name} to origin? [Y/n]: ").strip().lower()
        if response in ("", "y", "yes"):
            print(f"Pushing tag {tag_name}...")
            try:
                push_tag(tag_name)
                print(f"\nRelease v{target_version} completed successfully!")
            except ReleaseError as e:
                print(f"\nWarning: Tag push failed: {e}")
                print(f"Tag {tag_name} was created locally. Push manually later.")
        else:
            print(f"\nTag {tag_name} created locally. Push manually with:")
            print(f"  git push origin {tag_name}")


def main() -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Release management: bump version, tag, and push.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    %(prog)s patch              Bump patch version (0.1.3 -> 0.1.4)
    %(prog)s minor              Bump minor version (0.1.3 -> 0.2.0)
    %(prog)s major              Bump major version (0.1.3 -> 1.0.0)
    %(prog)s 2.0.0              Set explicit version
    %(prog)s --dry-run patch    Preview release without changes
    %(prog)s --no-push patch    Create tag but don't push
        """,
    )
    parser.add_argument(
        "version",
        help="Version bump type (patch/minor/major) or explicit version (X.Y.Z)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview actions without making changes",
    )
    parser.add_argument(
        "--no-push",
        action="store_true",
        help="Create tag locally without pushing",
    )

    args = parser.parse_args()

    project_dir = Path.cwd()

    try:
        # Run pre-flight checks
        if not args.dry_run:
            preflight_checks(project_dir)
        else:
            # Still validate pyproject.toml exists
            read_pyproject_version(project_dir)
            print("[dry-run] Skipping working directory check")

        # Execute release
        do_release(
            project_dir=project_dir,
            bump_or_version=args.version,
            dry_run=args.dry_run,
            skip_push=args.no_push,
        )
        return 0

    except ReleaseError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nRelease cancelled.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
