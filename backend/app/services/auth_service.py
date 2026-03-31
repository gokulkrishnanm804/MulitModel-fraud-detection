from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_value, verify_value
from app.models.user import User
from app.schemas.auth import AuthResponse, LoginRequest, RegisterRequest, SetPinRequest


class AuthService:
    @staticmethod
    def register(db: Session, request: RegisterRequest) -> AuthResponse:
        if db.query(User).filter(User.email == request.email).first():
            raise ValueError("Email already exists")
        if db.query(User).filter(User.phone == request.phone).first():
            raise ValueError("Phone already exists")

        user = User(
            name=request.name,
            email=request.email,
            phone=request.phone,
            password_hash=hash_value(request.password),
            balance=request.initial_balance,
            role="USER",
            is_blocked=False,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        token = create_access_token(user.email, user.role)
        return AuthResponse(token=token, requires_pin_setup=True)

    @staticmethod
    def login(db: Session, request: LoginRequest) -> AuthResponse:
        user = db.query(User).filter(User.email == request.email).first()
        if not user or not verify_value(request.password, user.password_hash):
            raise ValueError("Invalid credentials")
        if user.is_blocked:
            raise ValueError("User is blocked")

        token = create_access_token(user.email, user.role)
        return AuthResponse(token=token, requires_pin_setup=(user.pin_hash is None))

    @staticmethod
    def set_pin(db: Session, user_email: str, request: SetPinRequest) -> None:
        if request.pin != request.confirm_pin:
            raise ValueError("PIN and confirm PIN do not match")

        user = db.query(User).filter(User.email == user_email).first()
        if not user:
            raise ValueError("User not found")

        user.pin_hash = hash_value(request.pin)
        db.add(user)
        db.commit()
