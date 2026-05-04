---
agent: "agent"
description: "Generate Marp slides and HTML from ML artifacts"
---

# ML Report

Use:

- [generated-python instructions](../instructions/generated-python.instructions.md)
- [artifact contracts](../skills/artifact-contracts/SKILL.md)
- [ML reporting](../skills/ml-reporting/SKILL.md)
- [ML code review skill](../skills/ml-code-review/SKILL.md)
- #file:../../src/ml_agents_trial/presentation/templates/base.marp.md

## Role

Act as the reporter for this repository.

## Tasks

1. Confirm `artifacts/models/comparison.json` exists.
2. Implement presentation modules in `src/ml_agents_trial/presentation/` (file structure may vary by complexity):
   - Required public functions: `collect_slide_data() -> dict`, `build_slides(slide_data: dict) -> Path`.
   - Replace all Marp placeholders.
   - Copy images into `artifacts/presentation/images/` and reference relative paths.
   - Include purpose, evaluation method, model comparison, best model, limitations, and next actions.
3. Structurally review: run `/ml-code-review` with target=`src/ml_agents_trial/presentation/`. Return to implementation if FAIL.
4. ML quality review: run `/ml-quality-review` with phase=`report`, target=`src/ml_agents_trial/presentation/`. Return to implementation if FAIL.
5. Run:

```bash
.venv/bin/python src/ml_agents_trial/presentation/builder.py
npx --yes @marp-team/marp-cli artifacts/presentation/slides.md --output artifacts/presentation/slides.html
```

6. Run `uv run ruff check src/ tests/`.
7. Commit only `src/ml_agents_trial/presentation/` with:

```bash
git add src/ml_agents_trial/presentation/
STAGED=$(git diff --name-only --cached | grep 'ml_agents_trial/presentation/' | grep '\.py$' | sed 's|src/ml_agents_trial/presentation/||')
git commit -m "feat(presentation): generate slide builder

$(echo "$STAGED" | sed 's/^/- /')"
```

8. Report `artifacts/presentation/slides.html` and commit hash.
