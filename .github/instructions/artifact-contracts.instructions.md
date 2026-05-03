---
applyTo: "src/ml_agents_trial/{models,evaluation,presentation}/**/*.py"
---

# Artifact Contracts

Use the detailed Copilot Agent Skill at `.github/skills/artifact-contracts/SKILL.md` when generated code reads or writes ML artifacts.

Always preserve these short rules:

- Read and write JSON through `ml_agents_trial.core.io.load_json()` and `save_json()`.
- Preserve existing key meanings.
- Keep `comparison.json` sufficient to select the best model.
- Keep reporting artifacts sufficient to surface assumptions, limitations, and next steps.
