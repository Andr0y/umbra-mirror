######################
Preprocessing Guide
######################

Overview
========

The preprocessing pipeline converts raw NinaPro electromyogram (EMG) data into windowed, normalized datasets ready for model training. This guide covers the preprocessing architecture, parameters, and customization options.

Why Preprocessing?
==================

Raw EMG data requires several processing steps:

1. **Noise Removal**: Electrical interference and motion artifacts
2. **Normalization**: Account for inter-subject and inter-session variability
3. **Windowing**: Convert continuous signals into discrete samples
4. **Feature Engineering**: Extract meaningful patterns for the model

Preprocessing Pipeline
======================

The preprocessing pipeline follows these steps:

.. code-block:: text

   Raw EMG Data
   ↓
   Load NinaPro Dataset
   ↓
   Apply Bandpass Filter (5 Hz lowpass)
   ↓
   Create Sliding Windows (500 ms, 50% overlap)
   ↓
   Normalize Features (zero mean, unit variance)
   ↓
   Create Train/Test Split
   ↓
   Save NumPy Arrays (X.npy, y.npy)

Running Preprocessing
=====================

Basic Preprocessing
~~~~~~~~~~~~~~~~~~~

From the repository root:

.. code-block:: bash

   python -m src.main

This runs the default preprocessing pipeline and outputs to ``data/preprocessed/1/``.

Output Structure
~~~~~~~~~~~~~~~~

Preprocessing creates:

.. code-block:: text

   data/preprocessed/
   └── 1/
       ├── X.npy       # Shape: (n_samples, n_channels * n_features)
       └── y.npy       # Shape: (n_samples,) - gesture labels

Example output:

- ``X.npy``: (150000, 128) – 150k windows × 128 features per window
- ``y.npy``: (150000,) – gesture labels (0-52 for NinaPro DB1)

Preprocessing Parameters
========================

All parameters are defined in [src/config.py](../../src/config.py).

Sampling Rate
~~~~~~~~~~~~~

.. code-block:: python

   FS = 1000              # EMG sampling frequency (Hz)
   SAMPLING_EMG_RATE = 100  # Output resampling rate (Hz) - optional

Window Configuration
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   WINDOW_MS = 500              # Window size: 500 milliseconds
   WINDOW_SAMPLES = 500         # Samples per window: 500 (at 1000 Hz)
   WINDOW_STEP_MS = 100         # Window step: 100 milliseconds
   WINDOW_STEP_SAMPLES = 100    # Samples per step: 100 (50% overlap)

This creates overlapping windows:

- Window 1: samples [0, 500)
- Window 2: samples [100, 600)
- Window 3: samples [200, 700)
- ...

Filtering
~~~~~~~~~

.. code-block:: python

   LOWPASS_CUTOFF = 5    # Lowpass filter cutoff frequency (Hz)
   FILTER_ORDER = 2      # Filter order (2nd-order Butterworth)

This removes high-frequency noise while preserving gesture-relevant frequencies.

Labels
~~~~~~

.. code-block:: python

   REST_LABEL = 0        # Label for rest/no gesture state

Customizing Preprocessing
==========================

Modifying Parameters
~~~~~~~~~~~~~~~~~~~~

Edit [src/config.py](../../src/config.py) to change preprocessing settings:

.. code-block:: python

   # Example: Increase window size to 1000 ms
   WINDOW_MS = 1000
   WINDOW_SAMPLES = 1000
   WINDOW_STEP_MS = 200
   WINDOW_STEP_SAMPLES = 200

Then re-run preprocessing to generate a new dataset.

Advanced: Custom Preprocessing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For custom preprocessing logic, modify [src/emg_movement/preprocessing.py](../../src/emg_movement/preprocessing.py):

.. code-block:: python

   from src.emg_movement.preprocessing import EMGPreprocessor
   
   class CustomPreprocessor(EMGPreprocessor):
       def preprocess(self):
           """Custom preprocessing with additional steps."""
           X, y = super().preprocess()
           
           # Add custom processing here
           # e.g., additional feature engineering, augmentation
           
           return X, y

Example: Add PCA Dimensionality Reduction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from sklearn.decomposition import PCA
   from src.emg_movement.preprocessing import EMGPreprocessor
   
   preprocessor = EMGPreprocessor()
   X, y = preprocessor.preprocess()
   
   # Apply PCA to reduce to 64 dimensions
   pca = PCA(n_components=64)
   X_reduced = pca.fit_transform(X)
   
   print(f"Original shape: {X.shape}")
   print(f"Reduced shape: {X_reduced.shape}")

Example: Feature Engineering
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Extract additional hand-crafted features:

.. code-block:: python

   import numpy as np
   from scipy.signal import welch
   
   def extract_spectral_features(emg_window):
       """Extract frequency-domain features from EMG window."""
       freqs, power = welch(emg_window, fs=1000)
       
       # Power in common EMG bands
       delta = np.sum(power[(freqs > 0) & (freqs < 5)])      # 0-5 Hz
       theta = np.sum(power[(freqs > 5) & (freqs < 15)])     # 5-15 Hz
       alpha = np.sum(power[(freqs > 15) & (freqs < 50)])    # 15-50 Hz
       
       return np.array([delta, theta, alpha])

Troubleshooting Preprocessing
==============================

"ModuleNotFoundError: No module named 'src'"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Ensure you're running from the repository root:

.. code-block:: bash

   cd /path/to/umbra
   python -m src.main

"FileNotFoundError: data/ninapro not found"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Download the NinaPro dataset and place it in ``data/ninapro/``. See the :doc:`../setup` guide for download instructions.

"Memory error during preprocessing"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If preprocessing runs out of memory:

1. Reduce ``WINDOW_MS`` or increase ``WINDOW_STEP_MS``
2. Process a subset of the NinaPro database
3. Use a machine with more RAM

"NaN values in output"
~~~~~~~~~~~~~~~~~~~~~~~

Check for:

- Corrupted input data (use dataset quality checker)
- Division by zero (check filter parameters)
- Empty windows (increase ``WINDOW_STEP_MS``)

Next Steps
==========

- Read :doc:`../usage` for instructions on training with preprocessed data
- See :doc:`model_training` for model training best practices
- Check the :doc:`../api/emg_movement` for preprocessing API reference
