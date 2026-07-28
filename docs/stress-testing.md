# Tests de charge et stress (orientation)

Le dashboard Streamlit n’est **pas** un serveur API classique : le stress test pertinent est **l’inférence répétée** et la **latence** par batch.

## Déjà prévu dans le repo

- Page **EEG–EMG Hardware impact** : mesure latences pour plusieurs tailles de batch (`src/dashboard/eeg_emg_torch_hardware.py` via `run_torch_profile`).

## Exemple manuel — boucle d’inférence CPU

À la racine du dépôt, avec un `.npz` et un `.pth` valides :

```bash
python -c "
from time import perf_counter
from src.eeg_emg.eeg2emg_inference import run_inference
t0 = perf_counter()
r = run_inference('data/eeg_emg/dataset_augmented.npz', 'src/eeg_emg/eeg2emg_best.pth', no_cuda=True, batch_size=32)
print('seconds', round(perf_counter()-t0, 3), 'mse', r.mse)
"
```

Adapter les chemins si vos fichiers par défaut diffèrent.

## Pistes d’extension

- Marqueur pytest `@pytest.mark.slow` pour des tests d’inférence longs, exclus par défaut (`pytest -m "not slow"`).
- Script dédié sous `scripts/` si vous devez produire un graphique latence / débit pour un rapport.
