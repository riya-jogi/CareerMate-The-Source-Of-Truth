from fastapi import APIRouter
from app.core.errors import NotFoundError, ConflictError, AppException
from app.main import app
from fastapi.testclient import TestClient

dummy_error_router = APIRouter(prefix="/api/v1/test-errors")


@dummy_error_router.get("/not-found")
def trigger_not_found():
    raise NotFoundError("The candidate record was not found", details={"resource": "CareerProfile"})


@dummy_error_router.get("/conflict")
def trigger_conflict():
    raise ConflictError("An account with this email already exists", details={"field": "email"})


# Temporarily include router for testing
app.include_router(dummy_error_router)


def test_custom_not_found_error_format(client):
    response = client.get("/api/v1/test-errors/not-found")
    assert response.status_code == 404
    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == "RESOURCE_NOT_FOUND"
    assert data["error"]["message"] == "The candidate record was not found"
    assert data["error"]["details"]["resource"] == "CareerProfile"


def test_custom_conflict_error_format(client):
    response = client.get("/api/v1/test-errors/conflict")
    assert response.status_code == 409
    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == "RESOURCE_CONFLICT"
    assert data["error"]["details"]["field"] == "email"
