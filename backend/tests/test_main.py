from fastapi.testclient import TestClient

from app.main import app


def test_root() -> None:
    with TestClient(app) as client:
        response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "application": "AutoKey",
        "version": "0.1.0",
        "status": "ok",
    }


def test_health() -> None:
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
    }


def test_statistics() -> None:
    with TestClient(app) as client:
        response = client.get("/statistics")

    assert response.status_code == 200

    data = response.json()

    assert set(data) == {
        "word_count",
        "node_count",
        "average_depth",
        "memory_bytes",
        "memory_megabytes",
    }

    assert isinstance(data["word_count"], int)
    assert isinstance(data["node_count"], int)
    assert isinstance(data["average_depth"], float)
    assert isinstance(data["memory_bytes"], int)
    assert isinstance(data["memory_megabytes"], float)

    assert data["word_count"] > 0
    assert data["node_count"] >= data["word_count"]
    assert data["average_depth"] > 0
    assert data["memory_bytes"] > 0
    assert data["memory_megabytes"] > 0


def test_statistics_values_are_consistent() -> None:
    with TestClient(app) as client:
        response = client.get("/statistics")

    assert response.status_code == 200

    data = response.json()

    assert data["node_count"] >= data["word_count"]
    assert data["memory_bytes"] > 0
    assert data["memory_megabytes"] > 0
    assert data["average_depth"] > 0


def test_cors_allows_configured_frontend() -> None:
    with TestClient(app) as client:
        response = client.get(
            "/health",
            headers={
                "Origin": "http://localhost:3000",
            },
        )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == (
        "http://localhost:3000"
    )