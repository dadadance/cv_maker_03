# Requirement: [Feature/Task Name]

> Copy this template for each new feature branch. Name the file to match the branch scope.

---

## 1. Overview

**Summary:** [One-line description of what this feature/task accomplishes]

**Branch:** `[branch-type]/yyyymmdd-hhmmss-[name]`

**Priority:** High / Medium / Low

**Estimated Scope:** Small (hours) / Medium (days) / Large (week+)

---

## 2. Acceptance Criteria

> Define what "done" looks like. Be specific.

- [ ] [Specific, measurable outcome]
- [ ] [Specific, measurable outcome]
- [ ] [Specific, measurable outcome]

---

## 3. Implementation Checklist

> AI Agent checks this list before and during implementation. Delete items that don't apply.

### Core Implementation
- [ ] **Data/Models:** Define or update data structures
- [ ] **Business Logic:** Implement core functionality (pure functions preferred)
- [ ] **I/O / Services:** Implement side-effectful operations (API, DB, files)
- [ ] **Interface/UI:** Implement user-facing components (if applicable)

### Quality Assurance
- [ ] **Unit Tests:** Cover new pure functions and logic
- [ ] **Integration Tests:** Cover boundaries and workflows
- [ ] **Manual Testing:** Verify expected behavior

### Finalization
- [ ] **Code Review:** Self-review or peer review
- [ ] **Documentation:** Update relevant docs (README, API docs, etc.)
- [ ] **PROGRESS.md:** Update project progress report

---

## 4. Dependencies / Blockers

> List anything that must be done first or could block progress.

| Dependency | Status | Notes |
|------------|--------|-------|
| [Other task/feature] | Pending / Done | [Context] |
| [External factor] | Blocked / Clear | [Context] |

---

## 5. Technical Notes

> Implementation details, constraints, decisions, API specs, etc.

### Approach
- [Describe the implementation approach]

### Constraints
- [Any limitations or requirements]

### API / Interface (if applicable)
```
[Endpoint, function signature, or interface definition]
```

### Related Files
- `path/to/file.py` — [purpose]
- `path/to/other.py` — [purpose]

---

## 6. Open Questions

> Unresolved decisions. Answer before implementation or flag for user input.

- [ ] **Q:** [Question about implementation or requirements]
  - **A:** [Answer when resolved]

---

## 7. Notes / History

| Date | Note |
|------|------|
| YYYY-MM-DD | Feature branch created |
| YYYY-MM-DD | [Update/decision/change] |
