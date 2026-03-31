from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth, transaction, admin
from app.models.user import Base
from app.db import base as _db_base
from app.db.session import engine

app = FastAPI(title="Fraud Detection Backend", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(transaction.router)
app.include_router(admin.router)


@app.get("/health")
def health() -> dict:
    return {"status": "healthy"}
