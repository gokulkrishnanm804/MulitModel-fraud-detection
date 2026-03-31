from fastapi import FastAPI

from app.api import auth, transaction, admin
from app.models.user import Base
from app.db.session import engine

app = FastAPI(title="Fraud Detection Backend", version="1.0.0")

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(transaction.router)
app.include_router(admin.router)


@app.get("/health")
def health() -> dict:
    return {"status": "healthy"}
