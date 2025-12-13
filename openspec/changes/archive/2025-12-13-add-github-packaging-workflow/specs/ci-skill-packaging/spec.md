# ci-skill-packaging Specification

## Purpose

Automate the creation and distribution of `.skill` package archives via GitHub Actions when version tags are pushed. This capability ensures reproducible builds and provides users with downloadable skill packages directly from GitHub Releases.

## ADDED Requirements

### Requirement: Tag-based Workflow Trigger

The CI system SHALL trigger the packaging workflow when version tags are pushed.

#### Scenario: Version tag pushed

- **WHEN** a Git tag matching the pattern `v*` is pushed to the repository (e.g., `v0.1.0`, `v1.2.3`)
- **THEN** the packaging workflow is triggered automatically
- **AND** the workflow has access to the tag name and commit SHA

#### Scenario: Non-version tag pushed

- **WHEN** a Git tag not matching the pattern `v*` is pushed (e.g., `test-tag`, `release-candidate`)
- **THEN** the packaging workflow is NOT triggered

#### Scenario: Regular commit pushed

- **WHEN** commits are pushed without tags to any branch
- **THEN** the packaging workflow is NOT triggered

---

### Requirement: Environment Setup

The CI system SHALL configure a consistent Python environment for running the packaging script.

#### Scenario: Python and uv installation

- **WHEN** the workflow runs
- **THEN** Python 3.10 or higher is installed
- **AND** the `uv` package manager is installed and available

#### Scenario: Repository checkout

- **WHEN** the workflow checks out the repository
- **THEN** the full Git history is available (not shallow clone)
- **AND** all files required by `package_skill.py` are present

---

### Requirement: Skill Package Generation

The CI system SHALL execute the packaging script to generate the `.skill` archive.

#### Scenario: Successful packaging

- **WHEN** the packaging script `scripts/package_skill.py` is executed with `--output dist/`
- **THEN** the script runs using `uv` runtime
- **AND** the `.skill` archive is created in the `dist/` directory
- **AND** the archive name includes the version from `pyproject.toml` (e.g., `rhetorical-analysis-0.1.0.skill`)

#### Scenario: Packaging validation failure

- **WHEN** `package_skill.py` fails validation (missing SKILL.md, exceeds 500 lines, etc.)
- **THEN** the workflow fails with a clear error message
- **AND** no GitHub Release is created
- **AND** the workflow log shows the validation error from the script

---

### Requirement: Integrity Verification

The CI system SHALL generate cryptographic checksums for package integrity verification.

#### Scenario: SHA256 checksum generation

- **WHEN** the `.skill` archive is successfully created
- **THEN** a SHA256 hash of the archive file is computed
- **AND** the hash is stored in a `checksums.txt` file
- **AND** the format follows the standard checksum format: `<hash> <filename>`

#### Scenario: Multiple verification methods documented

- **WHEN** checksums are generated
- **THEN** the release includes documentation for verifying integrity on different platforms
- **AND** commands for Linux/macOS (`sha256sum -c checksums.txt`) are provided
- **AND** commands for Windows PowerShell (`Get-FileHash`) are provided

---

### Requirement: GitHub Release Creation

The CI system SHALL create a GitHub Release with the packaged skill archive and integrity verification files.

#### Scenario: Release created from tag

- **WHEN** the `.skill` archive and checksums are successfully generated
- **THEN** a GitHub Release is created with the tag name as the release title
- **AND** the release includes the `.skill` archive as a downloadable asset
- **AND** the release includes the `checksums.txt` file as a downloadable asset
- **AND** the release is marked as published (not draft)

#### Scenario: Pre-release detection

- **WHEN** the tag name contains pre-release identifiers (`-alpha`, `-beta`, `-rc`)
- **THEN** the GitHub Release is marked as a pre-release
- **AND** the release is still published (not draft)

#### Scenario: Release notes generation

- **WHEN** a GitHub Release is created
- **THEN** release notes are auto-generated from commits since the previous tag
- **OR** use the tag annotation message if the tag is annotated

---

### Requirement: Workflow Permissions

The CI workflow SHALL have appropriate permissions to create releases and upload assets.

#### Scenario: Sufficient permissions

- **WHEN** the workflow executes
- **THEN** the workflow has `contents: write` permission
- **AND** the workflow can create releases via GitHub API
- **AND** the workflow can upload release assets

---

### Requirement: Artifact Naming Consistency

The CI system SHALL ensure the artifact name matches the package metadata.

#### Scenario: Version consistency check (informational)

- **WHEN** the tag is `v0.1.0` and `pyproject.toml` contains `version = "0.1.0"`
- **THEN** the generated archive is named `rhetorical-analysis-0.1.0.skill`
- **AND** the release title is `v0.1.0`

#### Scenario: Version mismatch visibility

- **WHEN** the tag is `v0.2.0` but `pyproject.toml` contains `version = "0.1.0"`
- **THEN** the workflow still succeeds
- **AND** the archive is named `rhetorical-analysis-0.1.0.skill` (from pyproject.toml)
- **AND** the release title is `v0.2.0` (from tag)
- **AND** the mismatch is visible to users downloading the release

**Note**: This scenario documents expected behavior but does not enforce synchronization. Maintainers are responsible for ensuring tag and version consistency.

---

### Requirement: User Documentation

The CI system SHALL ensure users have clear instructions for downloading and verifying packages.

#### Scenario: README contains download section

- **WHEN** the workflow is implemented
- **THEN** the README.md file includes a section with links to GitHub Releases
- **AND** the section includes a GitHub release badge showing the latest version
- **AND** the section is placed in a prominent location (near installation instructions)

#### Scenario: Integrity verification documented

- **WHEN** checksums are generated for releases
- **THEN** the README includes instructions for verifying package integrity
- **AND** example commands are provided for at least Linux/macOS and Windows
- **AND** the verification process is explained clearly for non-technical users

#### Scenario: Installation workflow documented

- **WHEN** a user wants to install the skill
- **THEN** the README provides step-by-step instructions:
  1. Navigate to GitHub Releases page
  2. Download the `.skill` file and `checksums.txt`
  3. Verify integrity using checksums
  4. Install/use the skill package

---

## Related Specifications

- **skill-packaging**: Defines the requirements for the `package_skill.py` script used by this CI workflow
