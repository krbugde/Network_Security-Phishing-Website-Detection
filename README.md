# Network Security - Phishing Data Detection

A comprehensive machine learning pipeline for detecting and classifying phishing network traffic and security threats. This project implements an end-to-end ML workflow with data ingestion, validation, transformation, and model training components.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Pipeline Architecture](#pipeline-architecture)
- [Components](#components)
- [Requirements](#requirements)
- [Author](#author)

## Overview

This project provides a production-ready machine learning pipeline for network security threat detection, specifically focusing on phishing classification. It fetches network security data from MongoDB, performs comprehensive data validation, applies transformations, and trains machine learning models with automatic drift detection and monitoring.

### Key Features:

- **Automated Data Pipeline**: Streamlined data flow from MongoDB to model training
- **Data Validation**: Drift detection and data quality checks
- **Model Training**: Multiple algorithms with hyperparameter tuning using GridSearchCV
- **Experiment Tracking**: MLflow integration for tracking models and metrics
- **REST API**: FastAPI endpoints for model serving
- **Error Handling**: Custom exception handling and comprehensive logging
- **Reproducibility**: Structured configuration management and artifact versioning

## Features

✅ **Data Ingestion**
- Connects to MongoDB for data retrieval
- Automatic train-test splitting with configurable ratios
- CSV export for processed data

✅ **Data Validation**
- Schema validation against defined YAML schemas
- Data drift detection reports
- Data quality checks
- Automated validation workflow

✅ **Data Transformation**
- Feature preprocessing and normalization
- Scaling and encoding transformations
- Artifact management for reproducibility

✅ **Model Training**
- Multiple algorithm support (Random Forest, Gradient Boosting, etc.)
- Hyperparameter tuning with GridSearchCV
- Automated model evaluation and selection
- Performance metrics computation

✅ **Experiment Tracking**
- MLflow integration for experiment management
- DagsHub integration for model versioning
- Artifact and model storage

✅ **API Deployment**
- FastAPI for serving predictions
- RESTful endpoints for inference

## Project Structure

```
NetworkSecurity/
│
├── networksecurity/
│   ├── __init__.py
│   ├── components/
│   │   ├── data_ingestion.py       # MongoDB data retrieval & train-test split
│   │   ├── data_validation.py      # Schema validation & drift detection
│   │   ├── data_transformation.py  # Feature engineering & preprocessing
│   │   └── model_trainer.py        # Model training & evaluation
│   │
│   ├── entity/
│   │   ├── config_entity.py        # Configuration classes
│   │   └── artifact_entity.py      # Output artifact definitions
│   │
│   ├── constant/
│   │   └── training_pipeline/      # Pipeline constants
│   │
│   ├── exception/
│   │   └── exception.py            # Custom exception class
│   │
│   ├── logging/
│   │   └── logger.py               # Logging configuration
│   │
│   ├── pipeline/
│   │   └── __init__.py
│   │
│   ├── utils/
│   │   ├── main_utils/
│   │   │   └── utils.py            # Utility functions
│   │   └── ml_utils/
│   │       ├── metric/
│   │       │   └── classification_metric.py
│   │       └── model/
│   │           └── estimator.py
│   │
│   └── cloud/
│       └── __init__.py
│
├── data_schema/
│   └── schema.yaml                 # Data validation schema
│
├── logs/                           # Application logs
├── final_model/                    # Trained model storage
├── Artifacts/                      # Timestamped pipeline outputs
│
├── main.py                         # Training pipeline entry point
├── push_data.py                    # Data upload to MongoDB
├── test_mongodb.py                 # MongoDB connection test
│
├── requirements.txt                # Project dependencies
├── setup.py                        # Package configuration
├── Dockerfile                      # Container configuration
│
└── notebooks/                      # Jupyter notebooks for exploration
```

## Installation

### Prerequisites
- Python 3.8 or higher
- MongoDB instance (local or cloud)
- pip package manager

### Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd NetworkSecurity
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate    # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

## Configuration

### Environment Variables

Create a `.env` file in the project root with:

```env
MONGO_DB_URL=mongodb://<username>:<password>@<host>:<port>/<database>
```

### Schema Configuration

Update `data_schema/schema.yaml` with your data validation schema. Example format:

```yaml
properties:
  feature_1:
    type: number
  feature_2:
    type: string
required:
  - feature_1
  - feature_2
```

### Pipeline Configuration

Modify `data_ingestion` configuration in `networksecurity/entity/config_entity.py`:
- MongoDB connection settings
- Train-test split ratio (default: 80-20)
- Data paths and artifact directories

## Usage

### Run the Complete Training Pipeline

```bash
python main.py
```

This will execute:
1. **Data Ingestion** - Fetch data from MongoDB and create train/test splits
2. **Data Validation** - Validate data schema and detect drift
3. **Data Transformation** - Apply preprocessing and normalization
4. **Model Training** - Train and evaluate multiple models

### Upload Data to MongoDB

```bash
python push_data.py
```

### Test MongoDB Connection

```bash
python test_mongodb.py
```

## Pipeline Architecture

```
┌─────────────────────┐
│  Data Ingestion     │ ← MongoDB
├─────────────────────┤
│ Training Pipeline   │
│   Config            │
├─────────────────────┤
│ Data Validation     │ → Drift Report
├─────────────────────┤
│ Data Transformation │ → Transformed Data
├─────────────────────┤
│ Model Trainer       │ → Trained Model
├─────────────────────┤
│ MLflow Tracking     │
└─────────────────────┘
```

## Components

### Data Ingestion
- **File**: `networksecurity/components/data_ingestion.py`
- **Function**: Retrieves data from MongoDB, performs stratified train-test split
- **Output**: CSV files for train and test sets

### Data Validation
- **File**: `networksecurity/components/data_validation.py`
- **Function**: Validates data against schema, generates drift reports
- **Output**: Validation reports and drift analysis

### Data Transformation
- **File**: `networksecurity/components/data_transformation.py`
- **Function**: Feature scaling, normalization, and preprocessing
- **Output**: NumPy arrays for model training

### Model Trainer
- **File**: `networksecurity/components/model_trainer.py`
- **Function**: Trains multiple models, evaluates performance, selects best model
- **Output**: Trained model pickle file and performance metrics

## Requirements

Key dependencies:
- `pandas` - Data manipulation
- `numpy` - Numerical computing
- `scikit-learn` - Machine learning algorithms
- `pymongo` - MongoDB connectivity
- `mlflow` - Experiment tracking
- `fastapi` - REST API framework
- `uvicorn` - ASGI server
- `python-dotenv` - Environment variable management
- `pyaml` - YAML parsing
- `dagshub` - Model versioning

See [requirements.txt](requirements.txt) for complete list with versions.

## Example Output

After running `main.py`, artifacts are timestamped in the `Artifacts/` directory:

```
Artifacts/
└── 04_06_2026_21_32_25/
    ├── data_ingestion/
    │   └── feature_store/
    │       └── phishingData.csv
    ├── Data_validation/
    │   ├── validated/
    │   └── drift_report/
    ├── Data_transformation/
    │   └── transformed/
    └── model_trainer/
        └── trained_model/
```

## API Deployment

To run the FastAPI server for model serving:

```bash
uvicorn main:app --reload
```

Access the API documentation at `http://localhost:8000/docs`

## Docker

Build and run the Docker container:

```bash
docker build -t network-security .
docker run -p 8000:8000 network-security
```

## Logging

Logs are stored in the `logs/` directory with timestamps. Check logs for debugging and monitoring:

```bash
tail -f logs/application.log
```

## Best Practices

- Always activate the virtual environment before development
- Keep `.env` file secure and never commit it
- Review drift reports regularly
- Monitor MLflow experiments at `/mlruns`
- Update requirements.txt after adding new dependencies: `pip freeze > requirements.txt`

## Troubleshooting

**MongoDB Connection Issues**
- Verify MONGO_DB_URL in `.env` file
- Check network connectivity and firewall rules
- Run `python test_mongodb.py` to test connection

**Data Validation Failures**
- Check `data_schema/schema.yaml` matches your data
- Review drift reports in `Artifacts/*/Data_validation/drift_report/`

**Model Training Errors**
- Ensure data transformation artifacts exist
- Check available memory for model training
- Review logs in `logs/` directory

## Performance Monitoring

Track experiment metrics using MLflow:

```bash
mlflow ui
```

Access at `http://localhost:5000`

## Contributing

1. Create a new branch for features
2. Follow the existing code structure
3. Add comprehensive logging
4. Update README for significant changes

## Author

**Kumudini Bugde**
- Email: kumudinibugde@gmail.com

## License

[Add your license here]

## Version

Current Version: 0.0.1

---

**Last Updated**: April 2026