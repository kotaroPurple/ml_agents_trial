# GitHub Copilot Instructions

This repository supports Claude Code, Codex, and GitHub Copilot workflows.

- `.claude/` is the Claude Code workflow source of truth.
- `.codex/` is the Codex workflow source of truth.
- `.github/` is the GitHub Copilot workflow source of truth.
- Do not edit `.claude/` or `.codex/` when implementing Copilot-only workflow changes.

## Project Shape

This is a tabular ML pipeline. Fixed infrastructure lives in `src/ml_agents_trial/core/`; generated phase code lives in:

- `src/ml_agents_trial/eda/`
- `src/ml_agents_trial/features/`
- `src/ml_agents_trial/models/`
- `src/ml_agents_trial/evaluation/`
- `src/ml_agents_trial/presentation/`

Generated artifacts are written under `artifacts/` and are not source-controlled.

## Copilot Workflow

Use `.github/prompts/*.prompt.md` as reusable command prompts:

- `/ml-setup`
- `/ml-analyze`
- `/ml-engineer`
- `/ml-build`
- `/ml-evaluate`
- `/ml-report`
- `/ml-run-pipeline`

Use `.github/instructions/*.instructions.md` for short always-on or path-specific rules.
Use `.github/skills/*/SKILL.md` for detailed task-specific Agent Skills that Copilot can load when relevant.

## Engineering Rules

- Keep generated code scoped to the command-owned phase directory.
- Use `ml_agents_trial.core` for shared config, IO, and metrics.
- Avoid cross-imports between generated phase directories.
- Each generated phase directory must have at least one executable `if __name__ == "__main__":` entrypoint.
- Validate Python changes with `uv run ruff check src/ tests/` and `uv run pytest tests/`.
- Do not rely on Claude Code hooks or settings; Copilot prompts must spell out checks explicitly.
