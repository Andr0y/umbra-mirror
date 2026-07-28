# Changelog

Format inspired by [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

- _(nothing yet)_

## [0.4.0] — 2026-07-28

### Changed

- **Scope:** repository focused on **EEG→EMG** only (PyTorch + Streamlit). Removed Kestal/Forge tooling, NinaPro EMG hand-movement pipeline, Unity/gesture POC, and OpenSim scripts.
- Documentation, README, and CI aligned with the single-pipeline layout.
- Runtime dependencies trimmed (TensorFlow, MLflow, DVC, Prefect removed).

### Added

- `data/README.md`, `LICENSE` (MIT), `docs/dashboard_eeg_emg.md`, `make train-eeg2emg`.

### Removed

- `src/emg_movement/`, EMG dashboard section, NinaPro DVC tracking, Keras model CI workflows.

## [0.3.0] — indicative (EEG–EMG dashboard, March–April 2026)

### Added

- EEG–EMG dashboard pages: dataset quality, model comparator, hardware profiling.
- EEG→EMG decoder and shared inference metrics.

### Fixed

- Dashboard crashes and URL path errors; checkpoint config saved in `.pth` files.

## [0.2.0] — indicative (Streamlit dashboard, February–March 2026)

### Added

- Initial Streamlit dashboard and EMG tooling (since removed in favour of EEG→EMG focus).

## [0.1.0] — indicative (CI & quality, late 2025)

### Added

- CI workflows (Ruff, mypy, pytest, pip-audit, SonarCloud, Docker).
- Pre-commit hooks.
