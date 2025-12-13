# ci-testing

## Purpose

Ensure code quality by running automated tests on every push to main and pull request.

## ADDED Requirements

### Requirement: PR and Push Workflow Trigger

The CI system SHALL trigger the test workflow on pull requests and pushes to the main
branch.

#### Scenario: Pull request opened

- **WHEN** a pull request is opened targeting the main branch
- **THEN** the test workflow is triggered automatically
- **AND** test results appear as a GitHub check on the PR

#### Scenario: Pull request updated

- **WHEN** new commits are pushed to an open pull request
- **THEN** the test workflow is triggered for the new commit
- **AND** the previous workflow run is cancelled (if still running)

#### Scenario: Push to main

- **WHEN** commits are pushed directly to the main branch
- **THEN** the test workflow is triggered
- **AND** test results are visible in the repository's Actions tab

---

### Requirement: Test Environment Setup

The CI system SHALL configure a Python environment consistent with project conventions.

#### Scenario: Python and uv installation

- **WHEN** the workflow runs
- **THEN** Python 3.10 is installed
- **AND** the `uv` package manager is installed and available
- **AND** uv caching is enabled for faster subsequent runs

#### Scenario: Dependency installation

- **WHEN** the environment is set up
- **THEN** project dependencies including dev extras are installed via `uv sync --all-extras`
- **AND** the test command can import all required modules

---

### Requirement: Test Execution

The CI system SHALL run the test suite and report results.

#### Scenario: Tests pass

- **WHEN** all tests pass
- **THEN** the workflow completes successfully (exit code 0)
- **AND** the GitHub check shows a green checkmark

#### Scenario: Tests fail

- **WHEN** one or more tests fail
- **THEN** the workflow fails (non-zero exit code)
- **AND** the GitHub check shows a red X
- **AND** the failure details are visible in the workflow log

#### Scenario: Test output visibility

- **WHEN** tests are executed
- **THEN** pytest is run with `-v --tb=short` options
- **AND** individual test results are visible in the workflow log

---

### Requirement: Workflow Concurrency

The CI system SHALL manage concurrent workflow runs efficiently.

#### Scenario: Concurrent runs on same PR

- **WHEN** a new commit is pushed while tests are still running for a previous commit
- **THEN** the previous workflow run is cancelled
- **AND** only the latest commit's tests run to completion

#### Scenario: Concurrent runs on different PRs

- **WHEN** multiple PRs have concurrent test runs
- **THEN** all workflow runs execute independently
- **AND** each PR shows its own test status
