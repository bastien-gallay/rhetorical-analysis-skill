# Tasks: add-release-script

## 1. Core Script Structure

- [x] 1.1 Create `scripts/release.py` with CLI argument parsing (argparse)
- [x] 1.2 Implement version parsing and bump logic (patch/minor/major/explicit)
- [x] 1.3 Add semver validation for explicit versions

## 2. Pyproject Management

- [x] 2.1 Implement `pyproject.toml` version reader
- [x] 2.2 Implement `pyproject.toml` version writer (preserve formatting)
- [x] 2.3 Add version-already-exists check

## 3. Release Notes

- [x] 3.1 Create initial `RELEASE.md` with header and format documentation
- [x] 3.2 Implement release notes section parser
- [x] 3.3 Implement git log extraction (since last tag or all commits)
- [x] 3.4 Implement release notes template generation
- [x] 3.5 Add interactive prompt for accepting/rejecting proposed notes
- [x] 3.6 Implement `RELEASE.md` writer (append new section)

## 4. Git Operations

- [x] 4.1 Implement tag existence check (local and remote)
- [x] 4.2 Implement annotated tag creation with release notes as message
- [x] 4.3 Implement push with confirmation prompt
- [x] 4.4 Handle push failures gracefully

## 5. Pre-flight Checks

- [x] 5.1 Add clean working directory check
- [x] 5.2 Add current branch detection and warning for non-main
- [x] 5.3 Add pyproject.toml existence and version field validation

## 6. Dry Run Mode

- [x] 6.1 Add `--dry-run` flag to CLI
- [x] 6.2 Implement action preview output
- [x] 6.3 Ensure no side effects in dry-run mode

## 7. Testing

- [x] 7.1 Add unit tests for version bump logic
- [x] 7.2 Add unit tests for release notes parsing
- [x] 7.3 Add integration test with mock git operations

## 8. Documentation

- [x] 8.1 Update `CLAUDE.md` with release script commands
- [x] 8.2 Add usage examples in script docstring

## Dependencies

- Tasks 1.x are independent and can be parallelized
- Task 2.x depends on 1.1 (CLI structure)
- Task 3.x depends on 1.1 (CLI structure)
- Task 4.x depends on 2.x and 3.x (need version and notes ready)
- Task 5.x depends on 1.1 (CLI structure)
- Task 6.x depends on all implementation tasks (1-5)
- Task 7.x can start after corresponding implementation tasks
- Task 8.x should be done last
