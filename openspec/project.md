# Project Context

## Purpose

A **Claude skill** for rhetorical and epistemological analysis of articles, speeches, and
argumentative texts. The skill enables systematic evaluation of argument quality by combining:

- **Toulmin model** for argument structure analysis
- **CRAAP test** for source credibility evaluation
- **Fallacies catalog** for reasoning error detection
- **Reliability scale** (1-5) for overall assessment

The goal is to help users deconstruct arguments, identify logical flaws, and produce
structured critical analysis reports.

## Tech Stack

- **Python** 3.10+ (runtime)
- **uv** for dependency management and running scripts
- **openpyxl** for XLSX report generation
- **pytest** for testing
- **ruff** for linting (line-length: 100, target: py310)
- **markdownlint** for markdown files

### Dev dependencies (optional-dependencies.dev)

- pytest, pytest-cov for testing
- jsonschema for JSON validation
- httpx for URL fetching (future)
- beautifulsoup4, readability-lxml for HTML extraction (future)

## Project Conventions

### Code Style

- **Python files**: `snake_case` naming
- **Skill name**: `kebab-case` (rhetorical-analysis)
- **Type hints**: Required for all functions
- **Docstrings**: Google style format
- **Line length**: 100 characters (ruff config)
- **Design principles**: CUPID (Composable, Unix philosophy, Predictable, Idiomatic, Domain-based)

### Architecture Patterns

- **Scripts in `scripts/`**: Executable Python scripts with CLI interface
- **References in `references/`**: External documentation (frameworks, catalogs)
- **Assets in `assets/`**: Example files, templates, JSON schemas
- **JSON as interface contract**: Claude produces JSON, scripts consume it
- **SKILL.md as entry point**: Must stay lightweight (< 500 lines)

### Testing Strategy

- Tests in `tests/` directory
- Use `pytest` with `-v --tb=short` options
- Test files named `test_*.py`
- Run with: `uv run pytest tests/ -v`

### Git Workflow

- Standard feature branch workflow
- No "Claude" signature in commit messages
- Use markdownlint before committing markdown files

## Domain Context

### Toulmin Model (argument structure)

For each argument, extract:

- **Claim**: The thesis being defended
- **Grounds**: Evidence/data presented
- **Warrant**: Implicit logical link between evidence and thesis
- **Backing**: Supporting elements for the warrant
- **Qualifier**: Nuances or restrictions
- **Rebuttal**: Counter-arguments (recognized or ignored)

### CRAAP Test (source reliability)

Evaluate each cited source on:

- **Currency**: Is the information up-to-date?
- **Relevance**: Is it relevant to the topic?
- **Authority**: Is the author/source credible?
- **Accuracy**: Are facts verifiable and accurate?
- **Purpose**: What's the intent? (inform, persuade, sell...)

### Reliability Scale (1-5)

- **5**: Established fact, scientific consensus, multiple verifiable sources
- **4**: Serious sources, valid reasoning, possible nuances
- **3**: Mix of facts/interpretations, partial sources
- **2**: Questionable reasoning, fallacies identified
- **1**: Unsourced claims, major logical errors

## Important Constraints

- SKILL.md must stay under 500 lines - use external references for details
- JSON analysis format is the contract between Claude and scripts
- Always test script modifications before committing
- Distinguish argument weakness from conclusion validity
- Apply equal rigor regardless of agreement with conclusions

## External Dependencies

- No external APIs required currently
- Future: web_fetch integration for direct URL analysis
- Reference frameworks are local markdown files (no external fetching)
