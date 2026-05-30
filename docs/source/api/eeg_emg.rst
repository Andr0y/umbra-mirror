###############
EEG-EMG API
###############

The ``src.eeg_emg`` module provides EEG to EMG translation utilities. **This module is currently under development** and not fully integrated into the main pipeline.

Overview
========

The EEG-EMG module aims to bridge EEG brain signals to EMG muscle signals, enabling direct brain-to-gesture control. Current implementation includes:

- **EEG Data Conversion**: Convert raw EEG data to standard formats
- **Data Augmentation**: Generate synthetic EEG-EMG pairs
- **Model Inference**: Run pre-trained EEG→EMG models

.. warning::

   This module is in development. API and functionality may change. Use with caution in production environments.

Module Reference
=================

src.eeg_emg.eeg2emg_run
~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: src.eeg_emg.eeg2emg_run
   :members:
   :undoc-members:
   :show-inheritance:

src.eeg_emg.convert_eeg_emg_to_npz
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: src.eeg_emg.convert_eeg_emg_to_npz
   :members:
   :undoc-members:
   :show-inheritance:

src.eeg_emg.data_augmentation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: src.eeg_emg.data_augmentation
   :members:
   :undoc-members:
   :show-inheritance:

src.eeg_emg.check_results
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: src.eeg_emg.check_results
   :members:
   :undoc-members:
   :show-inheritance:

Pre-trained Models
==================

**eeg2emg_best.pth**

A pre-trained PyTorch model for EEG→EMG translation is provided:

.. code-block:: bash

   src/eeg_emg/eeg2emg_best.pth

This model can be loaded for inference (see examples below).

Current Status
==============

✓ **Implemented**

- Basic model architecture
- Pre-trained model weights
- Data conversion utilities

✗ **Not Yet Implemented**

- Full training pipeline
- Integration with EMG→Movement model
- Comprehensive testing

Future Work
~~~~~~~~~~~

Planned improvements:

1. Complete training pipeline
2. Multi-subject adaptation
3. Real-time inference
4. End-to-end EEG→Movement system
5. Validation on live subject data

Usage Examples
==============

Loading Pre-trained Model
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import torch
   
   # Load pre-trained model
   model = torch.load('src/eeg_emg/eeg2emg_best.pth')
   model.eval()

Converting EEG Data
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from src.eeg_emg.convert_eeg_emg_to_npz import convert_to_npz
   
   # Convert raw EEG to NumPy format
   X_eeg, y = convert_to_npz(
       eeg_file='path/to/raw/eeg.csv',
       output_path='data/eeg_data/'
   )

Data Augmentation
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from src.eeg_emg.data_augmentation import augment_eeg_data
   
   # Generate augmented EEG-EMG pairs
   X_augmented = augment_eeg_data(
       X_eeg,
       augmentation_factor=2,  # Generate 2x more data
       noise_level=0.1
   )

Running Inference
~~~~~~~~~~~~~~~~~

.. code-block:: python

   from src.eeg_emg.eeg2emg_run import predict_emg
   import numpy as np
   
   # Load EEG data
   X_eeg = np.load('data/eeg_data/X.npy')
   
   # Predict corresponding EMG
   emg_predictions = predict_emg(X_eeg)
   
   # Shape: (n_samples, n_eeg_channels) -> (n_samples, n_emg_channels)

Validating Results
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from src.eeg_emg.check_results import validate_predictions
   
   # Validate EEG→EMG predictions
   metrics = validate_predictions(
       y_true=emg_ground_truth,
       y_pred=emg_predictions
   )
   
   print(f"MSE: {metrics['mse']:.4f}")
   print(f"Correlation: {metrics['correlation']:.4f}")

Integration with EMG→Movement
==============================

.. warning::

   Full integration not yet available.

The long-term goal is a complete pipeline:

.. code-block:: text

   Raw EEG Data
   ↓
   [src.eeg_emg] → EEG→EMG Translation
   ↓
   Predicted EMG Signals
   ↓
   [src.emg_movement] → EMG→Movement Classification
   ↓
   Hand Gesture Prediction

This will enable direct brain-to-gesture control without separate EMG sensors.

Roadmap
=======

Phase 1 (Current)
~~~~~~~~~~~~~~~~~

- ✓ Pre-trained model weights
- ✓ Basic data conversion
- ✓ Inference utilities

Phase 2 (Planned)
~~~~~~~~~~~~~~~~~

- Full training pipeline
- Multi-subject adaptation
- Comprehensive validation

Phase 3 (Planned)
~~~~~~~~~~~~~~~~~

- Real-time inference optimization
- End-to-end EEG→Movement integration
- Live subject testing

See Also
========

- :doc:`../guides/preprocessing` for EMG preprocessing
- :doc:`emg_movement` for EMG→Movement API
- :doc:`../usage` for usage examples
