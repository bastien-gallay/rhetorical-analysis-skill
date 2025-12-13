# Tasks: add-ci-testing

## Implementation Order

### 1. Create test workflow file

- Create `.github/workflows/test.yml`
- Configure triggers: `push` to main, `pull_request` to main
- Add concurrency settings to cancel stale runs

**Verification**: File exists and YAML is valid (`uv run python -c "import yaml; yaml.safe_load(open('.github/workflows/test.yml'))"`)

### 2. Add environment setup steps

- Checkout repository
- Setup Python 3.10 via `actions/setup-python@v5`
- Install uv via `astral-sh/setup-uv@v4` with caching enabled
- Install dependencies via `uv sync --all-extras`

**Verification**: Run workflow manually or push test branch

### 3. Add test execution step

- Run `uv run pytest tests/ -v --tb=short`
- Ensure exit code propagates correctly

**Verification**: Push a branch and verify tests run in Actions tab

### 4. Update backlog

- Mark CI/CD item as complete in `docs/backlog.md`

**Verification**: `grep -q "CI/CD" docs/backlog.md` confirms update

## Parallelizable Work

Tasks 1-3 are sequential (each depends on the previous).
Task 4 can be done after task 3 passes verification.

## Dependencies

- Requires GitHub repository access (already configured via existing packaging workflow)
- Uses same GitHub Actions and setup as `package-skill.yml` for consistency
