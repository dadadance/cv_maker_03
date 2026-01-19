# CV Maker 03 - AI Development Context

---

## 0. Core Protocol: Context & Requirements (MANDATORY)

To minimize hallucination and ensure strict alignment with project goals, the AI Agent **MUST** follow this sequence at the start of every task:

1.  **Analyze & Confirm:** Identify the active git branch. **Explicitly ask the user:** _"Are we on the correct branch for this task, and are the relevant requirements in `docs/requirements/` up to date?"_
2.  **Locate Requirements:** Once confirmed, navigate to `docs/requirements/` and read the specific file matching the branch's scope.
3.  **Verify Status:** Check the **"Implementation Checklist"** section within that same requirements file to see what is already done.
4.  **Align & Act:** Only proceed with code generation or modification after establishing this grounded context.

### 0.1. Safety & Autonomy (Strict)
- **Ask Before Acting:** You MUST describe the intended action and wait for user confirmation before running any shell command or modifying files.
- **Explicit Permission:** You are only allowed to run autonomously if the user explicitly grants permission (e.g., "Run autonomously", "Go ahead").
- **Stop-on-Error:** If a command fails, **STOP**. Analyze the error, explain it to the user, and propose a fix. Do not blindly retry or loop.

**Universal Rule:** This "Branch -> Requirement (with Status)" workflow is the default standard for ALL projects.

## 1. Project Overview

- **Goal:** AI-powered CV/Resume maker with JSON-based storage, versioned experiences, and AI-assisted tailoring
- **Tech Stack:** Python 3.13, Django 6.0, HTMX, Tailwind CSS, Google Gemini (Flash 1.5), WeasyPrint, SQLite (minimal, for Django internals)

### 1.1. Architecture
- **Storage:** Single JSON file (`resume_bank/data.json`) - git-trackable
- **Versioning:** Experience versions nested under parent experience
- **IDs:** Human-readable (exp_001, skill_python, jd_001, etc.)

### 1.2. Tooling & Environment
- **Package Manager:** `uv` - STRICTLY USE THIS.
- **Environment:** Local `.venv`
- **Run Commands:**
  - Server: `uv run python manage.py runserver`
  - Migrations: `uv run python manage.py migrate`
  - Test: `uv run python manage.py test`
  - CLI: `uv run python -m cli.main <command>`

## 2. Coding Standards & Conventions

- **Standard Compliance:** All code must strictly follow functional programming patterns.
- **Research First:** Before writing code, verify the latest recommended patterns for the specific library/framework.

### 2.1. Core Principles
1. **Functional Programming** over OOP whenever possible
2. **Pure Functions** - no side effects, deterministic outputs
3. **Immutability** - prefer immutable data structures
4. **Composition** over inheritance
5. **Type Hints** - all functions must have type annotations

### 2.2. Strict Protocol: Git Branching & Scope

**Mandatory Rules:**

1.  **Naming Convention:** Branch names MUST follow: `<branch-type>/yyyymmdd-hhmmss-<meaningful-name>`
2.  **Scope Enforcement:** Strictly forbidden from tasks outside the branch's defined scope.
3.  **Atomic Changes:** Keep file modifications atomic. Do not mix refactoring with feature work.
4.  **Conventional Commits:** Format: `feat: ...`, `fix: ...`, `docs: ...`, `refactor: ...`, `test: ...`

### 2.3. Documentation Protocol (Mandatory)

**Always finish working on a branch by updating:**

1.  **Project Progress Report:** `docs/PROGRESS.md`
2.  **Branch/Topic Specific Doc:** `docs/requirements/<feature>.md`
3.  **Scripts Catalog:** `SCRIPTS_CATALOG.md` (if scripts added)

### 2.4. Verification Standard
- **Test Command:** `uv run python manage.py test`
- **Lint Command:** `uv run ruff check .`
- **Definition of Done:** Tests pass, lint passes, docs updated.

### 2.5. Architectural Constraints
- **Headless-First:** ALL core functionality MUST be accessible via CLI. No UI-only features.
- **CLI Entry Points:** `uv run python -m cli.main <command>`
- **JSON Repository:** All data operations go through `core/services/repository.py`
- **Security:** Never commit secrets. Use `.env` file with `python-dotenv`.

### 2.6. Directory Structure
```
cv-maker-03/
├── config/              # Django settings
├── core/                # Django app
│   ├── services/        # Business logic
│   │   ├── repository.py    # JSON file operations
│   │   ├── ai_service.py    # Gemini integration
│   │   └── exporter.py      # PDF generation
│   ├── views.py
│   └── templates/
├── cli/                 # CLI entry points (Typer)
│   ├── main.py
│   └── commands/
├── resume_bank/         # Data storage
│   └── data.json
├── docs/
│   ├── PROGRESS.md
│   └── requirements/
├── scripts/
│   └── temp/            # Gitignored temp scripts
├── pyproject.toml
└── CLAUDE.md
```

## 3. Data Schema

```json
{
  "profile": {
    "name": "string",
    "emails": ["string"],
    "phones": ["string"],
    "location": "string",
    "linkedin": "string",
    "github": "string",
    "portfolio": "string",
    "headline": "string",
    "summary": "string"
  },
  "skills": [{
    "id": "skill_001",
    "name": "Python",
    "category": "Language|Framework|Tool|Database|Cloud|Soft",
    "level": "Junior|Mid|Senior|Expert",
    "years": 5
  }],
  "experiences": [{
    "id": "exp_001",
    "company": "Acme Corp",
    "start_date": "2020-03",
    "end_date": "2023-06",
    "is_current": false,
    "versions": [{
      "id": "exp_001_v1",
      "title": "Senior Developer",
      "description": "...",
      "bullets": ["...", "..."],
      "skills": ["skill_001", "skill_002"],
      "created_at": "ISO datetime",
      "is_default": true
    }]
  }],
  "job_descriptions": [{
    "id": "jd_001",
    "title": "Backend Engineer",
    "company": "Target Co",
    "text": "Full JD text...",
    "url": "...",
    "created_at": "ISO datetime"
  }],
  "resumes": [{
    "id": "resume_001",
    "name": "Backend Resume for Target Co",
    "jd_id": "jd_001",
    "selected_versions": ["exp_001_v1", "exp_002_v2"],
    "selected_skills": ["skill_001", "skill_003"],
    "custom_summary": "...",
    "show_github": true,
    "show_linkedin": true,
    "created_at": "ISO datetime",
    "updated_at": "ISO datetime"
  }]
}
```
