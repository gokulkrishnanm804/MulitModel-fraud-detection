from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.transaction import TransferRequest, VerifyOtpRequest
from app.services.transaction_service import TransactionService

router = APIRouter(tags=["Transaction"])


@router.post("/transfer")
def transfer(
    request: TransferRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        data = TransactionService.transfer(db, current_user, request)
        return {"message": "Transfer processed", "data": data.model_dump()}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/verify-otp")
def verify_otp(
    request: VerifyOtpRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        data = TransactionService.verify_otp(db, current_user, request)
        return {"message": "OTP verification processed", "data": data.model_dump()}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
