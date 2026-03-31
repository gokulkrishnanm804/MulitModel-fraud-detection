from datetime import datetime, timedelta
import random
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import hash_value, verify_value
from app.models.otp import OtpRecord


class OtpService:
    @staticmethod
    def generate_otp(db: Session, user_id: int, transaction_id: int) -> None:
        otp = f"{random.randint(0, 999999):06d}"
        record = OtpRecord(
            user_id=user_id,
            otp_hash=hash_value(otp),
            transaction_id=transaction_id,
            expiry_time=datetime.utcnow() + timedelta(minutes=settings.otp_expiry_minutes),
            is_used=False,
        )
        db.add(record)
        db.commit()

        print(f"[MOCK OTP] user_id={user_id} transaction_id={transaction_id} otp={otp}")

    @staticmethod
    def verify_otp(db: Session, user_id: int, transaction_id: int, otp: str) -> bool:
        record = (
            db.query(OtpRecord)
            .filter(OtpRecord.user_id == user_id, OtpRecord.transaction_id == transaction_id)
            .order_by(OtpRecord.created_at.desc())
            .first()
        )
        if not record:
            return False
        if record.is_used or record.expiry_time < datetime.utcnow():
            return False
        if not verify_value(otp, record.otp_hash):
            return False

        record.is_used = True
        db.add(record)
        db.commit()
        return True
