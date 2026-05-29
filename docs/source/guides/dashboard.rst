##################
Dashboard Guide
##################

Overview
========

The Umbra Dashboard is a **Streamlit-based** web application for visualizing EMG data, running model inference, and analyzing results. It provides multiple interactive tools for dataset validation, model comparison, and performance profiling.

Launching the Dashboard
=======================

Start the dashboard from the repository root:

.. code-block:: bash

   streamlit run src/dashboard/app.py

The dashboard will open at ``http://localhost:8501`` in your default browser.

To run on a specific port:

.. code-block:: bash

   streamlit run src/dashboard/app.py --server.port 8080

Main Dashboard Features
=======================

The main dashboard page provides:

1. **Dataset Selection**
2. **Model Loading**
3. **Inference Interface**
4. **Results Visualization**

Step-by-Step Usage
~~~~~~~~~~~~~~~~~~

1. **Select Dataset**
   
   Choose a preprocessed dataset from the dropdown (e.g., ``1``, ``2``).
   Displays dataset info: shape, gesture count, class distribution.

2. **Load Model**
   
   Select a trained `.keras` model from ``src/models/``.
   Shows model architecture and parameter count.

3. **Run Inference**
   
   Click "Run Inference" to predict on the selected dataset.
   Displays predictions, confidence scores, confusion matrix.

4. **View Results**
   
   - Accuracy, F1-score, and per-class metrics
   - Confusion matrix heatmap
   - Prediction distribution

Sidebar Tools
=============

The Streamlit sidebar provides access to specialized analysis tools.

Dataset Quality Checker
~~~~~~~~~~~~~~~~~~~~~~~

**Location**: Sidebar → "Dataset Quality Check"

**Purpose**: Validate preprocessed datasets for training readiness

**Checks Performed**:

- ✓ File integrity (X.npy, y.npy exist and valid)
- ✓ Data shape consistency
- ✓ Label range validation (0 to n_gestures-1)
- ✓ Class distribution (sufficient samples per gesture)
- ✓ Missing value detection
- ✓ Train/test/validation split validation

**Usage**:

1. Select dataset to validate
2. Choose minimum samples per class threshold
3. Click "Check Quality"
4. Review report

**Output**:

- Overall quality score (0-100)
- Per-gesture sample counts
- Warnings and recommendations
- Exportable quality report (JSON)

Example Report
~~~~~~~~~~~~~~

.. code-block:: json

   {
     "dataset_id": 1,
     "status": "PASS",
     "quality_score": 92.5,
     "checks": {
       "file_integrity": "PASS",
       "data_shape": "PASS",
       "label_range": "PASS",
       "class_distribution": "PASS",
       "missing_values": "PASS"
     },
     "statistics": {
       "n_samples": 150000,
       "n_features": 128,
       "n_classes": 52,
       "samples_per_class_min": 2456,
       "samples_per_class_mean": 2884,
       "class_imbalance_ratio": 1.28
     }
   }

Hardware Impact Tracker
~~~~~~~~~~~~~~~~~~~~~~~

**Location**: Sidebar → "Hardware Impact Tracker"

**Purpose**: Monitor computational resource usage during training and inference

**Metrics Tracked**:

- CPU usage (%)
- Memory usage (GB)
- GPU usage (if available)
- Inference latency (ms/sample)
- Model size (MB)

**Features**:

1. **Real-time Monitoring**
   
   - Live CPU/RAM graphs
   - Update frequency: 1-5 seconds

2. **Model Profiling**
   
   - Inference time per batch
   - Memory footprint
   - Throughput (samples/sec)

3. **Hardware Requirements**
   
   - Recommends minimum hardware based on model
   - Estimates training time

**Usage**:

1. Select model to profile
2. Set test batch size (32, 64, 128)
3. Click "Profile Model"
4. Review resource usage graphs

**Output Example**:

.. code-block:: text

   Model: cnn_lstm_emg_v3.keras
   
   ┌─ Inference Profiling ──────┐
   │ Batch Size: 64             │
   │ Avg Latency: 45 ms         │
   │ Throughput: 1422 samples/s │
   │ Memory: 256 MB             │
   └────────────────────────────┘

Model Comparator
~~~~~~~~~~~~~~~~

**Location**: Sidebar → "Model Comparator"

**Purpose**: Compare multiple trained models on the same dataset

**Comparison Metrics**:

- Accuracy, Precision, Recall, F1-score
- Inference latency
- Model size
- Confusion matrices
- Per-class performance

**Features**:

1. **Multi-Model Selection**
   
   Select multiple models to compare simultaneously

2. **Performance Ranking**
   
   Automatically ranks models by selected metric

3. **Metric Visualization**
   
   - Bar charts for metric comparison
   - Performance curves across epochs
   - Per-gesture accuracy heatmap

4. **Export Reports**
   
   Download comparison reports as CSV or JSON

**Usage**:

