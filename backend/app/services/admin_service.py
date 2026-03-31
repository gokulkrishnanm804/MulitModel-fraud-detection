from sqlalchemy.orm import Session

from app.models.fraud_log import FraudLog
from app.models.transaction import Transaction
from app.models.user import User
from app.schemas.admin import DashboardResponse


class AdminService:
    @staticmethod
    def dashboard(db: Session) -> DashboardResponse:
        total = db.query(Transaction).count()
        completed = db.query(Transaction).filter(Transaction.status == "SUCCESS").count()
        flagged = db.query(Transaction).filter(Transaction.status == "PENDING").count()
        fraud_count = db.query(Transaction).filter(Transaction.risk_score > 0.7).count()

        return DashboardResponse(
            total_transactions=total,
            fraud_count=fraud_count,
            legit_count=completed,
            flagged_transactions=flagged,
        )

    @staticmethod
    def recent_transactions(db: Session) -> list[dict]:
        rows = db.query(Transaction).order_by(Transaction.created_at.desc()).limit(100).all()
        result = []
        for tx in rows:
            result.append(
                {
                    "id": tx.id,
                    "sender_id": tx.sender_id,
                    "receiver_id": tx.receiver_id,
                    "amount": float(tx.amount),
                    "type": tx.type,
                    "risk_score": float(tx.risk_score),
                    "status": tx.status,
                    "reason": tx.reason,
                    "created_at": tx.created_at.isoformat() if tx.created_at else None,
                }
            )
        return result

    @staticmethod
    def list_users(db: Session) -> list[dict]:
        rows = db.query(User).order_by(User.created_at.desc()).all()
        result = []
        for user in rows:
            result.append(
                {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "phone": user.phone,
                    "role": user.role,
                    "balance": float(user.balance),
                    "is_blocked": user.is_blocked,
                    "created_at": user.created_at.isoformat() if user.created_at else None,
                }
            )
        return result

    @staticmethod
    def fraud_transactions(db: Session) -> list[dict]:
        rows = db.query(Transaction).filter(Transaction.risk_score > 0.7).order_by(Transaction.created_at.desc()).all()
        result = []
        for tx in rows:
            result.append(
                {
                    "id": tx.id,
                    "sender_id": tx.sender_id,
                    "receiver_id": tx.receiver_id,
                    "amount": float(tx.amount),
                    "type": tx.type,
                    "risk_score": float(tx.risk_score),
                    "status": tx.status,
                    "reason": tx.reason,
                    "created_at": tx.created_at.isoformat() if tx.created_at else None,
                }
            )
        return result

    @staticmethod
    def fraud_logs(db: Session) -> list[dict]:
        rows = db.query(FraudLog).order_by(FraudLog.created_at.desc()).limit(200).all()
        result = []
        for log in rows:
            result.append(
                {
                    "id": log.id,
                    "transaction_id": log.transaction_id,
                    "risk_score": float(log.risk_score),
                    "reasons": log.reasons,
                    "created_at": log.created_at.isoformat() if log.created_at else None,
                }
            )
        return result

    @staticmethod
    def block_user(db: Session, user_id: int, blocked: bool) -> None:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")
        user.is_blocked = blocked
        db.add(user)
        db.commit()
