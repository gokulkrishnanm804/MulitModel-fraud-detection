def build_features(payload: dict) -> dict:
    hour = payload["step"] % 24
    amount_deviation = payload["amount"] / (payload["oldbalanceOrig"] + 1.0)
    balance_error = abs((payload["oldbalanceOrig"] - payload["newbalanceOrig"]) - payload["amount"])

    return {
        "hour": hour,
        "is_new_beneficiary": payload["is_new_beneficiary"],
        "amount_deviation": amount_deviation,
        "balance_error": balance_error,
        "amount": payload["amount"],
    }
