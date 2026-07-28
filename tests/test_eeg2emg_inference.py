"""Tests for EEG→EMG inference helpers (no training)."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import torch

from src.eeg_emg.eeg2emg_inference import load_eeg2emg_model, prepare_eeg_emg_trials
from src.eeg_emg.eeg2emg_run import CNNLSTM_EEG2EMG


def test_prepare_eeg_emg_trials_from_npz(tmp_path: Path) -> None:
    """Minimal paired EEG/EMG .npz loads to trial format."""
    eeg = np.random.randn(100, 4).astype(np.float32)
    emg = np.random.randn(100, 2).astype(np.float32)
    path = tmp_path / "pair.npz"
    np.savez(path, eeg=eeg, emg=emg)

    e_trial, m_trial, pre_w = prepare_eeg_emg_trials(str(path))
    assert e_trial.ndim == 3
    assert m_trial.ndim == 3
    assert e_trial.shape[0] == m_trial.shape[0]
    assert pre_w is False


def test_load_bare_state_dict_roundtrip(tmp_path: Path) -> None:
    """Legacy-style checkpoint: only state_dict on disk infers channel widths."""
    model = CNNLSTM_EEG2EMG(
        4,
        2,
        cnn_channels=8,
        lstm_hidden=16,
        lstm_layers=1,
        bidirectional=False,
    )
    path = tmp_path / "bare.pth"
    torch.save(model.state_dict(), path)
    loaded, cfg = load_eeg2emg_model(str(path), map_location="cpu")
    assert cfg["n_eeg_channels"] == 4
    assert cfg["n_emg_channels"] == 2
    assert sum(p.numel() for p in loaded.parameters()) == sum(p.numel() for p in model.parameters())
