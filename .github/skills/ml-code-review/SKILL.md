---
name: ml-code-review
description: Use when reviewing generated ML phase Python code for structural quality; checks import boundaries, ruff, executable entrypoints, matplotlib backend, and cross-import violations.
---

# ML Code Review

Use this skill to review generated Python phase code. Do not edit files while acting as the reviewer; return PASS or FAIL with fix instructions.

## Checks

- Import boundary:
  - `ml_agents_trial.core.*` is allowed.
  - External packages are allowed.
  - Same-package imports are allowed.
  - Cross-imports between generated phase directories are not allowed.
- Ruff:
  - Run `uv run ruff check [target]` or the command-specific ruff check.
- Entrypoint:
  - For each generated phase directory, at least one file must contain `if __name__ == "__main__":`.
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
