# Cas d’usage techniques

Acteurs : **chercheur / développeur**, **opérateur dashboard**, **CI**.

| ID | Acteur | Scénario | Déclencheur | Résultat attendu |
|----|--------|----------|-------------|------------------|
| UC-T1 | Développeur | Entraîner ou fine-tuner EEG→EMG | Scripts sous `src/eeg_emg/` | Checkpoint `.pth` |
| UC-T2 | Opérateur | Inférence + métriques EEG→EMG | Page *Decoder* | Métriques globales et par canal, courbes |
| UC-T3 | Opérateur | Contrôle qualité jeu `.npz` | Page *Dataset quality* | Rapport + JSON sous `data/eeg_emg_quality_reports/` |
| UC-T4 | Opérateur | Comparer plusieurs checkpoints | Page *Model comparator* | Tableau / graphiques + JSON sous `data/eeg_emg_comparison_reports/` |
| UC-T5 | Opérateur | Mesurer latence / débit | Page *Hardware impact* | Rapport JSON sous `data/eeg_emg_hardware_reports/` |
| UC-T6 | CI | Gate qualité sur chaque PR | Push / PR vers branches configurées | Ruff, mypy, pytest, pip-audit ; SonarCloud en suivi |

Les parcours **métier** (patient, exosquelette) restent dans le README ; ce document se limite au **système logiciel**.
