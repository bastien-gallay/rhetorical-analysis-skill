# Rhetorical Analysis Skill

![GitHub Release](https://img.shields.io/github/v/release/bastiengallay/rhetorical-analysis-skill?label=latest%20release)

A Claude skill for rhetorical and epistemological analysis of articles, speeches, and argumentative texts.

## Features

- **Toulmin Model Analysis**: Decompose arguments into claim, grounds, warrant, backing, qualifier, and rebuttal
- **CRAAP Test**: Evaluate source reliability (Currency, Relevance, Authority, Accuracy, Purpose)
- **Fallacy Detection**: Identify logical fallacies from a comprehensive catalog
- **XLSX Report Generation**: Export structured analysis to Excel format

## Download

Pre-packaged `.skill` archives are available for download from [GitHub Releases](https://github.com/bastiengallay/rhetorical-analysis-skill/releases).

### Installation Steps

1. Navigate to the [Releases page](https://github.com/bastiengallay/rhetorical-analysis-skill/releases)
2. Download the latest `.skill` file (e.g., `rhetorical-analysis-0.1.0.skill`)
3. Download the `checksums.txt` file from the same release
4. Verify package integrity (see below)
5. Use the `.skill` file with your Claude-compatible application

### Verify Package Integrity

After downloading, verify the package hasn't been tampered with:

**Linux/macOS:**

```bash
sha256sum -c checksums.txt
```

**Windows PowerShell:**

```powershell
Get-FileHash rhetorical-analysis-0.1.0.skill -Algorithm SHA256
# Compare the output hash with the value in checksums.txt
```

## Development Installation

```bash
uv sync --all-extras
```

## Usage

### Generate Analysis Report

```bash
uv run python scripts/generate_analysis.py input.json output.xlsx
```

### Package the Skill

The `package_skill.py` script validates and packages the skill for distribution.

```bash
# Create distributable .skill archive
uv run python scripts/package_skill.py

# Preview files without creating archive
uv run python scripts/package_skill.py --dry-run

# Output to specific directory
uv run python scripts/package_skill.py --output dist/
```

#### Validation

The script validates SKILL.md before packaging:

- Requires YAML frontmatter with `name` and `description` fields
- Enforces maximum 500 lines

#### Excluded Files

The following patterns are excluded from the archive by default:

| Category        | Patterns                                                                          |
| --------------- | --------------------------------------------------------------------------------- |
| Version control | `.git/`, `.gitignore`                                                             |
| Python          | `.venv/`, `__pycache__/`, `*.egg-info/`, `*.pyc`, `*.pyo`                         |
| Testing         | `tests/`, `.pytest_cache/`                                                        |
| IDE/Editor      | `.claude/`, `.cursor/`, `.vscode/`, `.idea/`, `.agent/`, `.opencode/`, `.github/` |
| Linters         | `.ruff_cache/`, `.mypy_cache/`, `.markdownlint.json`                              |
| Build           | `uv.lock`                                                                         |
| Development     | `openspec/`, `docs/`, `CLAUDE.md`, `AGENTS.md`                                    |
| OS              | `.DS_Store`                                                                       |

#### Output

The archive is named `{skill-name}-{version}.skill`, e.g., `rhetorical-analysis-0.1.0.skill`.

## Development

### Run Tests

```bash
uv run pytest tests/ -v
```

### Project Structure

```text
.
├── SKILL.md              # Skill entry point (read by Claude)
├── scripts/              # Python scripts
│   ├── generate_analysis.py
│   └── package_skill.py
├── references/           # Reference documentation
│   ├── fallacies-catalog.md
│   └── existing-frameworks-and-tools.md
├── assets/               # Example files and templates
│   └── example_analysis.json
└── tests/                # Unit tests
```

### Creating a Release (Maintainers)

Releases are automated via GitHub Actions when version tags are pushed.

#### Release Process

1. **Update version** in `pyproject.toml` to match the release version (e.g., `0.1.0`)
2. **Commit changes** and push to main branch
3. **Create and push tag** with the version number:

   ```bash
   git tag v0.1.0
   git push origin v0.1.0
   ```

4. **GitHub Actions automatically**:
   - Runs the packaging script (`scripts/package_skill.py`)
   - Generates SHA256 checksums
   - Creates a GitHub Release with the tag name
   - Uploads the `.skill` archive and `checksums.txt` as release assets

#### Tagging Conventions

- **Standard releases**: `v<major>.<minor>.<patch>` (e.g., `v1.0.0`, `v0.2.1`)
- **Pre-releases**: Include suffix `-alpha`, `-beta`, or `-rc` (e.g., `v0.1.0-alpha`, `v1.0.0-rc1`)
  - Pre-releases are automatically marked as such on GitHub

#### Version Consistency

Ensure the Git tag version matches the `version` field in `pyproject.toml`:

- Tag `v0.1.0` should correspond to `version = "0.1.0"` in `pyproject.toml`
- The `.skill` archive name is derived from `pyproject.toml`
- Mismatches will be visible to users but won't fail the workflow

#### Troubleshooting

**Workflow fails during packaging:**

- Check the workflow logs in the Actions tab
- Verify `SKILL.md` passes validation (max 500 lines, valid YAML frontmatter)
- Test locally: `uv run python scripts/package_skill.py --dry-run`

**Need to fix a release:**

1. Delete the tag locally and remotely:

   ```bash
   git tag -d v0.1.0
   git push origin :refs/tags/v0.1.0
   ```

2. Delete the GitHub Release in the web interface
3. Fix the issue, then create the tag again

**Verify release integrity:**

```bash
# Download the release assets
wget https://github.com/bastiengallay/rhetorical-analysis-skill/releases/download/v0.1.0/rhetorical-analysis-0.1.0.skill
wget https://github.com/bastiengallay/rhetorical-analysis-skill/releases/download/v0.1.0/checksums.txt

# Verify checksum
sha256sum -c checksums.txt
```

## License

MIT
