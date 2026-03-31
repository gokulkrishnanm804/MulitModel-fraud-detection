"""Training entry point."""

from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from xgboost import XGBClassifier

from app.ml.feature_engineering import build_feature_frame

DEFAULT_DATASET = Path(__file__).resolve().parents[3] / "backend" / "data" / "PS_20174392719_1491204439457_log.csv"
MODEL_DIR = Path(__file__).resolve().parents[1] / "ml" / "artifacts"


def load_dataset(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = {
        "step",
        "type",
        "amount",
        "nameOrig",
        "oldbalanceOrg",
        "newbalanceOrig",
        "nameDest",
        "oldbalanceDest",
        "newbalanceDest",
        "isFraud",
    }
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    return df


def build_is_new_beneficiary(df: pd.DataFrame) -> pd.Series:
    ordered = df.sort_values("step")
    first_seen = ordered.groupby(["nameOrig", "nameDest"]).cumcount().eq(0)
    return first_seen.reindex(df.index).fillna(False).astype(int)


def main() -> None:
    dataset_path = Path(str(DEFAULT_DATASET))
    if not dataset_path.exists():
        raise FileNotFoundError(f"PaySim dataset not found at {dataset_path}")

    df = load_dataset(dataset_path)
    df["is_new_beneficiary"] = build_is_new_beneficiary(df)

    features = build_feature_frame(df)
    target = df["isFraud"].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=0.2,
        random_state=42,
        stratify=target,
    )

    positive = y_train.sum()
    negative = len(y_train) - positive
    scale_pos_weight = (negative / positive) if positive else 1.0

    xgb_model = XGBClassifier(
        n_estimators=250,
        max_depth=6,
        learning_rate=0.08,
        subsample=0.9,
        colsample_bytree=0.9,
        objective="binary:logistic",
        eval_metric="auc",
        scale_pos_weight=scale_pos_weight,
        n_jobs=4,
    )
    xgb_model.fit(X_train, y_train)

    rf_model = RandomForestClassifier(
        n_estimators=300,
        max_depth=None,
        class_weight="balanced_subsample",
        random_state=42,
        n_jobs=-1,
    )
    rf_model.fit(X_train, y_train)

    iso_model = IsolationForest(
        n_estimators=250,
        contamination=0.002,
        random_state=42,
        n_jobs=-1,
    )
    iso_model.fit(X_train[y_train == 0])

    xgb_probs = xgb_model.predict_proba(X_test)[:, 1]
    rf_probs = rf_model.predict_proba(X_test)[:, 1]
    iso_scores = iso_model.score_samples(X_test)
    iso_min, iso_max = float(iso_scores.min()), float(iso_scores.max())
    iso_scaled = (iso_scores - iso_min) / (iso_max - iso_min + 1e-9)
    iso_probs = 1.0 - iso_scaled

    ensemble_probs = (xgb_probs + rf_probs + iso_probs) / 3.0
    auc = roc_auc_score(y_test, ensemble_probs)

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(xgb_model, MODEL_DIR / "xgboost.joblib")
    joblib.dump(rf_model, MODEL_DIR / "random_forest.joblib")
    joblib.dump(iso_model, MODEL_DIR / "isolation_forest.joblib")
    joblib.dump(
        {
            "iso_min": iso_min,
            "iso_max": iso_max,
            "feature_columns": list(features.columns),
            "auc": float(auc),
        },
        MODEL_DIR / "meta.joblib",
    )

    print(f"Training complete. Ensemble AUC={auc:.4f}. Models saved to {MODEL_DIR}")


if __name__ == "__main__":
    main()
