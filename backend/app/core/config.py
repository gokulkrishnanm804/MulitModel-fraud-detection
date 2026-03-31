from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Fraud Detection Backend"
    db_url: str = "mysql+pymysql://root:root@localhost:3306/fraud_detection"
    jwt_secret: str = "change_this_to_long_random_secret_for_production"
    jwt_algorithm: str = "HS256"
    jwt_expiry_minutes: int = 60
    ml_service_base_url: str = "http://localhost:8001/api/v1"
    otp_expiry_minutes: int = 5
    high_amount_threshold: float = 200000.0

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
