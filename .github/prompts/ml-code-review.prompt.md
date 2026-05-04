---
agent: "agent"
description: "Review generated ML phase Python code for structural issues"
---

# ML Code Review

Target path: `${input:target_path:src/ml_agents_trial/}`

Use:

- [generated-python instructions](../instructions/generated-python.instructions.md)
- [ML code review skill](../skills/ml-code-review/SKILL.md)

Do not edit files. Return PASS or FAIL with concrete fix instructions.

## Checks

1. Enumerate target Python files:

```bash
find ${input:target_path:src/ml_agents_trial/} -name "*.py" -not -path "*__pycache__*" | sort
```

2. Check imports (core module from copilot-instructions.md > プロジェクト設定):
   - `{core module}.*` is allowed.
   - External packages are allowed.
   - Same phase-directory imports are allowed.
   - Cross-imports between generated phase directories are not allowed.
3. Run ruff on the target.
4. Confirm at least one `if __name__ == "__main__":` exists when reviewing a generated phase directory.

## Output

Return:

```text
PASS: [target]
...
```

or:

```text
FAIL: [target]
Issues:
- ...
Fix instructions:
- ...
```
