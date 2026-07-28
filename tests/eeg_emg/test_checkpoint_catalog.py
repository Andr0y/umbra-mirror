"""Tests for checkpoint kind detection and default compare selection."""

from __future__ import annotations

from pathlib import Path

from src.eeg_emg.checkpoint_catalog import (
    default_compare_selection,
    detect_checkpoint_kind,
    list_checkpoint_basenames,
)

MODEL_DIR = Path("src/eeg_emg")


def test_detect_emg_checkpoints() -> None:
    for name in ("eeg2emg_best.pth", "eeg2emg_baseline.pth"):
        path = MODEL_DIR / name
        if not path.is_file():
            continue
        assert detect_checkpoint_kind(path) == "emg"


def test_list_emg_only_returns_emg_checkpoints() -> None:
    emg_names = list_checkpoint_basenames(MODEL_DIR, kind="emg")
    for name in emg_names:
        assert detect_checkpoint_kind(MODEL_DIR / name) == "emg"


def test_default_compare_selection_prefers_order() -> None:
    available = ["eeg2emg_best.pth", "eeg2emg_baseline.pth", "other.pth"]
    picked = default_compare_selection(
        available,
        ["eeg2emg_baseline.pth", "eeg2emg_best.pth"],
    )
    assert picked == ["eeg2emg_baseline.pth", "eeg2emg_best.pth"]
