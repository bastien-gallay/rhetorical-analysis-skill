# Proposal: add-ci-testing

## Summary

Add a GitHub Actions workflow to run tests automatically on pull requests and pushes
to main, completing the CI/CD setup alongside the existing packaging workflow.

## Motivation

The backlog item "CI/CD: GitHub Actions pour les tests et le packaging" is partially
complete. The packaging workflow (`package-skill.yml`) is implemented and runs on
version tags. However, there is no workflow to run tests on PRs and pushes, which
means:

- Test failures are only discovered locally by developers
- PRs can be merged without verified test results
- No visibility into test status via GitHub checks

## Scope

This proposal adds a **new workflow** for CI testing. It does NOT modify the existing
`package-skill.yml` workflow.

### In scope

- GitHub Actions workflow for running pytest
- Trigger on pushes to main and pull requests
- Python + uv environment setup
- Test result visibility via GitHub checks

### Out of scope

- Linting in CI (can be added later)
- Coverage reporting (can be added later)
- Integration tests or e2e tests (only unit tests exist currently)

## Impact

- **New file**: `.github/workflows/test.yml`
- **Spec**: New `ci-testing` capability spec

## References

- Existing packaging workflow: `.github/workflows/package-skill.yml`
- Existing tests: `tests/` directory (4 test files)
- Tech stack: Python 3.10+, uv, pytest
