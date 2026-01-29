# Scripts Catalog

> **Template for Script Registry**
>
> **AI Agents: MUST check this catalog before creating new scripts.**
>
> Maintain this catalog to track all permanent automation scripts. If a similar script exists, use or extend it instead of creating a new one.

---

## Quick Reference

| Category | Location | Description |
|----------|----------|-------------|
| Data | `scripts/data/` | Data import/export, transformations |
| Migration | `scripts/migration/` | Schema and data migrations |
| Utils | `scripts/utils/` | General utilities |
| Reports | `scripts/reports/` | Report generation |
| Maintenance | `scripts/maintenance/` | Cleanup, health checks |

---

## Data Processing (`scripts/data/`) <!-- CUSTOMIZE -->

| Script | Description | Usage |
|--------|-------------|-------|
| *No scripts yet* | — | — |

---

## Migration (`scripts/migration/`) <!-- CUSTOMIZE -->

| Script | Description | Usage |
|--------|-------------|-------|
| *No scripts yet* | — | — |

---

## Utilities (`scripts/utils/`) <!-- CUSTOMIZE -->

| Script | Description | Usage |
|--------|-------------|-------|
| `scripts/context.py` | Core JIT context management tool for agents | `python3 scripts/context.py fetch <key>` |
| `scripts/bootstrap.py` | Injects protocol files into other projects | `uv run scripts/bootstrap.py <target_dir>` |


---

## Reports (`scripts/reports/`) <!-- CUSTOMIZE -->

| Script | Description | Usage |
|--------|-------------|-------|
| *No scripts yet* | — | — |

---

## Maintenance (`scripts/maintenance/`) <!-- CUSTOMIZE -->

| Script | Description | Usage |
|--------|-------------|-------|
| *No scripts yet* | — | — |

---

## Temporary Scripts

Location: `scripts/temp/` (gitignored)

Temp scripts are for current branch/task only. Not cataloged here.

**To promote a temp script:**
1. Move to appropriate `scripts/<category>/`
2. Add entry to this catalog
3. Commit both changes
