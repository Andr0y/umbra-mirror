# Sécurité et exploitation

## Menaces principales (dashboard Streamlit)

| Risque | Contexte | Mitigation |
|--------|----------|------------|
| **Absence d’authentification** | `streamlit run` est prévu pour un usage **local** ou réseau **restreint** | Ne pas exposer le port 8501 sur Internet sans reverse-proxy + auth ; préférer VPN ou SSH tunnel. |
| **Upload de fichiers** | Pages EEG–EMG acceptent `.npz` / `.pth` en override | Limites de taille (`UMBRA_MAX_NPZ_UPLOAD_MB`, `UMBRA_MAX_PTH_UPLOAD_MB`) et extension contrôlées dans `src/dashboard/upload_guard.py`. |
| **Path traversal** | Noms de fichiers utilisateur | Les uploads sont écrits sous `data/eeg_emg/_uploads/` ou `src/eeg_emg/_uploads/` avec le nom fourni par le client — **n’exécuter pas** le dashboard en multi-tenant hostile sans durcissement supplémentaire. |
| **Données sensibles** | Signaux biométriques | Traiter les jeux comme **données personnelles potentielles** ; restreindre l’accès au dossier `data/`. |

## Sauvegardes (recommandations)

- **Modèles** : copier `src/eeg_emg/*.pth` vers un stockage versionné (DVC, git-lfs, ou artefact CI).
- **Données** : ne pas versionner les gros jeux dans Git ; documenter leur provenance et une procédure de restauration.
- **Rapports JSON** : `data/*_reports/` peut être archivé pour audit ou comparaisons longitudinales.

## Dépendances

- Audit automatique : `make audit` ou job `security` dans `.github/workflows/ci.yml`.
- Les alertes connues peuvent être suivies avec garde-fous documentés dans le workflow (ignore list temporaire — à revoir régulièrement).
