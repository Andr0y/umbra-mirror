"""Streamlit entry point for the EEG→EMG dashboard."""

from pathlib import Path

import streamlit as st

_dashboard = Path(__file__).resolve().parent

pages = [
    st.Page(
        str(_dashboard / "eeg_emg" / "eeg2emg_dashboard.py"),
        title="Decoder",
        url_path="eeg-emg-decoder",
    ),
    st.Page(
        str(_dashboard / "eeg_emg" / "dataset_quality_page.py"),
        title="Dataset quality",
        url_path="eeg-emg-dataset-quality",
    ),
    st.Page(
        str(_dashboard / "eeg_emg" / "model_comparator_page.py"),
        title="Model comparator",
        url_path="eeg-emg-model-comparator",
    ),
    st.Page(
        str(_dashboard / "eeg_emg" / "hardware_impact_page.py"),
        title="Hardware impact",
        url_path="eeg-emg-hardware-impact",
    ),
]

pg = st.navigation(pages)
pg.run()
