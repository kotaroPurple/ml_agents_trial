---
name: ml-code-review
description: Use when reviewing generated ML phase Python code for structural quality; checks import boundaries, ruff, executable entrypoints, matplotlib backend, and cross-import violations.
---

# ML Code Review

Use this skill to review generated Python phase code. Do not edit files while acting as the reviewer; return PASS or FAIL with fix instructions.

## Checks

- Import boundary (core module name from copilot-instructions.md > プロジェクト設定):
  - `{core module}.*` is allowed.
  - External packages are allowed.
  - Same phase-directory imports are allowed.
  - Cross-imports between generated phase directories are not allowed.
- Directory-based checking:
  - When given a directory, enumerate all `.py` files with `find [dir] -name "*.py" -not -path "*__pycache__*" | sort`.
  - Check every file for import boundary and ruff.
  - At least one file per directory must contain `if __name__ == "__main__":` (utility files do not need it).
- Ruff:
  - Run `uv run ruff check [target]` or the command-specific ruff check.
- Plot backend:
  - Plot modules must call `matplotlib.use("Agg")` before importing `matplotlib.pyplot`.
- Public functions should keep type hints.

## Output Format

PASS:

```text
PASS: [target]
- Import boundary: OK
- Ruff: OK
- Entrypoint: OK
- Plot backend: OK
```

FAIL:

```text
FAIL: [target]
Issues:
- [file:line] [problem]

Fix instructions:
- [specific requested change]
```
