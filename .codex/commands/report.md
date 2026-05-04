# codex command: report

Generate Marp slides from ML artifacts.

## Arguments

No arguments.

## Steps

1. Confirm `artifacts/models/comparison.json` exists.
2. Read:
   - `.codex/agents/reporter.md`
   - `.codex/skills/artifact-contracts/SKILL.md`
   - `.codex/skills/ml-reporting/SKILL.md`
3. Act as `reporter` and implement `src/ml_agents_trial/presentation/builder.py` using `apply_patch`.
4. Act as `code-reviewer` by reading `.codex/agents/code-reviewer.md` and checking `src/ml_agents_trial/presentation/`.
   - If review returns FAIL, fix the reported issues as `reporter`, then repeat this review before continuing.
5. Domain review:
   - All Marp placeholders are replaced.
   - Image paths are relative to `artifacts/presentation/images/`.
   - Purpose, evaluation method, limitations, and next actions are included.
   - If review fails, fix the issue and return to step 4.
6. Act as `ml-reviewer` by reading `.codex/agents/ml-reviewer.md` and checking artifact consistency, evaluation method, limitations, next actions, and conclusion strength.
   - If review returns FAIL, fix the reported issues as `reporter`, then repeat steps 4-6.
7. Execute:

```bash
.venv/bin/python src/ml_agents_trial/presentation/builder.py
```

8. Convert to HTML:

```bash
npx --yes @marp-team/marp-cli artifacts/presentation/slides.md --output artifacts/presentation/slides.html
```

9. Validate:

```bash
uv run ruff check src/ tests/
```

10. Commit only presentation Python files:

```bash
git add src/ml_agents_trial/presentation/
git commit -m "feat(presentation): generate slide builder"
```

11. Report `artifacts/presentation/slides.html` and commit hash.

## Codex Notes

- This command is invoked as `codex command: report`; it is not a slash command.
- Do not use Claude-specific named-agent calls, hooks, or settings files.
- Use `exec_command` for shell validation and commit only the files named in this command.
