####################
EMG Movement API
####################

The ``src.emg_movement`` module provides EMG signal processing, model architecture, and training utilities for hand gesture recognition.

Overview
========

The EMG Movement module is the core of Umbra's gesture recognition system:

- **Preprocessing**: Filter, window, and normalize raw EMG signals
- **Model Architecture**: CNN-LSTM neural network for gesture classification
- **Training**: End-to-end training pipeline with validation and early stopping
- **Utilities**: Helper functions for data loading, metrics, and visualization

Module Reference
=================

src.emg_movement.preprocessing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: src.emg_movement.preprocessing
   :members:
   :undoc-members:
   :show-inheritance:

src.emg_movement.model
~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: src.emg_movement.model
   :members:
   :undoc-members:
   :show-inheritance:

src.emg_movement.train
~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: src.emg_movement.train
   :members:
   :undoc-members:
   :show-inheritance:

src.emg_movement.utils
~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: src.emg_movement.utils
   :members:
   :undoc-members:
   :show-inheritance:

src.emg_movement.gestures
~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: src.emg_movement.gestures
   :members:
   :undoc-members:
   :show-inheritance:

Key Classes
===========

EMGPreprocessor
~~~~~~~~~~~~~~~

The main preprocessing class for EMG data:

.. autoclass:: src.emg_movement.preprocessing.EMGPreprocessor
   :members:
   :undoc-members:
   :show-inheritance:

Common Usage Patterns
=====================

Preprocessing EMG Data
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from src.emg_movement.preprocessing import EMGPreprocessor
   
   # Create preprocessor instance
   preprocessor = EMGPreprocessor()
   
   # Run preprocessing pipeline
   X, y = preprocessor.preprocess()
   
   # X: (n_samples, n_features)
   # y: (n_samples,) gesture labels

Building a Model
~~~~~~~~~~~~~~~~

.. code-block:: python

   from src.emg_movement.model import build_model
   
   # Build CNN-LSTM model
   model = build_model(
       input_shape=(500, 128),  # (window_size, n_channels)
       n_classes=52             # NinaPro gestures
   )
   
   model.summary()

Training a Model
~~~~~~~~~~~~~~~~

.. code-block:: python

   from src.emg_movement.train import train_model
   
   # Train with preprocessing data
   preprocessor = EMGPreprocessor()
   X, y = preprocessor.preprocess()
   
   model = train_model(
       X, y,
       epochs=50,
       batch_size=64,
       validation_split=0.2
   )
   
   # Save model
   model.save('src/models/trained_model.keras')

Loading and Using a Model
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from tensorflow.keras.models import load_model
   import numpy as np
   
   # Load trained model
   model = load_model('src/models/cnn_lstm_emg_v3.keras')
   
   # Load test data
   X_test = np.load('data/preprocessed/1/X_test.npy')
   
   # Run inference
   predictions = model.predict(X_test)
   predicted_labels = np.argmax(predictions, axis=1)

See Also
========

- :doc:`../guides/preprocessing` for preprocessing pipeline details
- :doc:`../guides/model_training` for training best practices
- :doc:`../usage` for usage examples
