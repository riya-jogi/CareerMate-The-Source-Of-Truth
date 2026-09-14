from app.core.config import Settings


def test_settings_default_values():
    settings = Settings()
    assert settings.PROJECT_NAME == "CareerMate - ATS & Resume Optimization Platform"
    assert settings.API_V1_STR == "/api/v1"
    assert "careermate_db" in settings.DATABASE_URL
    assert settings.JWT_ALGORITHM == "HS256"
    assert settings.ACCESS_TOKEN_EXPIRE_MINUTES > 0


def test_cors_origins_parsing():
    settings_from_str = Settings(CORS_ORIGINS="http://localhost:5173,https://careermate.ai")
    assert "http://localhost:5173" in settings_from_str.CORS_ORIGINS
    assert "https://careermate.ai" in settings_from_str.CORS_ORIGINS

    settings_from_list = Settings(CORS_ORIGINS=["http://custom-origin.com"])
    assert settings_from_list.CORS_ORIGINS == ["http://custom-origin.com"]


def test_get_safe_summary_redacts_credentials():
    settings = Settings(DATABASE_URL="postgresql+psycopg://myuser:supersecretpass@localhost:5432/testdb")
    summary = settings.get_safe_summary()
    assert "supersecretpass" not in summary["database_target"]
    assert "***" in summary["database_target"]
    assert "@localhost:5432/testdb" in summary["database_target"]


def test_production_rejects_development_jwt_secret():
    try:
        Settings(
            ENVIRONMENT="production",
            JWT_SECRET_KEY="careermate-insecure-dev-secret-key-change-in-production-2026",
            COOKIE_SECURE=True,
        )
    except ValueError as exc:
        assert "JWT_SECRET_KEY" in str(exc)
    else:
        raise AssertionError("Production settings accepted the development JWT secret")


def test_production_requires_secure_refresh_cookie():
    try:
        Settings(
            ENVIRONMENT="production",
            JWT_SECRET_KEY="a" * 64,
            COOKIE_SECURE=False,
        )
    except ValueError as exc:
        assert "COOKIE_SECURE" in str(exc)
    else:
        raise AssertionError("Production settings accepted an insecure refresh cookie")
