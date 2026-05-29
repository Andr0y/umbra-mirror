################
Beta Test Plan
################

Overview
========

The Umbra project is in beta testing phase. This document outlines the beta test plan, key features being tested, and success criteria.

Project Context
===============

Umbra is a neuromuscular interface system designed to create a **motor copy of an individual** to assist with:

- Research and medicine (neurodegenerative disease treatment, motor rehabilitation)
- Daily life and safety (augmenting capabilities, exoskeleton assistance)

The system uses non-invasive biosignals:

- **EEG** (Electroencephalography): Brain signals
- **EMG** (Electromyography): Muscle signals

Beta Test Roles
===============

Two main roles are involved in beta testing:

**Supervisor**

- Supervises and assists the user during data collection
- Monitors system evolution and data quality
- Manages data preprocessing and model training

**User**

- Primary reference for creating the motor copy
- Provides biosignal data during sessions
- Tests the practical 3D prototype

Features Under Testing
======================

.. list-table:: Beta Test Features
   :header-rows: 1
   :widths: 10, 15, 30, 30

   * - Feature ID
     - User Role
     - Feature Name
     - Description
   * - F1
     - Supervisor
     - Minimal Dashboard
     - App to visualize EEG/EMG data flow, pinpoint anomalies
   * - F2
     - Everyone
     - Model Prototype
     - Basic model trained on fake/real data for 3D testing
   * - F3
     - Supervisor
     - Preprocessing Pipeline
     - Complete data processing from capture to dataset
   * - F4
     - Everyone
     - Practical 3D Test
     - Blender script with real-time model visualization
   * - F5
     - Supervisor
     - Hardware Impact Tracker
     - Monitor model resource consumption for optimization
   * - F6
     - Everyone
     - Dataset Quality Checker
     - Validate dataset integrity and distribution
   * - F7
     - Supervisor
     - Model Comparator Tool
     - Compare model iterations and performance
   * - F8
     - Everyone
     - Automated Setup Script
     - Fully automate EEG/EMG hardware and analysis setup

Success Criteria
================

.. list-table:: Beta Test Success Criteria
   :header-rows: 1
   :widths: 10, 30, 25, 20

   * - Feature ID
     - Key Success Criteria
     - Indicator/Metric
     - Status
   * - F1
     - Fake data injection with expected readings
     - 10 attempts without visualization failures
     - ✓ Achieved 10/10
   * - F2
     - Model behavior with normal/abnormal data
     - Non-chaotic model output
     - ⚠ Partially Achieved
   * - F3
     - Pipeline step execution with typical data
     - All steps work as intended
     - ✓ Achieved
   * - F4
     - 3D prop sync with model output
     - 10 movement attempts without failures
     - ⚠ Partially Achieved
   * - F5
     - Analysis behaves correctly with alerts
     - 10 attempts without analysis failures
     - ✓ Achieved 10/10
   * - F6
     - Strict dataset validation
     - 20 attempts (10 bad, 10 good) without errors
     - ✓ Achieved 20/20
   * - F7
     - Model ranking and identification
     - 20 attempts (10 normal, 10 broken) without errors
     - ✓ Achieved 20/20
   * - F8
     - Smooth setup process
     - User: 10 attempts (⚠ Partially Achieved), Supervisor: 10/10 ✓
     - ⚠ User Partial, ✓ Supervisor Success

Test Results Summary
====================

Passing Features (100% Success Rate)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **F1**: Dashboard visualization ✓
- **F3**: Preprocessing pipeline ✓
- **F5**: Hardware profiler ✓
- **F6**: Dataset quality checker ✓
- **F7**: Model comparator ✓
- **F8** (Supervisor): Automated setup ✓

Partially Passing Features
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **F2**: Model prototype (non-chaotic behavior mostly achieved)
- **F4**: 3D practical test (synchronization partially working)
- **F8** (User): Automated setup (minor issues with user workflow)

Next Steps
==========

Addressing Partial Failures
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**F2 - Model Prototype**

- Enhance model robustness with additional validation
- Improve behavior with edge cases
- Increase training data diversity

**F4 - Practical 3D Test**

- Debug synchronization issues
- Optimize real-time performance
- Test with more users

**F8 - User Setup Script**

- Streamline user workflow
- Add better documentation
- Provide interactive setup assistance

Current Development
~~~~~~~~~~~~~~~~~~~

- CNN-LSTM model fully implemented for EMG→Movement
- EEG→EMG model in development (placeholder stage)
- Dashboard with quality checker, profiler, comparator
- Preprocessing pipeline complete and validated

Recommendations for Testers
=============================

**For Supervisors**

1. Test all management features (preprocessing, training, comparison)
2. Validate data quality at each pipeline stage
3. Profile hardware requirements for your setup
4. Document any anomalies or edge cases

**For Users**

1. Wear EMG sensors comfortably during data collection
2. Perform gestures slowly and deliberately
3. Follow supervisor instructions carefully
4. Report any discomfort or signal issues immediately

Testing Environment
====================

- **Python**: 3.11+
- **TensorFlow/Keras**: 2.19+
- **Streamlit**: 1.41+
- **Hardware**: Minimum Intel i5, 8GB RAM (recommended: M1+ or i7 with 16GB+)
- **Storage**: 20GB for dataset + models

Feedback and Reporting
======================

To report issues or provide feedback:

1. Document the issue with steps to reproduce
2. Include error messages and logs
3. Specify your hardware configuration
4. Report to the development team via the issue tracker

See Also
========

- :doc:`../setup` for installation instructions
- :doc:`../usage` for usage guide
- :doc:`../architecture` for system architecture
