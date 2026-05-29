#####################
Model Training Guide
#####################

Overview
========

This guide covers training CNN-LSTM models for EMG-based hand gesture recognition. It includes best practices, hyperparameter tuning, and troubleshooting.

Model Architecture
==================

Umbra uses a **CNN-LSTM** architecture that combines:

1. **Convolutional Layers**: Extract local patterns from EMG signals
2. **LSTM Layers**: Model temporal dependencies in gesture sequences
3. **Dense Layers**: Final classification

Typical Architecture
~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   Input (batch_size, window_size, n_channels)
   ↓
   Conv1D (32 filters, kernel=5)
   ↓
   MaxPooling1D (pool_size=2)
   ↓
   LSTM (64 units, return_sequences=True)
   ↓
   LSTM (32 units)
   ↓
   Dense (64 units, activation='relu')
   ↓
   Dropout (0.5)
   ↓
   Dense (n_gestures, activation='softmax')
   ↓
   Output (batch_size, n_gestures)

Basic Training
==============

Prerequisite: Preprocessed Data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Before training, ensure you have preprocessed datasets:

.. code-block:: bash

   python -m src.main

This creates ``data/preprocessed/1/`` with ``X.npy`` and ``y.npy``.

Training Command
~~~~~~~~~~~~~~~~

.. code-block:: bash

   python -m src.emg_movement.train --dataset 1

Training Arguments
~~~~~~~~~~~~~~~~~~~

- ``--dataset N`` (default: 1)
  
  Dataset ID to use (e.g., ``data/preprocessed/N/``)

- ``--output FILE.keras`` (default: ``cnn_lstm_emg_v3.keras``)
  
  Output model filename (saved to ``src/models/``)

Examples
~~~~~~~~

Train on dataset 1 with default output:

.. code-block:: bash

   python -m src.emg_movement.train --dataset 1

Train on dataset 2 with custom model name:

.. code-block:: bash

   python -m src.emg_movement.train --dataset 2 --output cnn_lstm_custom.keras

Training Output
~~~~~~~~~~~~~~~

The training script outputs:

1. **Trained Model**: Saved to ``src/models/cnn_lstm_emg_v3.keras``
2. **Training Logs**: Console output with epochs, loss, accuracy
3. **Checkpoints**: Best model saved during training (via callbacks)

Example output:

.. code-block:: text

   Epoch 1/50
   500/500 [==============================] - 25s 50ms/step - loss: 2.1543 - accuracy: 0.3245 - val_loss: 1.9876 - val_accuracy: 0.4123
   Epoch 2/50
   500/500 [==============================] - 24s 48ms/step - loss: 1.8765 - accuracy: 0.4512 - val_loss: 1.7654 - val_accuracy: 0.5234
   ...
   Epoch 50/50
   500/500 [==============================] - 24s 48ms/step - loss: 0.2345 - accuracy: 0.9234 - val_loss: 0.4567 - val_accuracy: 0.8956

Advanced Training Configuration
================================

Hyperparameter Tuning
~~~~~~~~~~~~~~~~~~~~~

Key hyperparameters to tune:

- **Batch Size**: 32, 64, 128 (larger = faster but less stable)
- **Learning Rate**: 0.001 (default), 0.0001, 0.01
- **Dropout**: 0.3-0.5 (higher = more regularization)
- **L2 Regularization**: 0.0001-0.001
- **Epochs**: 50-200 depending on dataset size

Example: Custom Training Script
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For advanced control, create a custom training script:

.. code-block:: python

   from tensorflow.keras.models import Sequential
   from tensorflow.keras.layers import Conv1D, LSTM, Dense, Dropout, MaxPooling1D
   from tensorflow.keras.optimizers import Adam
   import numpy as np
   
   # Load preprocessed data
   X = np.load('data/preprocessed/1/X.npy')
   y = np.load('data/preprocessed/1/y.npy')
   
   # Split data
   from sklearn.model_selection import train_test_split
   X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
   X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2)
   
   # Build model
   model = Sequential([
       Conv1D(32, kernel_size=5, activation='relu', input_shape=(X.shape[1], X.shape[2] if len(X.shape) > 2 else 1)),
       MaxPooling1D(pool_size=2),
       LSTM(64, return_sequences=True),
       LSTM(32),
       Dense(64, activation='relu'),
       Dropout(0.5),
       Dense(len(np.unique(y)), activation='softmax')
   ])
   
   # Compile
   model.compile(
       optimizer=Adam(learning_rate=0.001),
       loss='sparse_categorical_crossentropy',
       metrics=['accuracy']
   )
   
   # Train
   model.fit(
       X_train, y_train,
       validation_data=(X_val, y_val),
       epochs=50,
       batch_size=64,
       verbose=1
   )
   
   # Evaluate
   test_loss, test_acc = model.evaluate(X_test, y_test)
   print(f"Test Accuracy: {test_acc:.4f}")
   
   # Save
   model.save('src/models/custom_model.keras')

