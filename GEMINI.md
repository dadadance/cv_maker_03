# Gemini Agent Protocol (JIT Context)

## 0. Identity & Safety (MANDATORY)
You are an autonomous development agent.
1. **Safety First:** ALWAYS explain your plan before running shell commands.
2. **Stop on Error:** If a command fails, STOP and analyze. Do not loop.
3. **Paging System:** To avoid context overflow, DO NOT read large docs. Use the triggers below.

## 1. Context Triggers
Before starting any major task, fetch the required context.

| Task / Need | Command |
| :--- | :--- |
| **Project Setup & Rules** | `python3 scripts/context.py fetch protocol:init` |
| **Branching & Scope** | `python3 scripts/context.py fetch protocol:branching` |
| **Coding Standards** | `python3 scripts/context.py fetch protocol:standards` |
| **Scripts Catalog** | `python3 scripts/context.py fetch protocol:scripts` |
| **Current Progress** | `python3 scripts/context.py fetch protocol:progress` |

## 2. Dynamic Retrieval
- List all keys: `python3 scripts/context.py list`
- Maintain `docs/context_registry.json` if new documentation categories are added.

## 3. Mandatory Workflow
- **Confirm Branch:** Ask "Are we on the correct branch?"
- **Read Requirements:** Fetch context for the current task scope.
- **Update Progress:** Update `docs/PROGRESS.md` after completion.
