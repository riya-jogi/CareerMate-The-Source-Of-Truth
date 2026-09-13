def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert "CareerMate" in data["name"]
    assert "version" in data


def test_health_endpoint_success(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"
    assert isinstance(data["database_latency_ms"], (int, float))
    assert data["database_latency_ms"] >= 0
    assert "timestamp" in data
    assert data["environment"] == "development"


def test_root_health_alias(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"
