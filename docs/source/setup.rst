##############
Setup Guide
##############

Installation
============

Prerequisites
~~~~~~~~~~~~~

- **Python 3.11+** (or Python 3.14+)
- **Git**
- **Virtual environment** (venv, conda, or pipenv)

Installation from Source
~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Clone the repository**:

   .. code-block:: bash

      git clone https://github.com/Umbra-EIP/umbra-mirror.git
      cd umbra

2. **Create a virtual environment** (recommended):

   Using venv:

   .. code-block:: bash

      python3 -m venv venv
      source venv/bin/activate  # On Windows: venv\Scripts\activate

   Or using Conda:

   .. code-block:: bash

      conda env create --file environment.yml --name umbra-env
      conda activate umbra-env

3. **Install dependencies**:

   .. code-block:: bash

      pip install -r requirements.txt

   For development (includes test and documentation tools):

   .. code-block:: bash

      pip install -r requirements-dev.txt

4. **Verify installation**:

   .. code-block:: bash

      python -c "import tensorflow; print(f'TensorFlow version: {tensorflow.__version__}')"
      python -c "import streamlit; print('Streamlit installed successfully')"

Environment Configuration
==========================

Configuration Constants
~~~~~~~~~~~~~~~~~~~~~~~

All configuration is centralized in [src/config.py](../src/config.py):

.. code-block:: python

   FS = 1000                           # Sampling frequency (Hz)
   LOWPASS_CUTOFF = 5                  # Lowpass filter cutoff (Hz)
   FILTER_ORDER = 2                    # Filter order

   NINAPRO_ROOT = "data/ninapro"       # Raw NinaPro data location
   PREPROCESS_PATH = "data/preprocessed"  # Preprocessed data output
   MODEL_DIR = "src/models"            # Trained model directory

   WINDOW_MS = 500                     # EMG window size (ms)
   WINDOW_SAMPLES = 500                # EMG window size (samples)
   WINDOW_STEP_MS = 100                # EMG window step (ms)

   REST_LABEL = 0                      # Label for rest/no gesture

Data Directories
~~~~~~~~~~~~~~~~

Ensure the following directory structure exists:

.. code-block:: text

   umbra/
   ├── data/
   │   ├── ninapro/              # Raw NinaPro dataset (download separately)
   │   ├── preprocessed/         # Auto-created by preprocessing
   │   ├── quality_reports/      # Auto-created by quality checker
   │   ├── comparison_reports/   # Auto-created by model comparator
   │   └── hardware_reports/     # Auto-created by hardware profiler
   ├── src/
   │   ├── models/              # Trained .keras models
   │   ├── emg_movement/        # EMG→Movement model code
   │   ├── eeg_emg/             # EEG→EMG model code (WIP)
   │   └── dashboard/           # Streamlit apps
   └── logs/                    # (Optional) Experiment logs

Acquiring NinaPro Data
~~~~~~~~~~~~~~~~~~~~~~

The Umbra project uses the **NinaPro dataset** for hand gesture recognition. Download it from:

- `NinaPro Database <http://ninaweb.hevs.ch/>`_

Place the downloaded data in ``data/ninapro/`` with the expected structure (typically ``DB1/``, ``DB2/``, etc.).

System Requirements
===================

Minimum
~~~~~~~

- **CPU**: Intel i5 or equivalent (quad-core)
- **RAM**: 8 GB
- **Storage**: 20 GB (for NinaPro dataset + models)

Recommended
~~~~~~~~~~~

- **CPU**: Intel i7 or better / Apple Silicon M1+
- **RAM**: 16+ GB
- **GPU**: NVIDIA (CUDA 11.8+) or Apple Silicon
- **Storage**: 50+ GB

Troubleshooting
===============

TensorFlow Import Errors
~~~~~~~~~~~~~~~~~~~~~~~~

If you see ``ModuleNotFoundError: No module named 'tensorflow'``, ensure you've activated your virtual environment and run:

.. code-block:: bash

   pip install --upgrade tensorflow

Python Version Mismatch
~~~~~~~~~~~~~~~~~~~~~~~

If you see version conflicts, ensure you're using Python 3.11+:

.. code-block:: bash

   python --version

For conda environments, you can enforce the version:

.. code-block:: bash

   conda create -n umbra-env python=3.11
   conda activate umbra-env
   pip install -r requirements.txt

Missing NinaPro Data
~~~~~~~~~~~~~~~~~~~~

The preprocessing pipeline expects NinaPro data in ``data/ninapro/``. If the path doesn't exist, preprocessing will fail. Download the data from `NinaPro Database <http://ninaweb.hevs.ch/>`_.

Next Steps
==========

- Continue to the :doc:`usage` guide to learn how to run preprocessing, training, and the dashboard
- See :doc:`architecture` for an overview of the project structure
- Check the :doc:`guides/preprocessing` for detailed preprocessing pipeline documentation
