from sqlalchemy.orm import Session

from app.models.transaction import Transaction
from app.models.user import User
from app.schemas.admin import DashboardResponse


class AdminService:
    @staticmethod
    def dashboard(db: Session) -> DashboardResponse:
        total = db.query(Transaction).count()
        completed = db.query(Transaction).filter(Transaction.status == "COMPLETED").count()
        flagged = db.query(Transaction).filter(Transaction.status.in_(["PENDING_OTP", "BLOCKED"])).count()

        return DashboardResponse(
            total_transactions=total,
            fraud_count=flagged,
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
    def block_user(db: Session, user_id: int, blocked: bool) -> None:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")
        user.is_blocked = blocked
        db.add(user)
        db.commit()
