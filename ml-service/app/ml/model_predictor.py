from pathlib import Path

import joblib
import numpy as np


MODEL_DIR = Path(__file__).resolve().parent / "artifacts"
_MODELS = None


def _load_models() -> dict | None:
    global _MODELS
    if _MODELS is not None:
        return _MODELS

    xgb_path = MODEL_DIR / "xgboost.joblib"
    rf_path = MODEL_DIR / "random_forest.joblib"
    iso_path = MODEL_DIR / "isolation_forest.joblib"
    meta_path = MODEL_DIR / "meta.joblib"

    if not (xgb_path.exists() and rf_path.exists() and iso_path.exists() and meta_path.exists()):
        _MODELS = None
        return None

    _MODELS = {
        "xgb": joblib.load(xgb_path),
        "rf": joblib.load(rf_path),
        "iso": joblib.load(iso_path),
        "meta": joblib.load(meta_path),
    }
    return _MODELS


def _fallback_score(features: dict) -> dict:
    base_score = min(1.0, max(0.0, (features["amount_deviation"] * 0.35) + (features["balance_error"] / 100000.0)))
    reasons = []
    if features["amount"] > 200000:
        reasons.append("High amount")
    if features["is_new_beneficiary"] == 1:
        reasons.append("New beneficiary")
    if features["balance_error"] > 1000:
        reasons.append("Unusual transaction pattern")

    if base_score < 0.3:
        level = "LOW"
    elif base_score <= 0.7:
        level = "MEDIUM"
    else:
        level = "HIGH"

    return {
        "risk_score": round(base_score, 4),
        "risk_level": level,
        "reasons": reasons,
    }


def predict_risk(features: dict) -> dict:
    models = _load_models()
    if not models:
        return _fallback_score(features)

    meta = models["meta"]
    feature_columns = meta.get("feature_columns", [])
    vector = np.array([[features[name] for name in feature_columns]], dtype=float)

    xgb_prob = float(models["xgb"].predict_proba(vector)[:, 1][0])
    rf_prob = float(models["rf"].predict_proba(vector)[:, 1][0])
    iso_scores = models["iso"].score_samples(vector)
    iso_min = float(meta.get("iso_min", -1.0))
    iso_max = float(meta.get("iso_max", 1.0))
    iso_scaled = (iso_scores - iso_min) / (iso_max - iso_min + 1e-9)
    iso_prob = float(1.0 - iso_scaled[0])

    risk_score = (xgb_prob + rf_prob + iso_prob) / 3.0

    reasons = []
    if features["amount"] > 200000:
        reasons.append("High amount")
    if features["is_new_beneficiary"] == 1:
        reasons.append("New beneficiary")
    if features["balance_error"] > 1000:
        reasons.append("Unusual transaction pattern")

    if risk_score < 0.3:
        level = "LOW"
    elif risk_score <= 0.7:
        level = "MEDIUM"
    else:
        level = "HIGH"

    return {
        "risk_score": round(float(risk_score), 4),
        "risk_level": level,
        "reasons": reasons,
    }
