# reporter

Use this role for `codex command: report`. Generate or update the Marp slide builder under `src/ml_agents_trial/presentation/`.

## Required Reading

- `.codex/skills/artifact-contracts/SKILL.md`
- `.codex/skills/ml-reporting/SKILL.md`
- `src/ml_agents_trial/presentation/templates/base.marp.md`
- Available JSON artifacts under `artifacts/`.

## Required Output

Implement `src/ml_agents_trial/presentation/builder.py` with:

- `collect_slide_data() -> dict`
- `build_slides(slide_data: dict) -> Path`
- a `__main__` block that writes `artifacts/presentation/slides.md`.

## Rules

- Use `apply_patch` for edits and `exec_command` for validation commands.
- Replace all Marp placeholders.
- Copy images to `artifacts/presentation/images/` and reference relative paths.
- Include purpose, dataset overview, preprocessing, evaluation method, model comparison, best model, limitations, and next actions.
- Do not overstate conclusions beyond available metrics.
- Do not use Claude-specific tool names, named-agent calls, or hook syntax.
