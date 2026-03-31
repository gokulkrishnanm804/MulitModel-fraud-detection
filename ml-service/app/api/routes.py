from fastapi import APIRouter

from app.api.schemas import PredictRequest, PredictResponse
from app.ml.feature_engineering import build_features
from app.ml.model_predictor import predict_risk

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "healthy"}


@router.post("/predict", response_model=PredictResponse)
def predict(payload: PredictRequest):
    features = build_features(payload.model_dump())
    result = predict_risk(features)
    return PredictResponse(**result)
