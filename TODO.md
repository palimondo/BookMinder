# BookMinder Project TODO

## 🏗️ PROJECT CONTEXT
**BookMinder** = Second attempt (first was BookMind)
**Goal**: Create Walking Skeleton only (GOOS terminology) - minimal implementation exercising main architecture
**Constraint**: No creative feature additions - stick to defined scope
**Status**: Got sidetracked with tooling setup (uv migration) - need to refocus on core functionality

## 📌 PINNED ISSUES (High Priority)

### 1. Fix Apple Books lazy download issue
**Status**: Business Logic Bug
**Issue**: `list_books()` excludes valid books not downloaded from iCloud yet - causing test failures on MacBook Air
**Solution**: Include books from Books.plist even if not locally available, add `downloaded` status field
**Files**: `bookminder/apple_books/library.py`

### 2. Separate Unit vs Integration Tests
**Status**: Test Architecture Issue
**Issue**: Current tests are integration tests (real Apple Books) but run as unit tests, causing CI failures
**Solution**: Unit tests (mocked) for CI, integration tests (real Apple Books) for local validation
**Files**: Restructure `specs/` directory, create mocks

### 3. GitHub Actions workflow completion
**Status**: Partially Complete
**Issue**: CI workflow exists but fails due to test architecture issues above
**Solution**: Complete workflow setup once test mocking is done
**Files**: `.github/workflows/main.yml`

## 🚧 WALKING SKELETON COMPLETION

### 4. Complete Walking Skeleton - Missing CLI Entry Point
**Status**: Critical Gap for Walking Skeleton
**Issue**: README.md references `bookminder.py` CLI but it doesn't exist
**Solution**: Create minimal CLI that demonstrates book listing/search functionality
**Files**: `bookminder.py` (create), acceptance tests for CLI

---

## Requirements Status
| Requirement ID | Description | Status | Acceptance Tests | Notes |
|---------------|-------------|--------|------------------|-------|
| REQ-001       | Initial project setup | Completed | N/A | Project structure, dev environment |
| REQ-002       | List books from Apple Books | Completed | Implemented | Sort by last update date |
| REQ-003       | Extract book TOC | Not Started | Not Created | Table of contents extraction |
| REQ-004       | Extract highlights with context | Not Started | Not Created | With surrounding paragraphs |
| REQ-005       | Export to Markdown/HTML | Not Started | Not Created | For LLM consumption |

## Current Sprint
- [x] Review original vision document (ORIGINAL_VISION.md)
- [ ] Create README.md based on ORIGINAL_VISION.md
- [x] Set up project structure
- [x] Define core requirements through requirements dialogue
- [x] Create initial acceptance tests
- [x] Implement Apple Books library access
- [ ] Implement EPUB parsing and TOC extraction

## Backlog
- [x] Set up development environment
- [ ] Implement core functionality
- [ ] Build CLI interface
- [ ] Add documentation
- [ ] MCP integration

## Completed
- [x] Create project repository
- [x] Setup Python virtual environment
- [x] Install development dependencies

## Notes
- Read ORIGINAL_VISION.md for initial project scope and vision
- The README.md should be created based on a thorough review of ORIGINAL_VISION.md
- Conduct a comprehensive requirements gathering interview with the user to fully understand project scope
- The original vision may contain broader goals than previously implemented - ensure these are captured
- Follow the requirement gathering dialogue process for each new feature
- When creating README.md, ensure it reflects the complete vision rather than a narrower implementation
