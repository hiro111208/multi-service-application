def test_health_returns_ok(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_ready_returns_ok_when_dependencies_are_available(client):
    response = client.get("/ready")

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["status"] == "ready"
    assert payload["mongodb"] == "ok"
    assert payload["redis"] == "ok"
