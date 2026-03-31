from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import require_admin
from app.db.session import get_db
from app.schemas.admin import BlockUserRequest
from app.services.admin_service import AdminService

router = APIRouter(tags=["Admin"])


@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db), _=Depends(require_admin)):
    data = AdminService.dashboard(db)
    return {"message": "Dashboard fetched", "data": data.model_dump()}


@router.get("/transactions")
def transactions(db: Session = Depends(get_db), _=Depends(require_admin)):
    data = AdminService.recent_transactions(db)
    return {"message": "Transactions fetched", "data": data}


@router.get("/users")
def users(db: Session = Depends(get_db), _=Depends(require_admin)):
    data = AdminService.list_users(db)
    return {"message": "Users fetched", "data": data}


@router.get("/fraud-transactions")
def fraud_transactions(db: Session = Depends(get_db), _=Depends(require_admin)):
    data = AdminService.fraud_transactions(db)
    return {"message": "Fraud transactions fetched", "data": data}


@router.get("/fraud-logs")
def fraud_logs(db: Session = Depends(get_db), _=Depends(require_admin)):
    data = AdminService.fraud_logs(db)
    return {"message": "Fraud logs fetched", "data": data}


@router.post("/block-user")
def block_user(request: BlockUserRequest, db: Session = Depends(get_db), _=Depends(require_admin)):
    try:
        AdminService.block_user(db, request.user_id, request.blocked)
        return {"message": "User status updated", "data": "OK"}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
