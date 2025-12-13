# Tasks: add-github-packaging-workflow

## Implementation Tasks

### 1. Create GitHub Actions workflow directory structure

- [ ] Create `.github/workflows/` directory
- [ ] Verify directory permissions and structure

**Validation**: Directory exists and is tracked by Git

**Dependencies**: None

---

### 2. Create package-skill.yml workflow file

- [ ] Create `.github/workflows/package-skill.yml`
- [ ] Configure workflow triggers (on tag push matching `v*`)
- [ ] Set up Python 3.10+ environment
- [ ] Install `uv` package manager
- [ ] Configure checkout with full Git history (for version detection)

**Validation**: Workflow file passes GitHub Actions YAML validation

**Dependencies**: Task 1

---

### 3. Add packaging job steps

- [ ] Add step to run `uvx --from . python scripts/package_skill.py --output dist/`
- [ ] Add step to extract version from generated filename
- [ ] Add step to generate SHA256 checksum of the .skill archive
- [ ] Add step to create checksums.txt file with hash and filename
- [ ] Configure artifact retention settings

**Validation**: Job successfully executes package_skill.py script and generates checksums

**Dependencies**: Task 2

---

### 4. Add GitHub Release creation

- [ ] Add step to create GitHub Release using tag name
- [ ] Extract release notes from tag annotation or generate default notes
- [ ] Configure release as draft or published based on tag pattern (pre-release for `-alpha`, `-beta`)
- [ ] Upload `.skill` archive as release asset
- [ ] Upload `checksums.txt` as release asset

**Validation**: Release is created with correct metadata and both assets (archive + checksums)

**Dependencies**: Task 3

---

### 5. Test workflow with test tag

- [ ] Create a test tag locally (ex: `v0.1.0-test`)
- [ ] Push tag to GitHub
- [ ] Verify workflow runs successfully
- [ ] Verify release is created with artifact
- [ ] Download and validate the .skill archive
- [ ] Clean up test tag and release

**Validation**: Full workflow executes end-to-end successfully

**Dependencies**: Task 4

---

### 6. Update README with download instructions

- [ ] Add "Download" or "Installation" section with link to GitHub Releases
- [ ] Add release badge showing latest version
- [ ] Document how to verify package integrity using checksums
- [ ] Include example commands for SHA256 verification (Linux/macOS/Windows)

**Validation**: README contains clear download and verification instructions

**Dependencies**: Task 5 (after validation)

---

### 7. Document release workflow for maintainers

- [ ] Update README.md or add RELEASING.md with maintainer instructions
- [ ] Document tagging conventions (`v<major>.<minor>.<patch>`)
- [ ] Document how to create releases (tag creation process)
- [ ] Document checksum verification process
- [ ] Add troubleshooting section for common issues

**Validation**: Clear instructions for maintainers to create and verify releases

**Dependencies**: Task 6

---

## Notes

- **Parallel work**: Tasks 1-4 can be implemented sequentially in a single commit
- **Testing**: Task 5 is critical - must validate before merging
- **Rollback**: If workflow fails, tags can be deleted and recreated
- **Permissions**: Workflow needs `contents: write` permission for creating releases
