# Logique métier et signaux

Centralise les règles **métier / signal** et pointe vers le code qui les implémente.

## EEG → EMG

| Concept | Détail | Implémentation |
|---------|--------|----------------|
| Paires EEG / EMG | Fichiers `.npz` avec clés normalisées (`eeg`/`emg`, cas variants) | `load_npz_anycase` dans `src/eeg_emg/eeg2emg_run.py` |
| Forme essais | `(N, C, T)` après chargement | `prepare_eeg_emg_trials` dans `src/eeg_emg/eeg2emg_inference.py` |
| Fenêtrage en ligne | `window_size`, `step`, normalisation Z-score optionnelle | `EEGEMGWindowDataset`, `run_inference` |
| Split validation | Fraction + graine pour reproductibilité | `run_inference`, pages dashboard |
| Métriques | MSE, RMSE, MAE, R² global, Pearson / R² / MAE / envelope par canal EMG | `src/eeg_emg/eeg2emg_metrics.py`, `compute_metrics` |

## Lecture pédagogique

Les légendes des pages Streamlit décrivent fenêtrage et métriques ; pour la structure des pages, voir `docs/dashboard_eeg_emg.md`.
