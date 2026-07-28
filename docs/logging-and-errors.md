# Journalisation et gestion d’erreurs

## État actuel

- **Scripts et ML** : messages via `print`, barres `tqdm`, exceptions non interceptées remontent à l’utilisateur (CLI) ou à Streamlit (trace dans l’UI).
- **Streamlit** : `st.error`, `st.warning`, `try/except` autour des appels coûteux (inférence, sauvegarde de rapports).

## Orientation (industrialisation progressive)

Pour une traçabilité renforcée sans changer tout le code d’un coup :

1. Introduire `logging.getLogger(__name__)` dans les modules **non-UI** (`src/eeg_emg/`) avec niveau configurable via `UMBRA_LOG_LEVEL` (à ajouter quand besoin).
2. Garder Streamlit pour l’**affichage utilisateur** ; dupliquer les erreurs critiques vers le logger en `ERROR`.
3. En CI, conserver la sortie pytest comme source de vérité pour les régressions.

Aucune obligation d’outil externe (ELK, etc.) pour les besoins actuels du dépôt.
