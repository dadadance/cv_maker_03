# Coding Standards

> **Template for Engineering Guidelines**
>
> These standards apply to all code in this project. AI agents MUST read this before generating code. Customize the sections below to match your project's specific paradigm and library preferences.

---

## 1. Core Philosophy

### 1.1. Paradigm Preferences (Ordered)
1. **Functional Programming** over Object-Oriented Programming whenever possible
2. **Pure Functions** - no side effects, deterministic outputs
3. **Immutability** - prefer immutable data structures
4. **Composition** over inheritance
5. **Partial Functions / Currying** - use for reusable, configurable logic

### 1.2. Library Preferences (Ordered)
1. **Native/Standard Library First** - always prefer built-in solutions
2. **Well-Established Third-Party** - only when native is insufficient
3. **Minimal Dependencies** - every dependency is a liability

### 1.3. General Principles
- **Simplicity:** Code must be simple, concise, and readable. Avoid over-engineering.
- **DRY (Don't Repeat Yourself):** Extract common logic, but not prematurely.
- **KISS (Keep It Simple, Stupid):** The simplest solution that works is often the best.
- **YAGNI (You Aren't Gonna Need It):** Don't build for hypothetical future requirements.
- **Separation of Concerns:** Keep logic, data, and presentation separate.
- **Single Responsibility:** Each function/module does one thing well.
- **Fail Fast:** Validate inputs early, return/throw immediately on failure.

---

## 2. Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Variables | `snake_case` | `user_count`, `is_valid` |
| Functions | `snake_case` | `get_user()`, `calculate_total()` |
| Classes | `PascalCase` | `UserService`, `HttpClient` |
| Constants | `UPPER_SNAKE_CASE` | `MAX_RETRIES`, `API_URL` |
| Private/Internal | `_leading_underscore` | `_internal_helper()` |
| Boolean Variables | `is_`, `has_`, `can_`, `should_` prefix | `is_active`, `has_permission` |

### 2.1. Naming Guidelines
- Names should reveal intent - avoid abbreviations unless universally understood
- Functions should be verbs: `get_`, `set_`, `calculate_`, `validate_`, `fetch_`
- Predicates should return boolean: `is_valid()`, `has_access()`, `can_proceed()`
- Avoid generic names: `data`, `info`, `temp`, `result` (be specific)

### 2.2. Function Naming by Granularity

**Rule:** The more granular (low-level) a function, the more descriptive its name. Functions that compose others should have broader, more general names.

| Level | Function Type | Naming Style | Example |
|-------|--------------|--------------|---------|
| Low | Atomic operation | Highly specific | `extract_email_domain()`, `normalize_phone_number()` |
| Mid | Single transformation | Specific verb + noun | `validate_user_input()`, `format_currency()` |
| High | Orchestration/pipeline | General/abstract | `process_order()`, `handle_request()` |

```
# Low-level: very descriptive
def remove_whitespace(text: str) -> str: ...
def convert_to_lowercase(text: str) -> str: ...
def strip_special_characters(text: str) -> str: ...

# High-level: general name, composes the above
def sanitize_input(text: str) -> str:
    """Clean and normalize user input for storage."""
    return pipe(
        text,
        remove_whitespace,
        convert_to_lowercase,
        strip_special_characters,
    )
```

---

## 3. Function Design

### 3.1. Core Principles

| Principle | Description |
|-----------|-------------|
| **Single Purpose** | One function = one job. If you need "and" to describe it, split it. |
| **Referential Transparency** | Same input → same output, always. No hidden dependencies. |
| **Consistent Return Type** | A function should always return the same type (use `Optional[T]` or `Result[T, E]` for failure cases). |
| **Short & Readable** | 5-15 lines ideal. Max 20. If longer, extract smaller functions. |
| **Type Annotated** | All parameters and return types must have type hints. |
| **Documented** | Brief docstring: what it does (not how), return type, edge cases. |

### 3.2. Function Signature Standards

Every function MUST have:
1. **Type hints** for all parameters and return value
2. **Brief docstring** (1-2 lines for simple functions)
3. **Consistent return type** (never `Union[str, int, None]` chaos)

```python
def calculate_discount(price: float, percentage: float) -> float:
    """Apply percentage discount to price. Returns discounted price."""
    return price * (1 - percentage / 100)

def find_user_by_email(email: str) -> Optional[User]:
    """Lookup user by email. Returns None if not found."""
    ...
```

### 3.3. Pure Functions & Referential Transparency (Preferred)

**Referential transparency:** A function call can be replaced with its result without changing program behavior.

```python
# GOOD: Pure, referentially transparent
def add_tax(price: float, tax_rate: float) -> float:
    """Add tax to price. Pure function - no side effects."""
    return price * (1 + tax_rate)

# BAD: Impure - depends on external state
def add_tax(price: float) -> float:
    return price * (1 + GLOBAL_TAX_RATE)  # Hidden dependency!

# BAD: Impure - side effect
def add_tax(price: float, tax_rate: float) -> float:
    result = price * (1 + tax_rate)
    log_to_database(result)  # Side effect!
    return result
```

### 3.4. Function Composition & Piping

**Prefer piping/composition** for multi-step transformations. This makes data flow explicit and code self-documenting.

```python
from functools import reduce

# Simple pipe implementation
def pipe(value, *functions):
    """Pass value through a sequence of functions."""
    return reduce(lambda v, f: f(v), functions, value)

# Low-level functions: specific, single-purpose
def parse_date(raw: str) -> datetime:
    """Parse ISO date string to datetime."""
    return datetime.fromisoformat(raw)

def extract_year(dt: datetime) -> int:
    """Extract year from datetime."""
    return dt.year

def is_leap_year(year: int) -> bool:
    """Check if year is a leap year."""
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

# High-level function: composes the above, general name
def check_date_is_leap_year(date_string: str) -> bool:
    """Determine if the given date falls in a leap year."""
    return pipe(
        date_string,
        parse_date,
        extract_year,
        is_leap_year,
    )
```

**Benefits of piping:**
- Each step is testable in isolation
- Flow reads top-to-bottom (or left-to-right)
- Easy to insert/remove/reorder steps
- Reader understands the transformation at a glance

### 3.5. Partial Functions & Currying

Use `functools.partial` to create specialized versions of general functions.

```python
from functools import partial

# General function
def format_currency(amount: float, symbol: str, decimals: int) -> str:
    """Format amount as currency string."""
    return f"{symbol}{amount:.{decimals}f}"

# Specialized versions via partial application
format_usd = partial(format_currency, symbol="$", decimals=2)
format_eur = partial(format_currency, symbol="€", decimals=2)
format_btc = partial(format_currency, symbol="₿", decimals=8)

# Usage: format_usd(99.5) -> "$99.50"
```

### 3.6. Function Guidelines Summary

| Do | Don't |
|----|-------|
| Single responsibility | Multiple responsibilities ("and" in description) |
| 5-15 lines | 50+ line monoliths |
| Type hints everywhere | Untyped parameters or returns |
| Return consistent type | Return different types conditionally |
| Pure when possible | Hidden state dependencies |
| Compose small functions | Deeply nested logic |
| Early return on failure | Deep nesting with late validation |
| Max 3-4 parameters | 6+ parameters (use dataclass) |

---

## 4. Error Handling

### 4.1. Principles
- **Fail Fast:** Validate at boundaries (user input, external APIs), not deep in logic.
- **Explicit Errors:** Use specific exception types, not generic ones.
- **No Silent Failures:** Never catch and ignore exceptions without logging.
- **Return Types over Exceptions:** For expected failures, consider `Optional`, `Result`, or union types.

### 4.2. Guidelines
```
# GOOD: Early validation with clear error
def process_user(user_id: int) -> User:
    if user_id <= 0:
        raise ValueError(f"Invalid user_id: {user_id}")
    # ... rest of logic

# BAD: Deep validation, unclear error
def process_user(user_id: int) -> User:
    # ... lots of code
    if some_condition:
        if user_id <= 0:  # Too late!
            raise Exception("Error")  # Too vague!
```

---

## 5. Code Structure

### 5.1. Module Organization
```
module/
├── __init__.py      # Public API exports
├── core.py          # Core business logic (pure functions)
├── models.py        # Data structures / types
├── services.py      # Side-effectful operations (I/O, DB, API)
├── utils.py         # Generic utilities
└── constants.py     # Configuration constants
```

### 5.2. Import Order
1. Standard library imports
2. Third-party imports
3. Local/project imports

Each group separated by a blank line, alphabetically sorted within groups.

### 5.3. Headless Architecture (Mandatory)

**Principle:** ALL core functionality MUST be accessible via command line. UI is optional; CLI is not.

#### Why Headless-First?
- **Scriptability:** Automate workflows, chain commands, integrate with CI/CD
- **Testability:** Easier to test without UI dependencies
- **Flexibility:** Same logic powers CLI, API, UI, or other interfaces
- **Debugging:** Direct access to functionality without UI layers

#### CLI Design Pattern
```
project/
├── cli/
│   ├── __init__.py
│   └── commands.py      # CLI entry points
├── core/
│   └── logic.py         # Pure business logic (UI-agnostic)
├── services/
│   └── external.py      # I/O operations
├── scripts/
│   ├── temp/            # Temporary scripts (gitignored) - current branch only
│   ├── data/            # Data processing scripts
│   ├── migration/       # Migration scripts
│   └── utils/           # Utility scripts
└── SCRIPTS_CATALOG.md   # Index of all permanent scripts
```

#### CLI Entry Point Template
```python
#!/usr/bin/env python3
"""
Process data files.

Usage: uv run scripts/process_data.py <input_file> [--output <path>] [--verbose]
"""
import argparse
import sys
from core.logic import process_data

def main() -> int:
    """CLI entry point. Returns exit code."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_file", help="Path to input file")
    parser.add_argument("--output", "-o", default="output.json", help="Output path")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    args = parser.parse_args()

    try:
        result = process_data(args.input_file, args.output, verbose=args.verbose)
        print(f"Success: {result}")
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
```

#### CLI Guidelines
| Rule | Description |
|------|-------------|
| **Self-documenting** | ALL args MUST have `help=` text. The CLI is its own documentation. |
| **Exit codes** | Return 0 on success, non-zero on failure |
| **Stderr for errors** | Errors go to stderr, results to stdout |
| **Parseable output** | Support `--json` flag for machine-readable output |
| **Quiet mode** | Support `-q/--quiet` to suppress non-essential output |

#### Argument Documentation (Mandatory)

**Every argument MUST be self-documenting via `help=`.** Running `script.py --help` should provide complete usage instructions.

```python
# GOOD: Fully documented arguments
parser.add_argument(
    "input_file",
    help="Path to CSV file containing user data (required)"
)
parser.add_argument(
    "--output", "-o",
    default="output.json",
    help="Output file path (default: output.json)"
)
parser.add_argument(
    "--format", "-f",
    choices=["json", "csv", "yaml"],
    default="json",
    help="Output format: json, csv, or yaml (default: json)"
)
parser.add_argument(
    "--dry-run",
    action="store_true",
    help="Preview changes without writing to disk"
)

# BAD: Missing or vague help text
parser.add_argument("input_file")  # No help!
parser.add_argument("--output", "-o", help="output")  # Too vague!
```

**The `--help` output IS the documentation.** No separate docs needed for CLI usage.

### 5.4. Scripts Management (Mandatory)

#### Directory Structure

| Directory | Purpose | Git Status |
|-----------|---------|------------|
| `scripts/temp/` | Temporary, branch-specific scripts | **Gitignored** |
| `scripts/<category>/` | Permanent, reusable scripts | Committed |

**Categories** (create as needed): `data/`, `migration/`, `utils/`, `reports/`, `maintenance/`

#### Scripts Catalog (`SCRIPTS_CATALOG.md`)

Maintain a catalog at project root listing ALL permanent scripts. AI agents MUST consult this before creating new scripts.

```markdown
# Scripts Catalog

## Data Processing (`scripts/data/`)

| Script | Description | Usage |
|--------|-------------|-------|
| `export_users.py` | Export users to CSV | `uv run scripts/data/export_users.py --format csv` |
| `import_data.py` | Import from JSON | `uv run scripts/data/import_data.py <file>` |

## Migration (`scripts/migration/`)

| Script | Description | Usage |
|--------|-------------|-------|
| `migrate_v1_to_v2.py` | Migrate old schema | `uv run scripts/migration/migrate_v1_to_v2.py` |
```

#### Workflow Rules

| Rule | Description |
|------|-------------|
| **Check catalog first** | Before creating a script, AI MUST check `SCRIPTS_CATALOG.md` for existing solutions |
| **Temp for experiments** | Use `scripts/temp/` for one-off or WIP scripts |
| **Promote if reusable** | Move useful temp scripts to permanent location + update catalog |
| **Clean on merge** | `scripts/temp/` should be empty (gitignored handles this) |
| **Always document** | Every permanent script must be in the catalog with usage example |

#### .gitignore Entry

```gitignore
# Temporary scripts (branch-specific, not committed)
scripts/temp/
```

---

## 6. Documentation

### 6.1. When to Document
- **Public APIs:** Always document public functions/classes
- **Complex Logic:** When the "why" isn't obvious from the code
- **Workarounds:** Explain non-obvious solutions or hacks

### 6.2. When NOT to Document
- Self-explanatory code (good names eliminate need for comments)
- Obvious implementations
- TODOs without context or owner

### 6.3. Docstring Format
```
def fetch_user(user_id: int, include_deleted: bool = False) -> Optional[User]:
    """
    Retrieve a user by their unique identifier.

    Args:
        user_id: The unique identifier of the user.
        include_deleted: If True, includes soft-deleted users.

    Returns:
        The User object if found, None otherwise.

    Raises:
        ConnectionError: If the database is unreachable.
    """
```

---

## 7. Testing Standards

### 7.1. Test Structure
- **Arrange-Act-Assert (AAA):** Clear separation in each test
- **One Assertion Per Test:** Test one behavior at a time
- **Descriptive Names:** `test_<function>_<scenario>_<expected_result>`

### 7.2. Test Naming Examples
```
def test_calculate_discount_with_zero_percentage_returns_zero():
    ...

def test_fetch_user_with_invalid_id_raises_value_error():
    ...
```

### 7.3. Coverage Goals
- **Unit Tests:** Cover all pure functions and business logic
- **Integration Tests:** Cover boundaries (APIs, DB, external services)
- **Happy Path + Edge Cases:** Test both success and failure scenarios

---

## 8. Tech-Specific Rules <!-- CUSTOMIZE -->

> Add framework/language-specific rules below as needed.

### Python
- Use type hints for all function signatures
- Use `dataclasses` or `NamedTuple` for structured data
- Prefer `pathlib` over `os.path`
- Use `with` statements for resource management

### JavaScript/TypeScript
- Use `const` by default, `let` when mutation needed, never `var`
- Prefer arrow functions for callbacks
- Use TypeScript strict mode

### [Add more as needed]

---

## 9. Anti-Patterns to Avoid

| Anti-Pattern | Instead |
|--------------|---------|
| God classes/functions | Split into focused units |
| Deep nesting (>3 levels) | Early returns, extraction |
| Magic numbers/strings | Named constants |
| Mutable global state | Dependency injection, pure functions |
| Premature abstraction | Wait for 3+ duplications |
| Comments explaining "what" | Refactor to self-documenting code |
| Catching generic exceptions | Catch specific exception types |
| Boolean parameters | Use enums or separate functions |
