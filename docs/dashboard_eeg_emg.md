# Dashboard EEG→EMG

Reference for **Streamlit navigation** and page modules.

## Navigation

Single section with four pages (see `src/dashboard/app.py`):

| Page | URL path | Module |
|------|----------|--------|
| Decoder | `eeg-emg-decoder` | `eeg_emg/eeg2emg_dashboard.py` |
| Dataset quality | `eeg-emg-dataset-quality` | `eeg_emg/dataset_quality_page.py` |
| Model comparator | `eeg-emg-model-comparator` | `eeg_emg/model_comparator_page.py` |
| Hardware impact | `eeg-emg-hardware-impact` | `eeg_emg/hardware_impact_page.py` |

## Shared backends

| Module | Role |
|--------|------|
| `eeg_emg_dataset_quality.py` | NPZ validation, report JSON |
| `eeg_emg_model_compare.py` | Multi-checkpoint regression compare |
| `eeg_emg_torch_hardware.py` | PyTorch latency / throughput profiling |
| `upload_guard.py` | Upload size and extension checks |

## Data & reports

- **Inputs:** `data/eeg_emg/*.npz`, `src/eeg_emg/*.pth` (see [`../data/README.md`](../data/README.md))
- **Outputs:** JSON under `data/eeg_emg_quality_reports/`, `data/eeg_emg_comparison_reports/`, `data/eeg_emg_hardware_reports/`
