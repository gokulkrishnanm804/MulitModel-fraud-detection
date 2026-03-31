from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(title="Fraud Detection ML Service", version="0.1.0")
app.include_router(router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "Fraud Detection ML service is running"}