1. Select 2+ models from ``src/models/``
2. Choose dataset for evaluation
3. Select comparison metric (accuracy, F1, latency)
4. Click "Compare Models"
5. Review results and export if needed

**Example Output**:

.. code-block:: text

   Model Comparison Results (Dataset 1)
   
   Rank │ Model                    │ Accuracy │ F1-Score │ Latency
   ─────┼──────────────────────────┼──────────┼──────────┼─────────
   1    │ cnn_lstm_emg_v3.keras    │ 0.8956   │ 0.8923   │ 45 ms
   2    │ cnn_lstm_emg_v2.keras    │ 0.8734   │ 0.8701   │ 42 ms
   3    │ cnn_lstm_1.keras         │ 0.7234   │ 0.7156   │ 38 ms

Dashboard Architecture
======================

File Structure
~~~~~~~~~~~~~~

.. code-block:: text

   src/dashboard/
   ├── app.py                      # Main dashboard entry point
   ├── dataset_quality.py          # Dataset validation module
   ├── hardware_profiler.py        # Hardware profiling module
   ├── model_comparator.py         # Model comparison module
   └── pages/                      # Streamlit multi-page apps
       ├── 1_Dataset_Quality_Check.py
       ├── 2_Model_Comparator.py
       └── 3_Hardware_Impact_Tracker.py

Main Components
~~~~~~~~~~~~~~~

**app.py**: Entry Point

- Initializes Streamlit session state
- Loads sidebar pages
- Provides main inference interface

**dataset_quality.py**: Validation Logic

- Loads preprocessed datasets
- Runs integrity checks
- Generates quality reports

**hardware_profiler.py**: Resource Monitoring

- Monitors CPU/GPU/RAM usage
- Profiles model inference
- Tracks performance metrics

**model_comparator.py**: Comparison Logic

- Loads multiple models
- Evaluates on same dataset
- Generates comparison reports

Configuration
=============

Dashboard Settings
~~~~~~~~~~~~~~~~~~

Modify dashboard behavior in ``src/dashboard/app.py``:

.. code-block:: python

   # Page configuration
   st.set_page_config(
       page_title="Umbra Dashboard",
       layout="wide",
       initial_sidebar_state="expanded"
   )
   
   # Color theme
   PRIMARY_COLOR = "#0084B4"
   SECONDARY_COLOR = "#FF6B6B"

Data Paths
~~~~~~~~~~

All paths are defined in [src/config.py](../../src/config.py):

.. code-block:: python

   PREPROCESS_PATH = "data/preprocessed"      # Input datasets
   MODEL_DIR = "src/models"                   # Input models
   QUALITY_REPORTS_DIR = "data/quality_reports"      # Output reports
   COMPARISON_REPORTS_DIR = "data/comparison_reports"  # Comparison outputs
   HARDWARE_REPORTS_DIR = "data/hardware_reports"     # Hardware profiles

Examples
========

Example 1: Validate a Dataset
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   streamlit run src/dashboard/app.py
   # 1. Select "Dataset Quality Check" from sidebar
   # 2. Select dataset ID "1"
   # 3. Set min samples: 2000
   # 4. Click "Check Quality"

Example 2: Compare Two Models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   streamlit run src/dashboard/app.py
   # 1. Select "Model Comparator" from sidebar
   # 2. Check models: "cnn_lstm_emg_v3.keras" and "cnn_lstm_emg_v2.keras"
   # 3. Select dataset: "1"
   # 4. Select metric: "F1-Score"
   # 5. Click "Compare Models"

Example 3: Profile Model Hardware Impact
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   streamlit run src/dashboard/app.py
   # 1. Select "Hardware Impact Tracker" from sidebar
   # 2. Select model: "cnn_lstm_emg_v3.keras"
   # 3. Set batch size: 64
   # 4. Click "Profile Model"
   # 5. View CPU/GPU/memory graphs

Troubleshooting
===============

"ModuleNotFoundError: streamlit"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Install Streamlit:

.. code-block:: bash

   pip install streamlit

"Connection refused on localhost:8501"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Port might be in use. Try a different port:

.. code-block:: bash

   streamlit run src/dashboard/app.py --server.port 8080

"Dataset not found"
~~~~~~~~~~~~~~~~~~~~

Ensure preprocessed data exists in ``data/preprocessed/``:

.. code-block:: bash

   python -m src.main  # Generate preprocessed data

"Model fails to load"
~~~~~~~~~~~~~~~~~~~~~

Check that model exists in ``src/models/`` and is in `.keras` format.

Performance Tips
================

1. **Use Caching**: Streamlit caches expensive computations
2. **Reduce Dataset Size**: Test with smaller datasets first
3. **Batch Processing**: Process large datasets in batches
4. **Lazy Loading**: Load models only when needed
5. **Optimize Plots**: Use efficient visualization libraries

Next Steps
==========

- See :doc:`../usage` for usage examples
- Check :doc:`model_training` for model training best practices
- Read the :doc:`../api/dashboard` for dashboard API reference
