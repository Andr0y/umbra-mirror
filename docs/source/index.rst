##################################################
Umbra – Neuromuscular Interface Documentation
##################################################

Welcome to the **Umbra** project documentation! Umbra is an AI system that learns to become a **motor copy of an individual**, functioning in tandem with them. Using non-invasive signals like **EMG** (electromyograms) and **EEG** (electroencephalograms), Umbra can control supplementary limbs, replacement limbs, or assist with exoskeleton control.

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   setup
   usage
   architecture

.. toctree::
   :maxdepth: 2
   :caption: Guides

   guides/preprocessing
   guides/model_training
   guides/dashboard

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/emg_movement
   api/eeg_emg
   api/dashboard

.. toctree::
   :maxdepth: 2
   :caption: Project Info

   beta_test_plan


Project Overview
================

Umbra implements two main neural pathways:

1. **EEG → EMG Model** (In Development)
   
   Translates brain signals (EEG) to muscle signals (EMG) to capture motor intent.

2. **EMG → Movement Model** (Implemented)
   
   Converts muscle signals (EMG) to hand gestures using CNN-LSTM deep learning.

Key Features
============

- **EMG Signal Processing**: Windowing, filtering, and preprocessing of raw EMG data
- **CNN-LSTM Architecture**: State-of-the-art gesture recognition model
- **NinaPro Dataset**: Support for the NinaPro hand gesture dataset
- **Streamlit Dashboard**: Real-time visualization and inference interface
- **Dataset Quality Checker**: Validation and integrity checking for preprocessed datasets
- **Model Comparator**: Performance analysis and model iteration tracking
- **Hardware Profiler**: Computational resource monitoring and optimization tracking

Tech Stack
==========

- **ML/DL**: TensorFlow/Keras, Scikit-learn, PyTorch
- **Data**: NumPy, Pandas, SciPy
- **Experiment Tracking**: MLflow, DVC, Prefect
- **Dashboard**: Streamlit, Matplotlib, Seaborn
- **Language**: Python 3.11+

Indices and Tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

