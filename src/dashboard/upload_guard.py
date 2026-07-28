"""Validate Streamlit sidebar uploads (size limits, expected extensions)."""

from __future__ import annotations

import os
from typing import Any


def _max_bytes_mb(env_var: str, default_mb: int) -> int:
    raw = os.environ.get(env_var, str(default_mb))
    try:
        mb = float(raw)
    except ValueError:
        mb = float(default_mb)
    return int(max(1, mb) * 1024 * 1024)


MAX_NPZ_UPLOAD_BYTES = _max_bytes_mb("UMBRA_MAX_NPZ_UPLOAD_MB", 200)
MAX_PTH_UPLOAD_BYTES = _max_bytes_mb("UMBRA_MAX_PTH_UPLOAD_MB", 50)


def upload_violation_message(
    uploaded: Any,
    *,
    max_bytes: int,
    allowed_suffix: str,
) -> str | None:
    """
    Return a user-facing error message if ``uploaded`` is invalid, else ``None``.

    ``uploaded`` is a Streamlit ``UploadedFile``; if ``None``, returns ``None``.
    """
    if uploaded is None:
        return None
    name = getattr(uploaded, "name", "") or ""
    if not name.lower().endswith(allowed_suffix):
        return f"Fichier refusé : extension attendue {allowed_suffix!r}, reçu {name!r}."
    size = int(getattr(uploaded, "size", 0) or 0)
    if size > max_bytes:
        return (
            f"Fichier trop volumineux ({size // (1024 * 1024)} Mo > "
            f"{max_bytes // (1024 * 1024)} Mo max). Voir `.env.example` "
            "(UMBRA_MAX_NPZ_UPLOAD_MB / UMBRA_MAX_PTH_UPLOAD_MB)."
        )
    return None


def validate_upload(
    uploaded: Any,
    *,
    max_bytes: int,
    allowed_suffix: str,
) -> bool:
    """
    Return True if ``uploaded`` is None or passes checks; otherwise show ``st.error`` and False.
    """
    msg = upload_violation_message(uploaded, max_bytes=max_bytes, allowed_suffix=allowed_suffix)
    if msg is None:
        return True
    import streamlit as st

    st.error(msg)
    return False
