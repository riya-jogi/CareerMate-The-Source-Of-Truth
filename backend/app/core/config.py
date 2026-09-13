from typing import List, Union
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Project Information
    PROJECT_NAME: str = "CareerMate - ATS & Resume Optimization Platform"
    PROJECT_DESCRIPTION: str = (
        "AI Candidate ATS / Resume Optimization platform where the candidate's "
        "verified career information is the source of truth."
    )
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # Database Configuration
    DATABASE_URL: str = Field(
        default="postgresql+psycopg://postgres:Postgres%40123@localhost:5432/careermate_db",
        description="PostgreSQL connection string with psycopg3 driver",
    )
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    DB_POOL_TIMEOUT: int = 30
    DB_POOL_PRE_PING: bool = True

    # Security & JWT Authentication
    JWT_SECRET_KEY: str = Field(
        default="careermate-insecure-dev-secret-key-change-in-production-2026",
        description="Secret key for JWT signing",
    )
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15  # 15 minutes for short-lived access tokens
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7     # 7 days for revocable sessions
    REFRESH_COOKIE_NAME: str = "careermate_refresh_token"
    REFRESH_COOKIE_PATH: str = "/api/v1/auth"
    COOKIE_SECURE: bool = False
    COOKIE_SAMESITE: str = "lax"

    # CORS Configuration
    CORS_ORIGINS: Union[List[str], str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
    ]

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",") if i.strip()]
        elif isinstance(v, list):
            return v
        return ["http://localhost:5173", "http://127.0.0.1:5173"]

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT.lower() == "production"

    def get_safe_summary(self) -> dict:
        """Returns safe configuration summary with sensitive credentials redacted."""
        db_masked = self.DATABASE_URL
        if "@" in db_masked:
            prefix, rest = db_masked.split("@", 1)
            scheme_user = prefix.split(":")[0] + "://***"
            db_masked = f"{scheme_user}@{rest}"
        return {
            "project_name": self.PROJECT_NAME,
            "version": self.VERSION,
            "environment": self.ENVIRONMENT,
            "debug": self.DEBUG,
            "database_target": db_masked,
            "cors_origins": self.CORS_ORIGINS,
        }


settings = Settings()
