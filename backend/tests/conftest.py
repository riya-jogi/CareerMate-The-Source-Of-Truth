import os
import sys
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

# Add backend directory to sys.path
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.main import app
from app.db.session import SessionLocal, engine
from app.models import Base


@pytest.fixture
def db_session():
    """Provides an independent database session for tests."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="module")
def client():
    """Provides a TestClient for FastAPI app."""
    with TestClient(app) as test_client:
        yield test_client
