# MulitModel-fraud-detection

Build a full-stack project titled:

"Explainable AI-Driven Secure Multi-Model Financial Fraud Detection System"

----------------------------------------
TECH STACK
----------------------------------------
Frontend:
- React (Vite)
- Axios
- React Router
- Context API
- Tailwind CSS (optional)

Backend:
- Python FastAPI
- SQLAlchemy ORM
- JWT Authentication
- bcrypt for password and PIN hashing

Database:
- MySQL

Machine Learning:
- XGBoost (Supervised)
- Random Forest (Supervised)
- Isolation Forest (Unsupervised)
- Dataset: PaySim

----------------------------------------
PROJECT REQUIREMENTS
----------------------------------------

USER MODULE:
- Register and login users (JWT authentication)
- First login must require setting a 4-digit transaction PIN
- Store hashed password and PIN
- Maintain user balance
- Allow multiple users

TRANSACTION MODULE:
- Users can send money to other users
- Support 3 transaction types:
  - UPI
  - CARD
  - ACCOUNT TRANSFER
- Before transaction:
  - Validate PIN
  - Accept required details
- Update balances after transaction
- Store all transaction records

FRAUD DETECTION MODULE:
- Train models using PaySim dataset
- Perform feature engineering:
  - hour = step % 24
  - is_new_beneficiary (based on past transactions)
  - amount_deviation (compare with avg user amount)
  - balance_error = oldbalanceOrg - amount - newbalanceOrig
- Use:
  - XGBoost
  - Random Forest
  - Isolation Forest
- Output fraud probability (0–1)

RISK ENGINE:
- Define risk levels:
  - LOW (<0.3)
  - MEDIUM (0.3–0.7)
  - HIGH (>0.7)
- Combine:
  - ML prediction
  - Rule-based checks:
    - High amount
    - New beneficiary
    - Unusual transaction pattern

OTP VERIFICATION:
- If risk is MEDIUM or HIGH:
  - Generate 6-digit OTP
  - Store OTP in database with expiry (5 minutes)
  - Simulate sending OTP (console/log)
- Verify OTP before completing transaction
- If OTP correct → SUCCESS
- If OTP wrong/expired → FAILED

EXPLAINABLE AI:
- Provide reasons for fraud detection:
  - High amount
  - New beneficiary
  - Unusual behavior
- Return reasons to frontend
- (Optional) Use SHAP for feature importance

ADMIN MODULE:
- View all users
- View all transactions
- View fraud transactions (risk_score > 0.7)
- Block/unblock users
- View fraud logs and reasons

----------------------------------------
DATABASE DESIGN (MYSQL)
----------------------------------------

Users:
- id, name, email, phone, password_hash, pin_hash, balance, is_blocked, created_at

Transactions:
- id, sender_id, receiver_id, amount, type, risk_score, status (PENDING, SUCCESS, FAILED), reason, created_at

OTP:
- id, user_id, otp_code, expiry_time, is_verified

Fraud Logs:
- id, transaction_id, risk_score, reasons, created_at

Beneficiaries:
- id, user_id, beneficiary_id

----------------------------------------
BACKEND (FASTAPI)
----------------------------------------

- Use modular structure:
  - routers/
  - models/
  - schemas/
  - services/
  - utils/

- Implement APIs:

Auth:
- POST /register
- POST /login
- POST /set-pin

Transaction:
- POST /transfer
- POST /verify-otp

Admin:
- GET /admin/users
- GET /admin/transactions
- POST /admin/block-user

----------------------------------------
TRANSACTION WORKFLOW
----------------------------------------

1. User logs in
2. User initiates transfer
3. Validate PIN
4. Perform feature engineering
5. Call ML models
6. Get fraud probability
7. Apply risk rules

IF LOW RISK:
→ Complete transaction immediately

IF MEDIUM/HIGH RISK:
→ Generate OTP
→ Ask user to verify

IF OTP SUCCESS:
→ Complete transaction

IF OTP FAIL:
→ Reject transaction

----------------------------------------
FRONTEND (REACT)
----------------------------------------

Pages:
- /login
- /register
- /dashboard
- /transfer
- /otp
- /admin

Features:
- Login/Register UI
- Dashboard showing balance
- Transfer form (receiver, amount, type, PIN)
- OTP verification screen
- Transaction result screen
- Show fraud explanation (reasons)
- Admin dashboard (users + transactions)

----------------------------------------
API INTEGRATION
----------------------------------------

Use Axios:
- Attach JWT token in headers
- Handle responses:
  - SUCCESS
  - OTP_REQUIRED
  - FAILED

----------------------------------------
EXPECTED OUTPUT
----------------------------------------

Generate:
- FastAPI backend (complete structure)
- MySQL schema and SQLAlchemy models
- ML training code (PaySim dataset)
- Fraud detection service
- OTP service
- React frontend with all pages
- API integration between frontend and backend

----------------------------------------
SPECIAL REQUIREMENT
----------------------------------------

IMPORTANT SCENARIO:
If a user sends a high amount to a new beneficiary from a new pattern (like emergency case):

- DO NOT directly block transaction
- Mark as HIGH RISK
- Trigger OTP verification
- Allow transaction if OTP is verified

----------------------------------------
GOAL
----------------------------------------

Build a real-world financial fraud detection system that:
- Uses machine learning + rule-based logic
- Provides explainable AI output
- Uses OTP for secure verification instead of blocking legitimate users