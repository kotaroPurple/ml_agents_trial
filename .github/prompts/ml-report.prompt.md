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
2. Implement `src/ml_agents_trial/presentation/builder.py` with `collect_slide_data()` and `build_slides(slide_data)`.
3. Replace all Marp placeholders.
4. Copy images into `artifacts/presentation/images/` and reference relative paths.
5. Include purpose, evaluation method, model comparison, best model, limitations, and next actions.
6. Structurally review imports, ruff, and `__main__`.
7. Perform ML quality review for artifact consistency and conclusion strength. Return to implementation if review fails.
8. Run:

```bash
.venv/bin/python src/ml_agents_trial/presentation/builder.py
npx --yes @marp-team/marp-cli artifacts/presentation/slides.md --output artifacts/presentation/slides.html
```

9. Run `uv run ruff check src/ tests/`.
10. Commit only `src/ml_agents_trial/presentation/` with `feat(presentation): generate slide builder`.
11. Report `artifacts/presentation/slides.html` and commit hash.