Transfer Learning
~~~~~~~~~~~~~~~~~

Start with a pre-trained model and fine-tune:

.. code-block:: python

   from tensorflow.keras.models import load_model
   
   # Load pre-trained model
   model = load_model('src/models/cnn_lstm_emg_v3.keras')
   
   # Freeze early layers
   for layer in model.layers[:-2]:
       layer.trainable = False
   
   # Recompile with lower learning rate
   model.compile(
       optimizer=Adam(learning_rate=0.0001),
       loss='sparse_categorical_crossentropy',
       metrics=['accuracy']
   )
   
   # Fine-tune on new data
   model.fit(X_new, y_new, epochs=10, batch_size=64)
   model.save('src/models/finetuned_model.keras')

Model Evaluation
================

Evaluating on Test Set
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from tensorflow.keras.models import load_model
   from sklearn.metrics import classification_report, confusion_matrix
   import numpy as np
   
   model = load_model('src/models/cnn_lstm_emg_v3.keras')
   X_test = np.load('data/preprocessed/1/X_test.npy')
   y_test = np.load('data/preprocessed/1/y_test.npy')
   
   # Predictions
   y_pred = np.argmax(model.predict(X_test), axis=1)
   
   # Classification report
   print(classification_report(y_test, y_pred))
   
   # Confusion matrix
   cm = confusion_matrix(y_test, y_pred)
   print(f"Confusion Matrix:\n{cm}")

Cross-Validation
~~~~~~~~~~~~~~~~

Use k-fold cross-validation for robust evaluation:

.. code-block:: python

   from sklearn.model_selection import KFold
   
   kf = KFold(n_splits=5)
   scores = []
   
   for train_idx, val_idx in kf.split(X):
       X_train, X_val = X[train_idx], X[val_idx]
       y_train, y_val = y[train_idx], y[val_idx]
       
       model = build_model()  # Your model building function
       model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=50)
       score = model.evaluate(X_val, y_val)[1]
       scores.append(score)
   
   print(f"Mean CV Accuracy: {np.mean(scores):.4f} ± {np.std(scores):.4f}")

Tracking Experiments
====================

Using MLflow
~~~~~~~~~~~~

Log experiments for reproducibility:

.. code-block:: python

   import mlflow
   
   mlflow.start_run()
   mlflow.log_param("batch_size", 64)
   mlflow.log_param("learning_rate", 0.001)
   mlflow.log_param("epochs", 50)
   
   # Train model...
   
   mlflow.log_metric("test_accuracy", test_acc)
   mlflow.log_artifact("src/models/cnn_lstm_emg_v3.keras")
   mlflow.end_run()

View experiments:

.. code-block:: bash

   mlflow ui

Best Practices
==============

1. **Start Simple**: Train a small model first, then scale up
2. **Use Callbacks**: Early stopping, learning rate scheduling
3. **Monitor Metrics**: Loss, accuracy, F1-score, per-class performance
4. **Validate Regularly**: Use validation set during training
5. **Save Best Model**: Keep the model with best validation performance
6. **Document Hyperparameters**: Log all settings for reproducibility
7. **Normalize Data**: Zero mean, unit variance (or use batch normalization)
8. **Balance Data**: Handle class imbalance with class weights or stratified splits
9. **Augment Data**: Use data augmentation to improve generalization
10. **Test on Holdout Set**: Final evaluation on completely unseen data

Troubleshooting
===============

"Model not converging / loss not decreasing"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Try:

- Reduce learning rate
- Increase batch size
- Check data normalization
- Verify data labels are correct
- Try different model architecture

"Out of memory during training"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Solutions:

- Reduce batch size
- Reduce model complexity (fewer layers/units)
- Use gradient checkpointing
- Train on a machine with more RAM/GPU memory

"Validation accuracy much lower than training"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Indicates overfitting:

- Increase dropout rate
- Add L2 regularization
- Use early stopping
- Reduce model complexity
- Increase data augmentation

Next Steps
==========

- See :doc:`../usage` for usage examples
- Check :doc:`dashboard` for model evaluation using the dashboard
- Explore :doc:`../api/emg_movement` for training API details
