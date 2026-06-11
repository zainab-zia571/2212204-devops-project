def test_health_returns_ok(client):
    response = client.get("/health")
    assert response.status_code == 200


def test_health_has_required_fields(client):
    response = client.get("/health")
    data = response.json()
    assert "status" in data
    assert "db" in data
    assert "student" in data


def test_health_status_is_ok(client):
    response = client.get("/health")
    assert response.json()["status"] == "ok"
    