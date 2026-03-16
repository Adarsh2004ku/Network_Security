# 🔐 Network Security — End-to-End MLOps Phishing Detection System

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python&logoColor=white)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ML-orange?logo=scikit-learn&logoColor=white)
![MLflow](https://img.shields.io/badge/MLflow-Tracking-0194E2?logo=mlflow&logoColor=white)
![DagsHub](https://img.shields.io/badge/DagsHub-Experiment%20Tracking-orange)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-REST%20API-009688?logo=fastapi&logoColor=white)
![AWS ECR](https://img.shields.io/badge/AWS%20ECR-Registry-FF9900?logo=amazonaws&logoColor=white)
![AWS EC2](https://img.shields.io/badge/AWS%20EC2-Deployed-FF9900?logo=amazonaws&logoColor=white)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF?logo=githubactions&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-47A248?logo=mongodb&logoColor=white)

A **production-grade, end-to-end MLOps system** for detecting phishing websites with >99% accuracy. Built on the UCI Phishing Websites Dataset (11,055 records, 30 features), this project covers the full ML lifecycle — from automated data ingestion from MongoDB Atlas, through a five-stage training pipeline with MLflow experiment tracking, to a live FastAPI REST API deployed on AWS EC2 via Docker and GitHub Actions CI/CD.

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Architecture](#-architecture)
- [Pipeline Stages](#-pipeline-stages)
- [Dataset](#-dataset)
- [Model Performance](#-model-performance)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Setup & Installation](#-setup--installation)
- [Running the Pipeline](#-running-the-pipeline)
- [API Usage](#-api-usage)
- [CI/CD Deployment](#-cicd-deployment)
- [MLflow Experiment Tracking](#-mlflow-experiment-tracking)

---

## 🧠 Overview

Phishing attacks account for over **80% of reported security incidents** globally. Traditional rule-based detection systems fail against modern phishing campaigns that rotate domains and use HTTPS certificates to appear legitimate.

This system applies **MLOps best practices** to solve the problem at scale:
- ✅ Fully automated pipeline — raw MongoDB data → live prediction API
- ✅ Schema validation guards against data drift
- ✅ KNN imputation + StandardScaler preprocessing serialised for inference parity
- ✅ Multi-model training with F1-score gated model promotion
- ✅ Full experiment tracking via MLflow + DagsHub
- ✅ Dockerised deployment with GitHub Actions CI/CD to AWS ECR + EC2

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        DATA LAYER                                   │
│   MongoDB Atlas  ──► push_data.py  ──► phishing_data collection     │
└─────────────────────────┬───────────────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────────────┐
│                      PIPELINE LAYER                                 │
│                                                                     │
│  DataIngestion → DataValidation → DataTransformation →              │
│  ModelTrainer  → ModelEvaluation                                    │
│                                                                     │
│  (All stages produce typed Artifact dataclasses)                    │
└─────────────────────────┬───────────────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────────────┐
│                      SERVING LAYER                                  │
│   FastAPI  ──►  /train  |  /predict                                 │
│   model.pkl + preprocessor.pkl loaded at startup                   │
└─────────────────────────┬───────────────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────────────┐
│                   INFRASTRUCTURE LAYER                              │
│   GitHub Actions CI/CD → Docker Build → AWS ECR → AWS EC2          │
└─────────────────────────────────────────────────────────────────────┘
```

---

## ⚙️ Pipeline Stages

### Stage 1 — Data Ingestion
- Connects to **MongoDB Atlas** via `MONGO_DB_URL` env variable
- Fetches all documents from `phishing_data` collection using PyMongo
- Performs stratified **80/20 train-test split**
- Outputs: `feature_store.csv`, `train.csv`, `test.csv` → `Artifacts/data_ingestion/`

### Stage 2 — Data Validation
- Validates column presence, count, and data types against `data_schema/schema.yaml`
- Checks missing value thresholds per column
- Runs **Kolmogorov-Smirnov drift detection** between train and test distributions
- Outputs: structured JSON validation report with `validation_status`, `drift_report`, `missing_values`

### Stage 3 — Data Transformation
- **KNN Imputation** (k=3) for missing numerical values — more accurate than mean/median
- **StandardScaler** — zero mean, unit variance normalisation
- Preprocessor is **fit only on training set** (no data leakage)
- Serialises `preprocessor.pkl` for identical inference-time transformations
- Outputs: transformed NumPy arrays → `Artifacts/data_transformation/`

### Stage 4 — Model Training
Models trained and compared:

| Model | Notes |
|---|---|
| Random Forest | Best balance of accuracy & speed |
| XGBoost | Highest AUC-ROC via gradient boosting |
| Logistic Regression | Interpretable baseline (~90–92% accuracy) |
| Decision Tree | Fast, explainable |
| AdaBoost | Ensemble boosting baseline |

- All runs logged to **MLflow + DagsHub** (params, metrics, artifacts, confusion matrix, ROC curve)
- Model selected only if **test F1-score > 0.60** threshold — prevents poor models reaching production
- Best model + preprocessor copied to `final_model/`

### Stage 5 — Model Serving (FastAPI)
- `POST /predict` — accepts CSV file, returns JSON array with `predicted_label` + `phishing_probability`
- `POST /train` — triggers full pipeline retraining on demand
- Swagger UI available at `/docs`

---

## 📊 Dataset

**UCI Phishing Websites Dataset** — 11,055 instances, 30 integer-encoded features + 1 binary label

| Feature | Description |
|---|---|
| `SSLfinal_State` | HTTPS certificate validity |
| `URL_of_Anchor` | Anchor href patterns |
| `web_traffic` | Site traffic rank |
| `having_Sub_Domain` | Subdomain count |
| `Request_URL` | External resource loading ratio |
| `Page_Rank` | Google PageRank authority |
| ... | 24 more URL/page behavioural features |

**Target:** `Result` — `1` (legitimate) / `0` (phishing)

All features are integer-encoded: `-1` (phishing indicator), `0` (suspicious), `1` (legitimate indicator).

---

## 📈 Model Performance

| Metric | Target | Achieved |
|---|---|---|
| Accuracy | >95% | **>99%** |
| F1-Score | >0.95 | **>0.97** |
| AUC-ROC | >0.95 | **>0.97** |
| Precision | >0.95 | ✅ |
| Recall | >0.95 | ✅ |

> Best performing model: **Random Forest / XGBoost** (ensemble tree methods outperform linear models on this feature set)

---

## 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10 |
| ML | Scikit-learn, XGBoost |
| Experiment Tracking | MLflow, DagsHub |
| Data Store | MongoDB Atlas (PyMongo) |
| API | FastAPI, Uvicorn |
| Containerisation | Docker |
| CI/CD | GitHub Actions |
| Cloud Registry | AWS ECR |
| Cloud Compute | AWS EC2 |
| Data Processing | Pandas, NumPy |

---

## 📁 Project Structure

```
Network_Security/
├── networksecurity/
│   ├── components/          # Pipeline stage implementations
│   │   ├── data_ingestion.py
│   │   ├── data_validation.py
│   │   ├── data_transformation.py
│   │   └── model_trainer.py
│   ├── entity/
│   │   ├── config_entity.py     # Config dataclasses per stage
│   │   └── artifact_entity.py   # Artifact dataclasses per stage
│   ├── exception/           # Custom NetworkSecurityException
│   ├── logging/             # Centralised structured logger
│   ├── pipeline/            # Training & prediction pipeline orchestrators
│   └── utils/               # Shared utilities
├── data_schema/
│   └── schema.yaml          # Column names, types, validation rules
├── final_model/             # Best model.pkl + preprocessor.pkl
├── Artifacts/               # Timestamped pipeline run outputs
├── .github/workflows/       # CI/CD pipeline definition
├── app.py                   # FastAPI application entry point
├── main.py                  # Training pipeline runner
├── push_data.py             # MongoDB data upload script
├── Dockerfile               # Production container definition
├── render.yaml / docker-compose.yml
├── requirements.txt
└── setup.py
```

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.10+
- MongoDB Atlas account
- AWS account (ECR + EC2) for deployment
- DagsHub account linked to this repository
- Docker Desktop (for local containerised testing)

### 1. Clone & Install

```bash
git clone https://github.com/Adarsh2004ku/Network_Security.git
cd Network_Security
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```env
MONGO_DB_URL=mongodb+srv://<user>:<password>@<cluster>.mongodb.net/
MLFLOW_TRACKING_URI=https://dagshub.com/<username>/Network_Security.mlflow
MLFLOW_TRACKING_USERNAME=<dagshub_username>
MLFLOW_TRACKING_PASSWORD=<dagshub_token>
```

---

## ▶️ Running the Pipeline

### Push data to MongoDB (one-time setup)
```bash
python push_data.py
```

### Run the full training pipeline
```bash
python main.py
```
This runs all 5 stages sequentially: Ingest → Validate → Transform → Train → Evaluate

### Start the FastAPI server locally
```bash
uvicorn app:app --host 0.0.0.0 --port 8080 --reload
```
Swagger UI: [http://localhost:8080/docs](http://localhost:8080/docs)

### Docker local testing
```bash
docker build -t networksecurity:latest .
docker run -d -p 8080:8080 --env-file .env networksecurity:latest
```

---

## 🌐 API Usage

### Predict (POST /predict)
```bash
curl -X POST http://localhost:8080/predict \
  -F "file=@sample_data.csv"
```

**Response:**
```json
[
  {
    "predicted_label": 0,
    "phishing_probability": 0.94
  },
  {
    "predicted_label": 1,
    "phishing_probability": 0.07
  }
]
```
`predicted_label`: `0` = phishing, `1` = legitimate

### Trigger Retraining (POST /train)
```bash
curl -X POST http://localhost:8080/train
```

---

## 🔄 CI/CD Deployment

The `.github/workflows/` pipeline runs on every push to `main`:

```
Push to main
    │
    ▼
Job 1: CI — lint (flake8) + unit tests (pytest)
    │
    ▼
Job 2: CD — Docker build → push to AWS ECR
    │
    ▼
Job 3: Deploy — EC2 self-hosted runner pulls image → restarts container
```

### Required GitHub Secrets

| Secret | Purpose |
|---|---|
| `AWS_ACCESS_KEY_ID` | AWS IAM credentials |
| `AWS_SECRET_ACCESS_KEY` | AWS IAM credentials |
| `AWS_REGION` | Target AWS region |
| `ECR_REPOSITORY_URI` | ECR image registry URL |
| `MONGO_DB_URL` | MongoDB Atlas connection string |
| `MLFLOW_TRACKING_URI` | DagsHub MLflow endpoint |
| `MLFLOW_TRACKING_USERNAME` | DagsHub username |
| `MLFLOW_TRACKING_PASSWORD` | DagsHub token |

---

## 📊 MLflow Experiment Tracking

Every training run logs to DagsHub:
- **Parameters** — all hyperparameter values
- **Metrics** — accuracy, precision, recall, F1, AUC-ROC (train + test)
- **Artifacts** — model pickle, confusion matrix plot, ROC curve
- **Tags** — model name, pipeline timestamp, library versions

View experiments at: `https://dagshub.com/Adarsh2004ku/Network_Security`

---

## 👤 Author

**Adarsh Kumar**
- GitHub: [@Adarsh2004ku](https://github.com/Adarsh2004ku)
- LinkedIn: [adarsh-kumar-714108314](https://www.linkedin.com/in/adarsh-kumar-714108314/)
- Portfolio: [View Portfolio](https://portfolio-five-roan-hettkeuqbc.vercel.app/)
