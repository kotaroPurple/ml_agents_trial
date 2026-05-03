# codex command: build

Generate model training code and train all configured models.

## Arguments

`[TARGET_COLUMN]`

- Default TARGET_COLUMN: `MedHouseVal`

## Steps

1. Confirm `data/processed/features.csv` exists.
2. Read:
   - `.codex/agents/model-architect.md`
   - `.codex/skills/tabular-ml-quality/SKILL.md`
   - `.codex/skills/artifact-contracts/SKILL.md`
3. Act as `model-architect` and implement `src/ml_agents_trial/models/configs.py` and `src/ml_agents_trial/models/trainer.py`.
4. Act as `code-reviewer` by reading `.codex/agents/code-reviewer.md` and checking `src/ml_agents_trial/models/`.
5. Domain review:
   - Models match `artifacts/eda/data_summary.json` task type.
   - Metrics use `ml_agents_trial.core.metrics`.
   - Each model saves `model.pkl` and `metrics.json`.
6. Act as `ml-reviewer` by reading `.codex/agents/ml-reviewer.md` and checking model selection, baseline comparison, metrics, best-model rule, and artifact contracts.
7. Execute:

```bash
.venv/bin/python src/ml_agents_trial/models/trainer.py [TARGET_COLUMN]
```

8. Validate:

```bash
uv run ruff check src/ tests/
```

9. Commit only model files:

```bash
git add src/ml_agents_trial/models/
git commit -m "feat(models): generate model configs and trainer"
```

10. Report comparison table, best model, commit hash, and next command.
