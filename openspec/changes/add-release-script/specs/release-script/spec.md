# release-script Specification

## Purpose

Automate version management, release notes validation, and git tag creation for consistent
and error-free releases.

## ADDED Requirements

### Requirement: Version Bump Modes

The release script SHALL support multiple ways to specify the target version.

#### Scenario: Bump by increment type

- **WHEN** the user runs `uv run python scripts/release.py patch`
- **THEN** the script reads current version from `pyproject.toml`
- **AND** increments the patch number (e.g., `0.1.3` becomes `0.1.4`)
- **AND** proceeds with the release workflow

#### Scenario: Bump minor version

- **WHEN** the user runs `uv run python scripts/release.py minor`
- **THEN** the script increments minor and resets patch (e.g., `0.1.3` becomes `0.2.0`)

#### Scenario: Bump major version

- **WHEN** the user runs `uv run python scripts/release.py major`
- **THEN** the script increments major and resets minor/patch (e.g., `0.1.3` becomes `1.0.0`)

#### Scenario: Explicit version

- **WHEN** the user runs `uv run python scripts/release.py 1.2.3`
- **THEN** the script uses `1.2.3` as the target version
- **AND** validates it follows semver format (X.Y.Z)

#### Scenario: Invalid version format

- **WHEN** the user provides an invalid version (e.g., `1.2`, `v1.0.0`, `abc`)
- **THEN** the script exits with an error message explaining the expected format

---

### Requirement: Pyproject Version Update

The release script SHALL update the version in `pyproject.toml`.

#### Scenario: Successful version update

- **WHEN** the target version is determined
- **THEN** the script updates `version = "X.Y.Z"` in `pyproject.toml`
- **AND** preserves all other content and formatting

#### Scenario: Version already exists

- **WHEN** the target version equals the current version in `pyproject.toml`
- **THEN** the script exits with an error indicating the version is already set

---

### Requirement: Release Notes Validation

The release script SHALL validate that release notes exist for the target version.

#### Scenario: Release notes section exists

- **WHEN** `RELEASE.md` contains a section `## X.Y.Z` matching the target version
- **AND** the section has non-empty content
- **THEN** the script proceeds with the release workflow

#### Scenario: Release notes section missing

- **WHEN** `RELEASE.md` does not contain a section for the target version
- **THEN** the script generates proposed release notes from git log
- **AND** displays the proposed content to the user
- **AND** prompts the user to accept or abort

#### Scenario: User accepts proposed release notes

- **WHEN** the user accepts the proposed release notes
- **THEN** the script appends the new section to `RELEASE.md`
- **AND** proceeds with the release workflow

#### Scenario: User rejects proposed release notes

- **WHEN** the user rejects the proposed release notes
- **THEN** the script exits without making any changes
- **AND** displays a message suggesting manual editing of `RELEASE.md`

#### Scenario: RELEASE.md does not exist

- **WHEN** the `RELEASE.md` file does not exist
- **THEN** the script creates it with the proposed release notes section
- **AND** prompts the user to accept or abort

---

### Requirement: Git Log Based Release Notes

The release script SHALL generate release notes content from git history.

#### Scenario: Commits since last tag

- **WHEN** generating release notes
- **AND** previous version tags exist
- **THEN** the script extracts commit messages since the last `vX.Y.Z` tag
- **AND** formats them as a bullet list

#### Scenario: No previous tags

- **WHEN** generating release notes
- **AND** no previous version tags exist
- **THEN** the script extracts commit messages from the initial commit
- **AND** formats them as a bullet list

#### Scenario: Release notes template

- **WHEN** release notes are generated
- **THEN** the format follows this template:

```text
## X.Y.Z

- Commit message 1
- Commit message 2
...
```

---

### Requirement: Git Tag Creation

The release script SHALL create a git tag for the release.

#### Scenario: Tag created successfully

- **WHEN** version is updated and release notes are validated
- **THEN** the script creates an annotated git tag `vX.Y.Z`
- **AND** the tag message includes the release notes content

#### Scenario: Tag already exists

- **WHEN** a tag `vX.Y.Z` already exists locally or remotely
- **THEN** the script exits with an error before making any changes
- **AND** suggests using a different version or deleting the existing tag

---

### Requirement: Push with Confirmation

The release script SHALL push the tag with user confirmation.

#### Scenario: User confirms push

- **WHEN** the tag is created locally
- **THEN** the script displays a summary of changes
- **AND** prompts the user to confirm push
- **WHEN** the user confirms
- **THEN** the script pushes the tag to origin

#### Scenario: User declines push

- **WHEN** the user declines the push confirmation
- **THEN** the tag remains local
- **AND** the script displays the command to push manually later

#### Scenario: Push failure

- **WHEN** the push fails (network error, permissions, etc.)
- **THEN** the script displays the error
- **AND** the local tag and changes remain intact

---

### Requirement: Dry Run Mode

The release script SHALL support a preview mode without making changes.

#### Scenario: Dry run execution

- **WHEN** the user runs the script with `--dry-run` flag
- **THEN** the script displays all actions that would be performed
- **AND** does not modify `pyproject.toml`
- **AND** does not modify `RELEASE.md`
- **AND** does not create git tags
- **AND** does not push anything

#### Scenario: Dry run output

- **WHEN** running in dry-run mode
- **THEN** the output clearly indicates it is a preview
- **AND** shows the current version, target version, and proposed changes

---

### Requirement: Pre-flight Checks

The release script SHALL validate prerequisites before making changes.

#### Scenario: Clean working directory required

- **WHEN** the git working directory has uncommitted changes
- **THEN** the script exits with an error
- **AND** suggests committing or stashing changes first

#### Scenario: On main branch check

- **WHEN** the current branch is not `main`
- **THEN** the script displays a warning
- **AND** prompts the user to confirm proceeding from a non-main branch

#### Scenario: Pyproject.toml exists

- **WHEN** `pyproject.toml` does not exist or lacks a version field
- **THEN** the script exits with an error explaining the requirement
