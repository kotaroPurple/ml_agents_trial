# codex command: setup

Set up the project environment and demo data.

## Defaults

No arguments.

## Steps

1. Create the virtual environment:

```bash
uv venv --python 3.12
```

2. Install dependencies:

```bash
uv pip install -e ".[dev]"
```

3. Verify imports:

```bash
.venv/bin/python -c "import pandas, sklearn, lightgbm; print('OK')"
```

4. Download the California Housing CSV:

```bash
.venv/bin/python -c "from ml_agents_trial.data.datasets.house_prices import download; download()"
```

5. Verify core IO:

```bash
.venv/bin/python -c "from ml_agents_trial.core.config import DATA_RAW; from ml_agents_trial.core.io import load_csv; df = load_csv(DATA_RAW / 'house_prices.csv'); print(f'dataset: {df.shape}')"
```

6. Commit setup files only if this is an initial scaffold workflow and the user expects a commit. Otherwise report versions and dataset shape.

## Codex Notes

- This command is invoked as `codex command: setup`; it is not a slash command.
- Do not use Claude-specific hooks or settings files.
- Use `exec_command` for shell validation.
