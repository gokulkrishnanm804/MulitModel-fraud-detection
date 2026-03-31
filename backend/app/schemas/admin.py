from pydantic import BaseModel


class DashboardResponse(BaseModel):
    total_transactions: int
    fraud_count: int
    legit_count: int
    flagged_transactions: int


class BlockUserRequest(BaseModel):
    user_id: int
    blocked: bool
