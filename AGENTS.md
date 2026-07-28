# AGENTS.md

> Cross-tool agent configuration for this project.

## Project Overview

**Umbra** — EEG→EMG prediction (PyTorch, `.npz` datasets, Streamlit dashboard). CI: Ruff, mypy, pytest, SonarCloud.

**Stack**: python | test: pytest | lint: ruff

## Commands

```bash
docker build -t umbra:latest .
pytest
ruff check .
streamlit run src/dashboard/app.py
```

## Repository Layout

```
data/
Dockerfile
docs/
environment.yml
Makefile
pyproject.toml
README.md
requirements-dev.txt
requirements.txt
src/
tests/
```

## Coding Standards

- Follow existing conventions in the codebase.
- Run the linter after every edit.
- Write tests for new logic.
- Prefer editing existing files over creating new ones.

## Commit Convention

Conventional Commits: `type(scope): message`

Types: `feat` · `fix` · `refactor` · `test` · `docs` · `chore`

## Agent Behavior Rules

1. Read before write.
2. Minimal diff.
3. No placeholder content.
4. Verify with lint and tests.

## Security

- Never commit secrets, API keys, or credentials.
- Validate all user input.
