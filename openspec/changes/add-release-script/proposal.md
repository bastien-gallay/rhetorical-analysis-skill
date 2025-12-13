# Change: Add release script for version management

## Why

Currently, releasing a new version requires manual steps: editing `pyproject.toml`, creating
a git tag, and pushing. This is error-prone and lacks validation of release notes. A dedicated
script will streamline the release process and ensure consistency between version, tag, and
release documentation.

## What Changes

- Add `RELEASE.md` file with simple version-section format
- Add `scripts/release.py` script that:
  - Bumps version in `pyproject.toml` (patch/minor/major or explicit version)
  - Validates release notes exist for the target version
  - Proposes auto-generated release notes from git log if missing
  - Creates git tag with version
  - Pushes tag with user confirmation
  - Supports `--dry-run` mode

## Impact

- Affected specs: New capability `release-script`
- Affected code:
  - `scripts/release.py` (new)
  - `RELEASE.md` (new)
  - `pyproject.toml` (modified at runtime)
