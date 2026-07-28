# src/config.py — EEG→EMG paths and dashboard defaults

EEG_EMG_DATA_DIR = "data/eeg_emg"
EEG_EMG_MODEL_DIR = "src/eeg_emg"

# Canonical files auto-selected by dashboard pages when present
EEG_EMG_DEFAULT_NPZ = "data/eeg_emg/dataset_augmented.npz"
EEG_EMG_DEFAULT_PTH = "src/eeg_emg/eeg2emg_best.pth"
EEG_EMG_SUBJECT_MODEL_PTH = "src/eeg_emg/eeg2emg_single_subject_best.pth"

EEG_EMG_QUALITY_REPORTS_DIR = "data/eeg_emg_quality_reports"
EEG_EMG_COMPARISON_REPORTS_DIR = "data/eeg_emg_comparison_reports"
EEG_EMG_HARDWARE_REPORTS_DIR = "data/eeg_emg_hardware_reports"
