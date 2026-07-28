"""List and classify EEG→EMG PyTorch checkpoints in a model directory."""

from __future__ import annotations

from pathlib import Path
from typing import Literal

import torch

CheckpointKind = Literal["emg", "unknown"]


def _peek_checkpoint(path: str | Path) -> dict:
    """Load checkpoint metadata without building a full model."""
    try:
        ckpt = torch.load(path, map_location="cpu", weights_only=False)
    except TypeError:
        ckpt = torch.load(path, map_location="cpu")
    return ckpt if isinstance(ckpt, dict) else {}


def detect_checkpoint_kind(path: str | Path) -> CheckpointKind:
    """
    Return whether a ``.pth`` file is an EEG→EMG regressor.

    Uses saved ``config`` keys and top-level checkpoint fields; falls back to the
    ``eeg2emg`` filename prefix.
    """
    name = Path(path).name.lower()
    if name.startswith("eeg2emg"):
        return "emg"

    meta = _peek_checkpoint(path)
    cfg = meta.get("config") or {}
    if isinstance(cfg, dict) and "n_emg_channels" in cfg:
        return "emg"
    if meta.get("best_val_mse") is not None:
        return "emg"
    return "unknown"


def list_checkpoint_basenames(
    model_dir: str | Path,
    *,
    kind: CheckpointKind | None = None,
) -> list[str]:
    """Sorted ``.pth`` basenames under ``model_dir``, optionally filtered by ``kind``."""
    root = Path(model_dir)
    if not root.is_dir():
        return []
    names = sorted(
        f.name for f in root.iterdir() if f.suffix == ".pth" and not f.name.startswith(".")
    )
    if kind is None:
        return names
    return [n for n in names if detect_checkpoint_kind(root / n) == kind]


def default_compare_selection(
    available: list[str],
    preferred: list[str],
    *,
    max_count: int = 2,
) -> list[str]:
    """
    Pick up to ``max_count`` models for side-by-side comparison.

    Prefer names from ``preferred`` that exist in ``available``; if fewer than
    ``max_count``, fill from remaining ``available`` in sorted order.
    """
    picked: list[str] = []
    for name in preferred:
        if name in available and name not in picked:
            picked.append(name)
        if len(picked) >= max_count:
            return picked
    for name in available:
        if name not in picked:
            picked.append(name)
        if len(picked) >= max_count:
            break
    return picked
