# MulitModel-fraud-detection

Full-stack Explainable AI-Driven Secure Multi-Model Financial Fraud Detection System.

## Current Stack
- Backend: Python FastAPI
- Frontend: React (Vite)
- Database: MySQL
- ML Service: Python FastAPI (XGBoost, Random Forest, Isolation Forest)

## Backend Note
- Active backend is the `backend` folder (FastAPI).

## Implemented API Endpoints

Auth:
- POST /register
- POST /login
- POST /set-pin

Transaction:
- POST /transfer
- POST /verify-otp

Admin:
- GET /dashboard
- GET /transactions
- POST /block-user

Health:
- GET /health

## Process Split (Phased)

Part 1 completed:
- Python backend scaffold with clean modules
- React frontend scaffold
- MySQL schema baseline

Part 2 completed:
- JWT auth flow + PIN setup
- Transfer flow + risk scoring call to ML service
- OTP generation and verification flow
- Admin endpoints for dashboard, transactions, and block/unblock

Part 3 (next):
- Upgrade risk engine and explainable decision responses
- Add stricter per-type transaction validation rules

Part 4 (after PaySim upload):
- Train XGBoost, Random Forest, Isolation Forest on PaySim
- Replace placeholder ML scoring with model artifacts

## Project Structure

- backend (FastAPI backend)
- ml-service (ML FastAPI service)
- frontend (React Vite app)
- database/schema.sql

## Run Instructions

1. Database
- Start MySQL and create database `fraud_detection`.
- Run `database/schema.sql`.

2. Backend (FastAPI)
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

3. ML Service (FastAPI)
```bash
cd ml-service
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

4. Frontend (React)
```bash
cd frontend
npm install
npm run dev
```

## PaySim Dataset Timing

Upload PaySim later as planned. Once uploaded, training implementation will be completed in `ml-service/app/training/train_models.py` and the inference code will be switched from placeholder scoring to trained model artifacts.