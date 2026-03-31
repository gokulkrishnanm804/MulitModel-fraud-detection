from pydantic import BaseModel, Field


class TransferRequest(BaseModel):
    receiver_id: int
    amount: float = Field(gt=0)
    type: str = Field(pattern=r"^(UPI|CARD|ACCOUNT_TRANSFER)$")
    pin: str = Field(pattern=r"^[0-9]{4,6}$")
    step: int = Field(ge=0)
    oldbalanceOrig: float | None = None
    newbalanceOrig: float | None = None
    oldbalanceDest: float | None = None
    newbalanceDest: float | None = None
    is_new_beneficiary: int = Field(default=0, ge=0, le=1)


class VerifyOtpRequest(BaseModel):
    transaction_id: int
    otp: str = Field(pattern=r"^[0-9]{6}$")


class TransferResponse(BaseModel):
    transaction_id: int
    status: str
    risk_score: float
    risk_level: str
    message: str
    reasons: list[str]
