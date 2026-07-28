# Umbra – EIP

[![CI](https://github.com/Andr0y/umbra-mirror/actions/workflows/ci.yml/badge.svg)](https://github.com/Andr0y/umbra-mirror/actions/workflows/ci.yml)

## Objectif du projet

Développer une IA visant une **copie motrice** de l’individu à partir de signaux **non invasifs** (**EEG**, **EMG**) : prédire l’activité EMG à partir de l’EEG pour des usages recherche, rééducation ou interfaces homme-machine.

Ce dépôt fournit un pipeline **EEG → EMG** (jeux appariés `.npz`, modèle CNN–LSTM **PyTorch**, inférence et dashboard Streamlit).

---

## Prérequis

| Élément | Détail |
|---------|--------|
| Python | **3.11+** |
| GPU | Optionnel (entraînement PyTorch ; inférence CPU possible) |
| Données | Fichiers `.npz` et checkpoints `.pth` en local — voir [`data/README.md`](data/README.md) |

---

## Installation

```bash
git clone https://github.com/Andr0y/umbra-mirror.git
cd umbra-mirror
make install
```

Puis placer vos données et modèles (non versionnés) :

- `data/eeg_emg/*.npz`
- `src/eeg_emg/*.pth`

---

## Démarrage rapide

### 1. Entraîner (optionnel)

```bash
make train-eeg2emg
```

### 2. Lancer le dashboard

```bash
streamlit run src/dashboard/app.py
```

Ouvrir **http://localhost:8501** — pages : Decoder, Dataset quality, Model comparator, Hardware impact.

---

## Commandes Makefile

| Cible | Description |
|-------|-------------|
| `make install` | Dépendances + pre-commit |
| `make lint` / `make format` | Ruff |
| `make type-check` | Mypy |
| `make test` | Pytest + couverture |
| `make train-eeg2emg` | Entraînement EEG→EMG (exemple) |
| `make docker-build` / `make docker-run` | Conteneur Streamlit |

---

## Structure

| Chemin | Rôle |
|--------|------|
| `src/eeg_emg/` | Entraînement, inférence, métriques PyTorch |
| `src/dashboard/` | Streamlit (`app.py`, pages `eeg_emg/`) |
| `src/config.py` | Chemins par défaut |
| `data/` | Données et rapports JSON ([`data/README.md`](data/README.md)) |
| `docs/` | Architecture, sécurité ([`docs/README.md`](docs/README.md)) |
| `tests/` | Pytest |

---

## Variables d’environnement

| Variable | Défaut | Rôle |
|----------|--------|------|
| `UMBRA_MAX_NPZ_UPLOAD_MB` | `200` | Taille max upload `.npz` |
| `UMBRA_MAX_PTH_UPLOAD_MB` | `50` | Taille max upload `.pth` |

---

## Documentation

- [Architecture](docs/architecture.md)
- [Dashboard pages](docs/dashboard_eeg_emg.md)
- [Changelog](CHANGELOG.md)

Qualité locale : `make lint`, `make type-check`, `make test`.

---

## Licence

[MIT](LICENSE) — projet Umbra EIP.
