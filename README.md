# MulitModel-fraud-detection


Build a full-stack "Explainable AI-Driven Secure Multi-Model Financial Fraud Detection System".

Tech Stack:
- Backend: Java Spring Boot
- Frontend: React (optional basic UI)
- Database: MySQL
- ML Models: Python (XGBoost, Random Forest, Isolation Forest)
- Integration: REST APIs

----------------------------------------
CORE MODULES
----------------------------------------

1. USER MODULE:
- User registration and login
- First login requires PIN setup
- Store hashed PIN securely
- Allow multiple users in system
- Maintain wallet/account balance

2. TRANSACTION MODULE:
- Support 3 transaction types:
  - UPI
  - CARD
  - ACCOUNT TRANSFER
- Before transaction:
  - Validate PIN
  - Collect transaction-specific details
- Perform money transfer between users
- Store transaction history

3. FRAUD DETECTION MODULE:
- Use ML models:
  - XGBoost (supervised)
  - Random Forest (supervised)
  - Isolation Forest (unsupervised)
- Train using PaySim dataset
- Perform feature engineering:
  - hour = step % 24
  - is_new_beneficiary
  - amount_deviation
  - balance_error
- Output fraud probability score (0–1)

4. RISK ENGINE:
- Define risk levels:
  - LOW (<0.3)
  - MEDIUM (0.3–0.7)
  - HIGH (>0.7)
- Combine:
  - ML prediction
  - Rule-based checks:
    - high amount
    - new beneficiary
    - abnormal behavior

5. OTP VERIFICATION MODULE:
- If risk is MEDIUM or HIGH:
  - Generate 6-digit OTP
  - Store OTP with expiry (5 minutes)
  - Send OTP (mock or console log)
- Verify OTP before completing transaction

6. EXPLAINABLE AI MODULE:
- Provide reasons for fraud detection:
  - High amount
  - New beneficiary
  - Unusual transaction pattern
- (Optional) Integrate SHAP for feature importance

7. ADMIN MODULE:
- Dashboard with:
  - Total transactions
  - Fraud vs legit count
  - Flagged transactions
- User management:
  - Block/unblock users
- View transaction logs
- Override fraud decisions

----------------------------------------
DATABASE TABLES
----------------------------------------

Users:
- id, name, email, phone, password, pin_hash, balance

Transactions:
- id, sender_id, receiver_id, amount, type, risk_score, status, timestamp

OTP:
- id, user_id, otp, expiry_time

----------------------------------------
API ENDPOINTS
----------------------------------------

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

----------------------------------------
WORKFLOW
----------------------------------------

1. User initiates transaction
2. Validate PIN
3. Extract features
4. Call ML model API
5. Get fraud probability
6. Apply risk rules
7. If LOW → complete transaction
8. If MEDIUM/HIGH → trigger OTP
9. Verify OTP
10. Complete or block transaction

----------------------------------------
EXTRA REQUIREMENTS
----------------------------------------

- Use clean architecture (Controller, Service, Repository)
- Use DTOs for request/response
- Use proper exception handling
- Log all transactions
- Ensure secure coding practices

----------------------------------------
OUTPUT EXPECTATION
----------------------------------------

Generate:
- Spring Boot backend structure
- REST APIs implementation
- OTP service
- Fraud detection integration logic
- Sample ML model API (Python FastAPI)
- Example feature engineering code

----------------------------------------
IMPLEMENTATION STATUS
----------------------------------------

Part 1 completed:
- Backend folder scaffold created (clean architecture package layout)
- Spring Boot baseline project files added
- MySQL schema baseline added
- Python FastAPI ML skeleton created
- Feature engineering placeholder code added

Part 2 completed:
- User auth APIs implemented: /register, /login, /set-pin
- Transaction APIs implemented: /transfer, /verify-otp
- Admin APIs implemented: /dashboard, /transactions, /block-user
- JWT auth, PIN validation, OTP generation/verification flow integrated
- ML client integration scaffolded with fallback behavior

Planned next:
- Part 3: Backend-ML integration and risk scoring contract
- Part 4: OTP + risk engine orchestration
- Part 5: PaySim training pipeline completion after dataset upload
- Part 6: Admin module and hardening

----------------------------------------
PROJECT STRUCTURE (CURRENT)
----------------------------------------

- backend
  - src/main/java/com/frauddetection
    - auth, transaction, fraud, otp, admin
    - common, config, exception
  - src/main/resources/application.yml
  - pom.xml
- ml-service
  - main.py
  - app/api
  - app/ml
  - app/training
  - requirements.txt
- database
  - schema.sql

----------------------------------------
QUICK START (PART 1 BASELINE)
----------------------------------------

1. Backend prerequisites:
   - Java 17+
   - Maven 3.9+
   - MySQL running with database fraud_detection

2. Backend run:
   - cd backend
   - mvn spring-boot:run

3. ML service run:
   - cd ml-service
   - python -m venv .venv
   - source .venv/bin/activate
   - pip install -r requirements.txt
   - uvicorn main:app --host 0.0.0.0 --port 8001 --reload

4. ML health endpoint:
   - GET /api/v1/health

5. Implemented API endpoints in backend:
  - POST /register
  - POST /login
  - POST /set-pin
  - POST /transfer
  - POST /verify-otp
  - GET /dashboard
  - GET /transactions
  - POST /block-user

Note:
- PaySim dataset integration is intentionally deferred to Part 5.