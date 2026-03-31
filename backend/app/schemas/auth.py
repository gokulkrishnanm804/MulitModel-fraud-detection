from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    phone: str = Field(pattern=r"^[0-9]{10,15}$")
    password: str = Field(min_length=8)
    initial_balance: float = Field(ge=0)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class SetPinRequest(BaseModel):
    pin: str = Field(pattern=r"^[0-9]{4,6}$")
    confirm_pin: str


class AuthResponse(BaseModel):
    token: str
    requires_pin_setup: bool
