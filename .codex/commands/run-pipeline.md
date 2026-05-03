# codex command: run-pipeline

Run the whole ML pipeline from EDA to Marp slides.

## Arguments

`[CSV_PATH] [TARGET_COLUMN]`

- Default CSV_PATH: `data/raw/house_prices.csv`
- Default TARGET_COLUMN: `MedHouseVal`

## Steps

1. Confirm `[CSV_PATH]` exists. If missing, run or request `codex command: setup`.
2. Run `codex command: analyze [CSV_PATH] [TARGET_COLUMN]`.
3. Run `codex command: engineer [TARGET_COLUMN]`.
4. Run `codex command: build [TARGET_COLUMN]`.
5. Run `codex command: evaluate [TARGET_COLUMN]`.
6. Run `codex command: report`.

Stop immediately if any command fails, if `code-reviewer` fails, or if `ml-reviewer` fails.

## Completion Report

Run:

```bash
git log --oneline -6
```

Report:

- Best model and primary metric.
- Generated slides: `artifacts/presentation/slides.html`.
- Any residual validation risks.
