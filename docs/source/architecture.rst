##############
Architecture
##############

Project Structure
=================

The Umbra project is organized as follows:

.. code-block:: text

   umbra/
   ├── src/                          # Main source code
   │   ├── __init__.py
   │   ├── config.py                 # Global configuration
   │   ├── main.py                   # Entry point for preprocessing
   │   ├── emg_movement/             # EMG → Movement module
   │   │   ├── __init__.py
   │   │   ├── model.py              # CNN-LSTM model architecture
   │   │   ├── preprocessing.py      # EMG preprocessing pipeline
   │   │   ├── train.py              # Training script
   │   │   ├── utils.py              # Utility functions
   │   │   └── gestures.py           # Gesture definitions (NinaPro)
   │   ├── eeg_emg/                  # EEG → EMG module (WIP)
   │   │   ├── __init__.py
   │   │   ├── eeg2emg_run.py
   │   │   ├── convert_eeg_emg_to_npz.py
   │   │   ├── data_augmentation.py
   │   │   ├── check_results.py
   │   │   └── eeg2emg_best.pth      # Pre-trained PyTorch model
   │   ├── dashboard/                # Streamlit dashboard
   │   │   ├── __init__.py
   │   │   ├── app.py                # Main dashboard app
   │   │   ├── dataset_quality.py    # Dataset quality checker
   │   │   ├── hardware_profiler.py  # Hardware impact tracker
   │   │   ├── model_comparator.py   # Model comparison tool
   │   │   └── pages/                # Multi-page Streamlit apps
   │   │       ├── 1_Dataset_Quality_Check.py
   │   │       ├── 2_Model_Comparator.py
   │   │       └── 3_Hardware_Impact_Tracker.py
   │   └── models/                   # Trained Keras models
   │       ├── cnn_lstm_1.keras
   │       ├── cnn_lstm_emg_v2.keras
   │       └── cnn_lstm_emg_v3.keras
   ├── data/                         # Data directory
   │   ├── ninapro/                  # Raw NinaPro dataset (not in repo)
   │   ├── preprocessed/             # Preprocessed datasets
   │   ├── quality_reports/          # Quality check results
   │   ├── comparison_reports/       # Model comparison outputs
   │   ├── hardware_reports/         # Hardware profiling results
   │   └── ninapro.dvc               # DVC data tracking
   ├── docs/                         # Documentation (Sphinx)
   │   ├── source/                   # Sphinx source files
   │   │   ├── conf.py               # Sphinx configuration
   │   │   ├── index.rst             # Main documentation index
   │   │   ├── setup.rst             # Setup guide
   │   │   ├── usage.rst             # Usage guide
   │   │   ├── api/                  # API reference
   │   │   └── guides/               # Detailed guides
   │   └── build/                    # Built HTML documentation
   ├── tests/                        # Test suite
   │   ├── conftest.py               # Pytest configuration
   │   ├── test_model.py             # Model tests
   │   ├── test_env.py               # Environment tests
   │   └── test_emg_train_import.py  # Training script tests
   ├── scripts/                      # Utility scripts
   │   ├── setup.sh                  # Setup script
   │   ├── run_comparison.py         # Batch comparison runner
   │   └── regression_check.py       # Regression testing
   ├── pyproject.toml                # Project metadata & dependencies
   ├── requirements.txt              # Core dependencies
   ├── requirements-dev.txt          # Development dependencies
   ├── environment.yml               # Conda environment
   ├── Dockerfile                    # Docker image definition
   ├── Makefile                      # Build/deployment tasks
   └── README.md                     # Main README

Core Modules
============

src/config.py
~~~~~~~~~~~~~

Centralized configuration for paths and hyperparameters:

- **Sampling frequency** (FS = 1000 Hz)
- **Filter settings** (lowpass cutoff, filter order)
- **Path constants** (NinaPro root, preprocessed path, model directory)
- **Preprocessing parameters** (window size, step size, labels)

All constants can be imported and used throughout the project.

src/emg_movement/ – EMG to Movement
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The main EMG gesture recognition module:

**preprocessing.py**

- Loads raw NinaPro EMG data
- Applies bandpass filtering (lowpass at 5 Hz)
- Creates sliding windows (500 ms with 50% overlap)
- Normalizes and standardizes features
- Saves output as NumPy arrays (X.npy, y.npy)

**model.py**

- Defines CNN-LSTM architecture:
  
  - Convolutional layers for feature extraction
  - LSTM layers for temporal modeling
  - Dense layers for classification

