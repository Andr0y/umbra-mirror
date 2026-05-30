###########
Usage Guide
###########

Overview
========

The Umbra project provides a complete pipeline for EMG signal processing and hand gesture recognition. The main workflow consists of:

1. **Preprocessing**: Convert raw NinaPro EMG data into windowed datasets
2. **Training**: Train a CNN-LSTM model on preprocessed data
3. **Evaluation**: Use the dashboard to visualize and evaluate models
4. **Comparison**: Compare multiple model versions using the comparator tool

All commands should be run from the repository root.

Quick Start
===========

Activate the virtual environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Before running any command, activate your environment:

.. code-block:: bash

   source venv/bin/activate
   # Or if using conda: conda activate umbra-env

1. Preprocessing EMG Data
=========================

Convert raw NinaPro data into windowed EMG datasets with labels.

Running Preprocessing
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   python -m src.main

This command:

- Reads raw NinaPro data from ``data/ninapro/``
- Applies preprocessing (filtering, windowing)
- Outputs preprocessed datasets to ``data/preprocessed/<id>/`` with:
  - ``X.npy``: Feature matrix (n_samples, n_features)
  - ``y.npy``: Label vector (n_samples,)

Preprocessing Output
~~~~~~~~~~~~~~~~~~~~

Each preprocessing run creates a new directory with a unique ID:

.. code-block:: text

   data/preprocessed/
   ├── 1/
   │   ├── X.npy          # Preprocessed features
   │   └── y.npy          # Labels
   ├── 2/
   │   ├── X.npy
   │   └── y.npy
   └── ...

Configuration
~~~~~~~~~~~~~~

Preprocessing parameters are defined in [src/config.py](../src/config.py):

.. code-block:: python

   WINDOW_MS = 500          # 500 ms window
   WINDOW_STEP_MS = 100     # 100 ms step (50% overlap)
   LOWPASS_CUTOFF = 5       # 5 Hz lowpass filter
   FILTER_ORDER = 2

2. Model Training
=================

Train a CNN-LSTM model on preprocessed EMG data.

Basic Training
~~~~~~~~~~~~~~

Train using dataset ID 1 (created during preprocessing):

.. code-block:: bash

   python -m src.emg_movement.train --dataset 1

Training Arguments
~~~~~~~~~~~~~~~~~~

- ``--dataset N`` (default: 1)
  
  Preprocessed dataset ID to use (e.g., ``data/preprocessed/N/``)

- ``--output FILE.keras`` (default: ``cnn_lstm_emg_v3.keras``)
  
  Output filename for the trained model (saved in ``src/models/``)

Example with custom output:

.. code-block:: bash

   python -m src.emg_movement.train --dataset 1 --output cnn_lstm_best.keras

Training Output
~~~~~~~~~~~~~~~

Trained models are saved to ``src/models/``:

.. code-block:: text

   src/models/
   ├── cnn_lstm_emg_v1.keras
   ├── cnn_lstm_emg_v2.keras
   ├── cnn_lstm_emg_v3.keras
   └── cnn_lstm_best.keras

Training typically takes 5-15 minutes depending on dataset size and hardware.

3. Streamlit Dashboard
======================

Visualize datasets, run inference, and analyze model performance.

Launching the Dashboard
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   streamlit run src/dashboard/app.py

The dashboard will open at ``http://localhost:8501`` in your default browser.

Dashboard Features
~~~~~~~~~~~~~~~~~~

**EMG Hand Movement Decoder** (Main Tab)

- Select a preprocessed dataset from ``data/preprocessed/``
- Load a trained model from ``src/models/``
- Run inference on test data
- View predictions and confidence scores

**Dataset Quality Checker** (Sidebar)

- Validate preprocessed dataset integrity
- Check train/test/evaluation split distribution
- Ensure minimum samples per gesture
- Detect data anomalies

**Model Comparator** (Sidebar)

- Load multiple trained models
- Compare performance metrics across datasets
- Identify best-performing iterations
- Export comparison reports

**Hardware Impact Tracker** (Sidebar)

- Monitor memory and CPU usage during training
- Track model inference latency
- Identify optimization opportunities
- Generate hardware profiling reports

4. Advanced Usage
=================

Batch Processing
~~~~~~~~~~~~~~~~

Process multiple datasets sequentially:

.. code-block:: bash

   for id in {1..5}; do
     echo "Training on dataset $id..."
     python -m src.emg_movement.train --dataset $id --output "cnn_lstm_v3_dataset${id}.keras"
   done

Custom Preprocessing
~~~~~~~~~~~~~~~~~~~~

For advanced preprocessing customization, edit [src/emg_movement/preprocessing.py](../src/emg_movement/preprocessing.py):

.. code-block:: python

   from src.emg_movement.preprocessing import EMGPreprocessor
   
   preprocessor = EMGPreprocessor()
   X, y = preprocessor.preprocess()  # Returns feature matrix and labels

Model Evaluation
~~~~~~~~~~~~~~~~

Export model predictions and evaluation metrics:

.. code-block:: bash

   python -c "
   from src.emg_movement.preprocessing import EMGPreprocessor
   from tensorflow.keras.models import load_model
   
   model = load_model('src/models/cnn_lstm_emg_v3.keras')
   X_test, y_test = EMGPreprocessor().preprocess()
   predictions = model.predict(X_test)
   "

Running Tests
~~~~~~~~~~~~~

Execute the test suite:

.. code-block:: bash

   pytest tests/

Run specific tests:

.. code-block:: bash

   pytest tests/test_model.py -v
   pytest tests/test_env.py::test_imports -v

Debugging
=========

Enable Verbose Output
~~~~~~~~~~~~~~~~~~~~~

Set environment variable for TensorFlow logging:

.. code-block:: bash

   TF_CPP_MIN_LOG_LEVEL=0 python -m src.emg_movement.train --dataset 1

View Streamlit Logs
~~~~~~~~~~~~~~~~~~~

Run the dashboard with verbose logging:

.. code-block:: bash

   streamlit run src/dashboard/app.py --logger.level=debug

Check Dataset Integrity
~~~~~~~~~~~~~~~~~~~~~~~

Validate a preprocessed dataset:

.. code-block:: python

   import numpy as np
   
   X = np.load('data/preprocessed/1/X.npy')
   y = np.load('data/preprocessed/1/y.npy')
   
   print(f"Features shape: {X.shape}")
   print(f"Labels shape: {y.shape}")
   print(f"Unique gestures: {np.unique(y)}")

Next Steps
==========

- See :doc:`guides/preprocessing` for detailed preprocessing pipeline documentation
- Check :doc:`guides/model_training` for training best practices
- Read :doc:`guides/dashboard` for dashboard feature details
- Explore the :doc:`api/emg_movement` for API reference
