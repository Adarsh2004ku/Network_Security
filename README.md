<<<<<<< HEAD
# Network Security

A machine learning-based network security system for detecting anomalies and threats in network traffic data. This project implements a complete MLOps pipeline from data ingestion to model deployment using MongoDB for data storage and Docker for containerization.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Components](#components)
- [Contributing](#contributing)

---

## Overview

This project provides an end-to-end solution for network security monitoring using machine learning. It processes network traffic data, trains models to detect anomalies, and provides predictions on potential security threats.

**Key Technologies:**
- Python 3.8+
- MongoDB (NoSQL Database)
- Docker (Containerization)
- GitHub Actions (CI/CD)
- Machine Learning (Scikit-learn/TensorFlow)

---

## Features

- **Data Ingestion**: Automated data collection from network sources and storage in MongoDB
- **Data Validation**: Schema-based validation to ensure data quality
- **Data Transformation**: Feature engineering and preprocessing pipeline
- **Model Training**: Training ML models for anomaly detection
- **Model Evaluation**: Performance metrics and model selection
- **Logging**: Comprehensive logging for debugging and monitoring
- **Docker Support**: Containerized application for easy deployment
- **CI/CD Pipeline**: Automated workflows using GitHub Actions

---

## Project Structure

```
Network_Security/
│
├── networksecurity/              # Main application package
│   ├── components/               # Core components
│   │   ├── data_ingestion.py
│   │   ├── data_validation.py
│   │   ├── data_transformation.py
│   │   └── model_trainer.py
│   ├── entity/                   # Configuration entities
│   │   ├── config_entity.py
│   │   └── artifact_entity.py
│   ├── pipeline/                 # Training pipeline
│   │   └── training_pipeline.py
│   ├── utils/                    # Utility functions
│   └── constants/                # Application constants
│
├── Network_Data/                 # Network dataset storage
├── Artifacts/                    # Training artifacts
│   ├── data_ingestion/
│   ├── data_validation/
│   ├── data_transformation/
│   └── model_trainer/
│
├── final_model/                  # Production-ready models
├── data_schema/                  # Data validation schemas
├── logs/                         # Application logs
│
├── .github/workflows/            # CI/CD configurations
├── main.py                       # Application entry point
├── push_data.py                  # Data ingestion script
├── test_mongo_db.py             # MongoDB connection test
├── setup.py                      # Package setup
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Docker configuration
└── .gitignore                    # Git ignore rules
```

---

## Prerequisites

- Python 3.8 or higher
- MongoDB 4.0 or higher
- Docker (optional, for containerized deployment)
- pip (Python package manager)

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Adarsh2004ku/Network_Security.git
cd Network_Security
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Package in Development Mode

```bash
pip install -e .
```

---

## Configuration

### MongoDB Setup

1. Install MongoDB on your system or use MongoDB Atlas (cloud)
2. Create a `.env` file in the root directory:

```env
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=network_security
COLLECTION_NAME=network_data
```

### Test MongoDB Connection

```bash
python test_mongo_db.py
```

If the connection is successful, you should see a confirmation message.

---

## Usage

### 1. Push Data to MongoDB

Load your network data into MongoDB:

```bash
python push_data.py
```

### 2. Train the Model

Run the complete training pipeline:

```bash
python main.py
```

This will execute:
- Data ingestion from MongoDB
- Data validation against schema
- Data transformation and feature engineering
- Model training and evaluation
- Model artifact storage

### 3. Run with Docker

Build and run the application using Docker:

```bash
# Build Docker image
docker build -t network-security:latest .

# Run container
docker run -p 8000:8000 network-security:latest
```

---

## Components

### 1. Data Ingestion (`data_ingestion.py`)

- Connects to MongoDB database
- Retrieves network traffic data
- Splits data into training and testing sets
- Stores data in the feature store

**Output**: Raw data artifacts in `Artifacts/data_ingestion/`

### 2. Data Validation (`data_validation.py`)

- Validates data against predefined schema
- Checks for missing values and data types
- Detects data drift
- Generates validation reports

**Output**: Validation reports in `Artifacts/data_validation/`

### 3. Data Transformation (`data_transformation.py`)

- Handles missing values
- Encodes categorical features
- Scales numerical features
- Creates feature engineering pipeline
- Transforms data for model training

**Output**: Preprocessed data and transformer objects in `Artifacts/data_transformation/`

### 4. Model Training (`model_trainer.py`)

- Trains multiple ML models
- Performs hyperparameter tuning
- Evaluates model performance
- Selects the best performing model
- Saves model artifacts

**Output**: Trained models in `Artifacts/model_trainer/` and `final_model/`

### 5. Training Pipeline (`training_pipeline.py`)

Orchestrates the entire training workflow by executing all components in sequence:

```
Data Ingestion → Data Validation → Data Transformation → Model Training
```

---

## Logging

All operations are logged to the `logs/` directory with timestamps. Log files contain:
- Component execution status
- Error messages and stack traces
- Data processing information
- Model training metrics

---

## CI/CD Pipeline

The project uses GitHub Actions for automated workflows defined in `.github/workflows/`:

- **Continuous Integration**: Automatic testing on code push
- **Continuous Deployment**: Automated Docker image builds
- **Code Quality Checks**: Linting and formatting validation

---

## Data Schema

The `data_schema/` directory contains JSON schema definitions for:
- Input data validation
- Feature names and types
- Expected data ranges
- Missing value handling rules

Ensure your network data conforms to the schema before training.

---

## Artifacts

Training artifacts are stored in the `Artifacts/` directory with timestamp-based organization:

```
Artifacts/
├── <timestamp>/
│   ├── data_ingestion/
│   │   ├── feature_store/
│   │   └── ingested/
│   ├── data_validation/
│   │   └── report/
│   ├── data_transformation/
│   │   └── transformed/
│   └── model_trainer/
│       └── model/
```

---

## Model Files

Final production-ready models are saved in:
- `final_model/` - Best performing model
- Includes model file, preprocessor, and metadata

---

## Troubleshooting

### MongoDB Connection Issues

```bash
# Check if MongoDB is running
sudo systemctl status mongod

# Start MongoDB service
sudo systemctl start mongod
```

### Import Errors

```bash
# Reinstall the package
pip install -e .
```

### Docker Issues

```bash
# Check Docker status
docker --version

# View running containers
docker ps

# View logs
docker logs <container_id>
```

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add YourFeature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

### Code Style

- Follow PEP 8 guidelines
- Add docstrings to functions and classes
- Write unit tests for new features
- Update documentation as needed

---

- Repository: [Network_Security](https://github.com/Adarsh2004ku/Network_Security)

---

## Acknowledgments

- Built with modern MLOps practices
- Uses industry-standard tools and libraries
- Inspired by network security research and best practices
=======
>>>>>>> fab2362 (mlflow integrated)
