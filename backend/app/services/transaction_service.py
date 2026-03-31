from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import verify_value
from app.models.beneficiary import Beneficiary
from app.models.fraud_log import FraudLog
from app.models.transaction import Transaction
from app.models.user import User
from app.schemas.transaction import TransferRequest, TransferResponse, VerifyOtpRequest
from app.services.ml_service import MlService
from app.services.otp_service import OtpService


class TransactionService:
    @staticmethod
    def transfer(db: Session, current_user: User, request: TransferRequest) -> TransferResponse:
        receiver = db.query(User).filter(User.id == request.receiver_id).first()
        if not receiver:
            raise ValueError("Receiver not found")

        if current_user.balance < request.amount:
            raise ValueError("Insufficient balance")

        if not current_user.pin_hash or not verify_value(request.pin, current_user.pin_hash):
            raise ValueError("Invalid PIN")

        beneficiary_exists = (
            db.query(Beneficiary)
            .filter(Beneficiary.user_id == current_user.id, Beneficiary.beneficiary_id == receiver.id)
            .first()
            is not None
        )
        is_new_beneficiary = 0 if beneficiary_exists else 1

        payload = {
            "step": request.step,
            "amount": request.amount,
            "oldbalanceOrig": request.oldbalanceOrig if request.oldbalanceOrig is not None else float(current_user.balance),
            "newbalanceOrig": request.newbalanceOrig if request.newbalanceOrig is not None else float(current_user.balance) - request.amount,
            "oldbalanceDest": request.oldbalanceDest if request.oldbalanceDest is not None else float(receiver.balance),
            "newbalanceDest": request.newbalanceDest if request.newbalanceDest is not None else float(receiver.balance) + request.amount,
            "is_new_beneficiary": is_new_beneficiary,
        }

        score = MlService.score(payload)

        reasons = list(score.get("reasons", []))
        if request.amount >= settings.high_amount_threshold:
            reasons.append("High amount")
        if is_new_beneficiary == 1:
            reasons.append("New beneficiary")

        risk_score = float(score.get("risk_score", 0.0))
        if request.amount >= settings.high_amount_threshold and is_new_beneficiary == 1:
            risk_score = max(risk_score, 0.85)

        if risk_score < 0.3:
            risk_level = "LOW"
        elif risk_score <= 0.7:
            risk_level = "MEDIUM"
        else:
            risk_level = "HIGH"

        tx = Transaction(
            sender_id=current_user.id,
            receiver_id=receiver.id,
            amount=request.amount,
            type=request.type,
            risk_score=risk_score,
            status="PENDING" if risk_level in {"MEDIUM", "HIGH"} else "SUCCESS",
            reason=", ".join(dict.fromkeys(reasons)) if reasons else None,
        )
        db.add(tx)
        db.commit()
        db.refresh(tx)

        fraud_log = FraudLog(
            transaction_id=tx.id,
            risk_score=risk_score,
            reasons=tx.reason,
        )
        db.add(fraud_log)
        db.commit()

        if tx.status == "SUCCESS":
            current_user.balance = float(current_user.balance) - request.amount
            receiver.balance = float(receiver.balance) + request.amount
            db.add(current_user)
            db.add(receiver)
            db.commit()
            if is_new_beneficiary == 1:
                db.add(Beneficiary(user_id=current_user.id, beneficiary_id=receiver.id))
                db.commit()
            msg = "Transaction completed"
        else:
            OtpService.generate_otp(db, current_user.id, tx.id)
            msg = "OTP required to complete transaction"

        return TransferResponse(
            transaction_id=tx.id,
            status="OTP_REQUIRED" if tx.status == "PENDING" else tx.status,
            risk_score=risk_score,
            risk_level=risk_level,
            message=msg,
            reasons=list(dict.fromkeys(reasons)),
        )

    @staticmethod
    def verify_otp(db: Session, current_user: User, request: VerifyOtpRequest) -> TransferResponse:
        tx = db.query(Transaction).filter(Transaction.id == request.transaction_id).first()
        if not tx:
            raise ValueError("Transaction not found")
        if tx.sender_id != current_user.id:
            raise ValueError("Unauthorized transaction")
        if tx.status != "PENDING":
            raise ValueError("Transaction is not pending OTP")

        otp_ok, _ = OtpService.verify_otp(db, current_user.id, tx.id, request.otp)
        if not otp_ok:
            tx.status = "FAILED"
            db.add(tx)
            db.commit()
            raise ValueError("Invalid or expired OTP")

        sender = db.query(User).filter(User.id == tx.sender_id).first()
        receiver = db.query(User).filter(User.id == tx.receiver_id).first()

        if not sender or not receiver:
            raise ValueError("User record missing")
        if sender.balance < tx.amount:
            raise ValueError("Insufficient balance")

        sender.balance = float(sender.balance) - float(tx.amount)
        receiver.balance = float(receiver.balance) + float(tx.amount)
        tx.status = "SUCCESS"

        beneficiary_exists = (
            db.query(Beneficiary)
            .filter(Beneficiary.user_id == sender.id, Beneficiary.beneficiary_id == receiver.id)
            .first()
            is not None
        )
        if not beneficiary_exists:
            db.add(Beneficiary(user_id=sender.id, beneficiary_id=receiver.id))

        db.add(sender)
        db.add(receiver)
        db.add(tx)
        db.commit()

        if float(tx.risk_score) < 0.3:
            risk_level = "LOW"
        elif float(tx.risk_score) <= 0.7:
            risk_level = "MEDIUM"
        else:
            risk_level = "HIGH"

        return TransferResponse(
            transaction_id=tx.id,
            status=tx.status,
            risk_score=float(tx.risk_score),
            risk_level=risk_level,
            message="Transaction completed after OTP verification",
            reasons=[tx.reason] if tx.reason else [],
        )
