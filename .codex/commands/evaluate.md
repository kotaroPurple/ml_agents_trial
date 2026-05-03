# codex command: evaluate

Generate model evaluation modules and plots.

## Arguments

`[TARGET_COLUMN]`

- Default TARGET_COLUMN: `MedHouseVal`

## Steps

1. Confirm `artifacts/models/comparison.json` exists.
2. Read:
   - `.codex/agents/evaluator.md`
   - `.codex/skills/tabular-ml-quality/SKILL.md`
   - `.codex/skills/artifact-contracts/SKILL.md`
3. Act as `evaluator` and implement `src/ml_agents_trial/evaluation/plots.py` and `src/ml_agents_trial/evaluation/report.py`.
4. Act as `code-reviewer` by reading `.codex/agents/code-reviewer.md` and checking `src/ml_agents_trial/evaluation/`.
5. Domain review:
   - Plot modules set `matplotlib.use("Agg")`.
   - Plot functions accept `Path` output paths.
   - `generate_report()` records evaluation method, limitations, and next steps when possible.
6. Act as `ml-reviewer` by reading `.codex/agents/ml-reviewer.md` and checking evaluation design, overfitting checks, best-model rule, `report_summary.json`, and plot relevance.
7. Execute:

```bash
.venv/bin/python src/ml_agents_trial/evaluation/report.py [TARGET_COLUMN]
```

8. Confirm generated plots:

```bash
find artifacts/models -name "*.png" | sort
```

9. Validate:

```bash
uv run ruff check src/ tests/
```

10. Commit only evaluation files:

```bash
git add src/ml_agents_trial/evaluation/
git commit -m "feat(evaluation): generate evaluation modules"
```

11. Report generated plots, commit hash, and next command.