- Supports model saving/loading in Keras format (.keras)

**train.py**

- Loads preprocessed data
- Splits into train/validation/test sets
- Trains model with callbacks:
  
  - Early stopping
  - Model checkpointing
  - Validation monitoring

- Evaluates on test set and logs metrics (accuracy, F1-score)

**utils.py**

- Helper functions for data loading, normalization
- Metrics computation
- Visualization utilities

**gestures.py**

- NinaPro gesture definitions
- Gesture name mappings
- Label encoding/decoding

src/eeg_emg/ – EEG to EMG (In Development)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Placeholder module for the EEG → EMG translation model:

- ``eeg2emg_run.py``: Main training/inference script
- ``eeg2emg_best.pth``: Pre-trained PyTorch model
- ``convert_eeg_emg_to_npz.py``: Data conversion utilities
- ``data_augmentation.py``: EEG data augmentation pipeline
- ``check_results.py``: Result validation

This module is currently under development and not fully integrated.

src/dashboard/ – Streamlit Interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Multi-page Streamlit application for visualization and analysis:

**app.py**

- Main entry point
- Initializes session state
- Provides central UI for model inference
- Integrates with sidebar pages

**dataset_quality.py**

- Validates preprocessed datasets
- Checks data distribution
- Detects anomalies
- Generates quality reports

**hardware_profiler.py**

- Monitors CPU/GPU/RAM usage
- Profiles inference latency
- Identifies bottlenecks
- Tracks model efficiency

**model_comparator.py**

- Compares multiple models
- Evaluates on same dataset
- Visualizes performance metrics
- Exports comparison reports

**pages/**

- Streamlit multi-page structure
- Each page (1_Dataset_Quality_Check.py, etc.) runs independently
- Accessible via sidebar navigation

Data Pipeline
=============

The Umbra data pipeline follows this flow:

.. code-block:: text

   Raw NinaPro Data
   ↓
   [preprocessing.py] → Filtering, Windowing, Normalization
   ↓
   Preprocessed Data (X.npy, y.npy)
   ↓
   [train.py] → CNN-LSTM Training
   ↓
   Trained Model (.keras file)
   ↓
   [dashboard] → Inference & Visualization
   ↓
   Predictions & Analysis

Key Algorithms
==============

CNN-LSTM Architecture
~~~~~~~~~~~~~~~~~~~~~

The CNN-LSTM model combines:

1. **Convolutional Layers** (feature extraction)
   
   - Extract local EMG patterns
   - Reduce dimensionality

2. **LSTM Layers** (temporal modeling)
   
   - Capture temporal dependencies in EMG signals
   - Learn long-range gesture dynamics

3. **Dense Layers** (classification)
   
   - Final classification layer with softmax
   - Output: probability distribution over gestures

EMG Signal Processing
~~~~~~~~~~~~~~~~~~~~~

Preprocessing steps:

1. **Bandpass Filtering**: Remove DC offset and high-frequency noise
2. **Windowing**: Create overlapping 500 ms windows with 50% overlap
3. **Feature Extraction**: Compute statistical features per window
4. **Normalization**: Standardize to zero mean, unit variance
5. **Train/Test Split**: Stratified split by gesture class

Experiment Tracking
===================

The project uses **MLflow** for experiment tracking:

.. code-block:: bash

   mlflow ui  # Launch MLflow tracking server

Models, metrics, and parameters are logged for reproducibility and comparison.

Dependencies
============

See [src/config.py](../src/config.py) and [requirements.txt](../requirements.txt) for the full dependency list.

**Key Libraries**

- **TensorFlow/Keras**: Deep learning framework
- **NumPy/Pandas**: Data processing
- **Scikit-learn**: ML utilities and preprocessing
- **Streamlit**: Dashboard framework
- **Matplotlib/Seaborn**: Visualization
- **MLflow**: Experiment tracking
- **DVC**: Data versioning and pipeline management

Development
===========

Testing
~~~~~~~

Run tests with pytest:

.. code-block:: bash

   pytest tests/

Code Quality
~~~~~~~~~~~~

The project uses Ruff for linting and formatting:

.. code-block:: bash

   ruff check src/
   ruff format src/

Configuration is in [pyproject.toml](../pyproject.toml).

Next Steps
==========

- Read :doc:`guides/preprocessing` for preprocessing details
- See :doc:`guides/model_training` for training best practices
- Check the :doc:`api/emg_movement` for detailed API documentation
