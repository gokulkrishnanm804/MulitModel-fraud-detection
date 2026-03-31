import httpx

from app.core.config import settings


class MlService:
    @staticmethod
    def score(payload: dict) -> dict:
        try:
            response = httpx.post(f"{settings.ml_service_base_url}/predict", json=payload, timeout=4.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return {
                "risk_score": 0.5,
                "risk_level": "MEDIUM",
                "reasons": ["ML service unavailable"],
            }
