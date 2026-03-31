def predict_risk(features: dict) -> dict:
    # Placeholder scoring logic until PaySim models are trained and loaded.
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
