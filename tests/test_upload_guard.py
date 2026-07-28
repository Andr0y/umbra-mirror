"""Tests for Streamlit upload validation helpers (no Streamlit runtime)."""

from __future__ import annotations

from types import SimpleNamespace

from src.dashboard.upload_guard import (
    MAX_NPZ_UPLOAD_BYTES,
    upload_violation_message,
)


def test_upload_violation_none() -> None:
    assert upload_violation_message(None, max_bytes=100, allowed_suffix=".npz") is None


def test_upload_violation_bad_suffix() -> None:
    up = SimpleNamespace(name="x.txt", size=10)
    msg = upload_violation_message(up, max_bytes=MAX_NPZ_UPLOAD_BYTES, allowed_suffix=".npz")
    assert msg is not None
    assert ".npz" in msg


def test_upload_violation_too_large() -> None:
    up = SimpleNamespace(name="a.npz", size=MAX_NPZ_UPLOAD_BYTES + 1)
    msg = upload_violation_message(up, max_bytes=MAX_NPZ_UPLOAD_BYTES, allowed_suffix=".npz")
    assert msg is not None
    assert "volumineux" in msg.lower() or "Mo" in msg
