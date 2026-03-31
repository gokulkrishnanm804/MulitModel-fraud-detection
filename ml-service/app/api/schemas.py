from pydantic import BaseModel, Field


class PredictRequest(BaseModel):
    step: int = Field(ge=0)
    amount: float = Field(gt=0)
    oldbalanceOrig: float
    newbalanceOrig: float
    oldbalanceDest: float
    newbalanceDest: float
    is_new_beneficiary: int = Field(ge=0, le=1)


class PredictResponse(BaseModel):
    risk_score: float = Field(ge=0.0, le=1.0)
    risk_level: str
    reasons: list[str]
