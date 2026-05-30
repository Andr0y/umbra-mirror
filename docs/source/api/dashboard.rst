##############
Dashboard API
##############

The ``src.dashboard`` module provides the Streamlit-based web interface for Umbra.

Overview
========

The Dashboard module consists of:

- **app.py**: Main dashboard entry point with inference interface
- **dataset_quality.py**: Dataset validation and quality checking
- **hardware_profiler.py**: Resource usage monitoring
- **model_comparator.py**: Multi-model performance comparison
- **pages/**: Streamlit multi-page apps accessible via sidebar

Module Reference
=================

src.dashboard.app
~~~~~~~~~~~~~~~~~

.. automodule:: src.dashboard.app
   :members:
   :undoc-members:
   :show-inheritance:

src.dashboard.dataset_quality
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: src.dashboard.dataset_quality
   :members:
   :undoc-members:
   :show-inheritance:

src.dashboard.hardware_profiler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: src.dashboard.hardware_profiler
   :members:
   :undoc-members:
   :show-inheritance:

src.dashboard.model_comparator
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: src.dashboard.model_comparator
   :members:
   :undoc-members:
   :show-inheritance:

Key Functions
=============

Launching Dashboard
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   streamlit run src/dashboard/app.py

Running on Custom Port
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   streamlit run src/dashboard/app.py --server.port 8080

Usage Examples
==============

Inference on Dataset
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from src.dashboard.app import load_dataset, load_model
   from tensorflow.keras.models import load_model
   
   # Load dataset
   dataset_id = 1
   X, y = load_dataset(dataset_id)
   
   # Load model
   model = load_model('src/models/cnn_lstm_emg_v3.keras')
   
   # Run inference
   predictions = model.predict(X)
   predicted_labels = np.argmax(predictions, axis=1)

Dataset Quality Checking
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from src.dashboard.dataset_quality import check_quality
   
   # Check dataset quality
   report = check_quality(
       dataset_id=1,
       min_samples_per_class=2000
   )
   
   print(f"Quality Score: {report['quality_score']}")
   print(f"Status: {report['status']}")

Hardware Profiling
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from src.dashboard.hardware_profiler import profile_model
   
   # Profile model performance
   metrics = profile_model(
       model_path='src/models/cnn_lstm_emg_v3.keras',
       batch_size=64,
       num_batches=100
   )
   
   print(f"Avg Inference Time: {metrics['avg_latency']} ms")
   print(f"Throughput: {metrics['throughput']} samples/sec")
   print(f"Memory Usage: {metrics['memory_used']} MB")

Model Comparison
~~~~~~~~~~~~~~~~

.. code-block:: python

   from src.dashboard.model_comparator import compare_models
   
   # Compare models
   results = compare_models(
       model_paths=[
           'src/models/cnn_lstm_emg_v3.keras',
           'src/models/cnn_lstm_emg_v2.keras'
       ],
       dataset_id=1,
       metric='f1_score'
   )
   
   for rank, (model, score) in enumerate(results, 1):
       print(f"{rank}. {model}: {score:.4f}")

Dashboard Configuration
======================

Page Configuration
~~~~~~~~~~~~~~~~~~

Customize dashboard settings in ``src/dashboard/app.py``:

.. code-block:: python

   import streamlit as st
   
   st.set_page_config(
       page_title="Umbra Dashboard",
       page_icon="🧠",
       layout="wide",
       initial_sidebar_state="expanded",
   )

Custom Styling
~~~~~~~~~~~~~~~

Add custom CSS to ``src/dashboard/_static/style.css``:

.. code-block:: css

   :root {
       --primary-color: #0084B4;
       --secondary-color: #FF6B6B;
       --text-color: #333333;
   }

Advanced Usage
==============

Adding Custom Pages
~~~~~~~~~~~~~~~~~~~~

Create a new file in ``src/dashboard/pages/``:

**4_Custom_Analysis.py**:

.. code-block:: python

   import streamlit as st
   import numpy as np
   
   st.title("Custom Analysis")
   
   # Your custom analysis code here
   dataset_id = st.selectbox("Select Dataset", [1, 2, 3])
   st.write(f"Analyzing dataset {dataset_id}...")

Custom Metrics
~~~~~~~~~~~~~~

Add custom metrics to ``src/dashboard/app.py``:

.. code-block:: python

   from sklearn.metrics import roc_auc_score
   
   def compute_custom_metrics(y_true, y_pred):
       """Compute additional evaluation metrics."""
       return {
           'roc_auc': roc_auc_score(y_true, y_pred, multi_class='ovr'),
           'custom_score': custom_evaluation_fn(y_true, y_pred)
       }

Caching for Performance
~~~~~~~~~~~~~~~~~~~~~~~

Use Streamlit caching for expensive operations:

.. code-block:: python

   import streamlit as st
   
   @st.cache_resource
   def load_model(model_path):
       from tensorflow.keras.models import load_model
       return load_model(model_path)
   
   @st.cache_data
   def load_dataset(dataset_id):
       import numpy as np
       X = np.load(f'data/preprocessed/{dataset_id}/X.npy')
       y = np.load(f'data/preprocessed/{dataset_id}/y.npy')
       return X, y

Deployment
==========

Local Deployment
~~~~~~~~~~~~~~~~

.. code-block:: bash

   streamlit run src/dashboard/app.py

Remote Deployment (Streamlit Cloud)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Push code to GitHub
2. Go to https://share.streamlit.io/
3. Deploy from GitHub repo

Docker Deployment
~~~~~~~~~~~~~~~~~

Build and run in Docker:

.. code-block:: bash

   docker build -t umbra-dashboard .
   docker run -p 8501:8501 umbra-dashboard

Environment Variables
~~~~~~~~~~~~~~~~~~~~~

Set environment variables for configuration:

.. code-block:: bash

   export DATA_PATH=data/
   export MODEL_PATH=src/models/
   export REPORT_PATH=data/reports/
   streamlit run src/dashboard/app.py

Troubleshooting
===============

"ModuleNotFoundError: streamlit"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Install Streamlit:

.. code-block:: bash

   pip install streamlit

"Dataset not found" error
~~~~~~~~~~~~~~~~~~~~~~~~~~

Ensure datasets exist in ``data/preprocessed/``:

.. code-block:: bash

   python -m src.main

"Model loading fails"
~~~~~~~~~~~~~~~~~~~~~~

Verify model exists and is in `.keras` format:

.. code-block:: bash

   ls src/models/*.keras

Slow inference
~~~~~~~~~~~~~~

Try:

- Reduce batch size
- Use GPU if available
- Cache models with ``@st.cache_resource``
- Profile with hardware profiler

See Also
========

- :doc:`../guides/dashboard` for dashboard usage guide
- :doc:`emg_movement` for EMG module API
- :doc:`../usage` for usage examples
