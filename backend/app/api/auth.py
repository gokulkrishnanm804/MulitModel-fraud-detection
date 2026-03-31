from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, RegisterRequest, SetPinRequest
from app.services.auth_service import AuthService

router = APIRouter(tags=["Auth"])


@router.post("/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    try:
        data = AuthService.register(db, request)
        return {"message": "User registered", "data": data.model_dump()}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    try:
        data = AuthService.login(db, request)
        return {"message": "Login successful", "data": data.model_dump()}
    except ValueError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc


@router.post("/set-pin")
def set_pin(
    request: SetPinRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        AuthService.set_pin(db, current_user.email, request)
        return {"message": "PIN set successfully", "data": "OK"}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
