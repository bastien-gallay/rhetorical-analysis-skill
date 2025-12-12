# Rhetorical Analysis Skill

A Claude skill for rhetorical and epistemological analysis of articles, speeches, and argumentative texts.

## Features

- **Toulmin Model Analysis**: Decompose arguments into claim, grounds, warrant, backing, qualifier, and rebuttal
- **CRAAP Test**: Evaluate source reliability (Currency, Relevance, Authority, Accuracy, Purpose)
- **Fallacy Detection**: Identify logical fallacies from a comprehensive catalog
- **XLSX Report Generation**: Export structured analysis to Excel format

## Installation

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

## License

MIT
