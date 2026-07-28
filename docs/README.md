# Documentation Umbra — index

Bienvenue : ordre de lecture suggéré pour une **prise en main développeur**.

1. [`../README.md`](../README.md) — objectif, installation, commandes.
2. [`architecture.md`](architecture.md) — composants, flux, déploiement, versioning.
3. [`domain-logic.md`](domain-logic.md) — fenêtres, labels, métriques EEG→EMG.
4. [`use-cases-technical.md`](use-cases-technical.md) — scénarios outillés.
5. [`security-and-operations.md`](security-and-operations.md) — exposition Streamlit, uploads, sauvegardes.

Conventions et checks : [`../AGENTS.md`](../AGENTS.md), cibles `make` à la racine, [`quality-reports.md`](quality-reports.md).

## Référence par thème

| Thème | Fichier |
|-------|---------|
| Couverture, Sonar, lint | [`quality-reports.md`](quality-reports.md) |
| Logs et erreurs (stratégie) | [`logging-and-errors.md`](logging-and-errors.md) |
| Stress / perf inférence | [`stress-testing.md`](stress-testing.md) |
| Layout pages dashboard | [`dashboard_eeg_emg.md`](dashboard_eeg_emg.md) |

## Artefacts de livrable (captures, exports)

Placer captures d’écran ou exports PDF **non versionnés** sous un dossier `artifacts/` local (non suivi par Git).

## Wiki externe

Pas de wiki Notion obligatoire : ce dépôt sert de **wiki technique** via Markdown. Un espace Notion externe peut pointer vers ce dossier `docs/`.
