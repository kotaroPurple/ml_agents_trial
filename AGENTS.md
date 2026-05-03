# Codex Workflow Guide

This repository supports both Claude Code and Codex.

- Keep `.claude/` intact. It is the Claude Code configuration and must not be edited when implementing Codex-only workflow changes.
- Use `.codex/` as the Codex workflow source of truth.
- Core ML infrastructure lives in `src/ml_agents_trial/core/`; generated phase code lives under `src/ml_agents_trial/{eda,features,models,evaluation,presentation}/`.

## How To Run Codex Commands

When the user asks for `codex command: <name> ...`, read the matching file in `.codex/commands/` and follow it exactly.

Available commands:

| Request | Command file |
|---|---|
| `codex command: setup` | `.codex/commands/setup.md` |
| `codex command: analyze [CSV_PATH] [TARGET_COLUMN]` | `.codex/commands/analyze.md` |
| `codex command: engineer [TARGET_COLUMN]` | `.codex/commands/engineer.md` |
| `codex command: build [TARGET_COLUMN]` | `.codex/commands/build.md` |
| `codex command: evaluate [TARGET_COLUMN]` | `.codex/commands/evaluate.md` |
| `codex command: report` | `.codex/commands/report.md` |
| `codex command: run-pipeline [CSV_PATH] [TARGET_COLUMN]` | `.codex/commands/run-pipeline.md` |

## Commands, Agents, Skills

- Commands define the ordered workflow, checks, execution, and commit policy.
- Agents are role prompts. In Codex, read `.codex/agents/<role>.md` and perform that role yourself unless the user explicitly asks for parallel subagents.
- Skills are reusable quality standards. Repo-local skills are not assumed to auto-trigger; command and agent docs explicitly name which `.codex/skills/*/SKILL.md` files to read.

## Review Flow

For generated Python phase code:

1. Read the relevant command, agent, and skill docs.
2. Generate or update the target module with `apply_patch`.
3. Run the structural checks from `.codex/agents/code-reviewer.md`.
4. Run ML quality checks from `.codex/agents/ml-reviewer.md` where the command requires it.
5. Execute the generated module with `.venv/bin/python` or `uv run`.
6. Run `uv run ruff check src/ tests/` when the command asks for validation.
7. Commit only the files owned by that command.

Do not rely on Claude Code hooks or `.claude/settings.json`; Codex commands spell out the required checks.
