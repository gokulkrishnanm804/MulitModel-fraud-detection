from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import verify_value
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

        payload = {
            "step": request.step,
            "amount": request.amount,
            "oldbalanceOrig": request.oldbalanceOrig if request.oldbalanceOrig is not None else float(current_user.balance),
            "newbalanceOrig": request.newbalanceOrig if request.newbalanceOrig is not None else float(current_user.balance) - request.amount,
            "oldbalanceDest": request.oldbalanceDest if request.oldbalanceDest is not None else float(receiver.balance),
            "newbalanceDest": request.newbalanceDest if request.newbalanceDest is not None else float(receiver.balance) + request.amount,
            "is_new_beneficiary": request.is_new_beneficiary,
        }

        score = MlService.score(payload)

        reasons = score.get("reasons", [])
        if request.amount >= settings.high_amount_threshold:
            reasons.append("High amount")
        if request.is_new_beneficiary == 1:
            reasons.append("New beneficiary")

        risk_score = float(score["risk_score"])
        risk_level = score["risk_level"]

        tx = Transaction(
            sender_id=current_user.id,
            receiver_id=receiver.id,
            amount=request.amount,
            type=request.type,
            risk_score=risk_score,
            status="PENDING_OTP" if risk_level in {"MEDIUM", "HIGH"} else "COMPLETED",
            reason=", ".join(dict.fromkeys(reasons)) if reasons else None,
        )
        db.add(tx)
        db.commit()
        db.refresh(tx)

        if tx.status == "COMPLETED":
            current_user.balance = float(current_user.balance) - request.amount
            receiver.balance = float(receiver.balance) + request.amount
            db.add(current_user)
            db.add(receiver)
            db.commit()
            msg = "Transaction completed"
        else:
            OtpService.generate_otp(db, current_user.id, tx.id)
            msg = "OTP required to complete transaction"

        return TransferResponse(
            transaction_id=tx.id,
            status=tx.status,
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
        if tx.status != "PENDING_OTP":
            raise ValueError("Transaction is not pending OTP")

        if not OtpService.verify_otp(db, current_user.id, tx.id, request.otp):
            raise ValueError("Invalid or expired OTP")

        sender = db.query(User).filter(User.id == tx.sender_id).first()
        receiver = db.query(User).filter(User.id == tx.receiver_id).first()

        if not sender or not receiver:
            raise ValueError("User record missing")
        if sender.balance < tx.amount:
            raise ValueError("Insufficient balance")

        sender.balance = float(sender.balance) - float(tx.amount)
        receiver.balance = float(receiver.balance) + float(tx.amount)
        tx.status = "COMPLETED"

        db.add(sender)
        db.add(receiver)
        db.add(tx)
        db.commit()

        return TransferResponse(
            transaction_id=tx.id,
            status=tx.status,
            risk_score=float(tx.risk_score),
            risk_level="MEDIUM" if float(tx.risk_score) <= 0.7 else "HIGH",
            message="Transaction completed after OTP verification",
            reasons=[tx.reason] if tx.reason else [],
        )
