from app import extensions


def test_create_and_list_items(client):
    create_response = client.post("/items", json={"name": "Test item"})

    assert create_response.status_code == 201
    created = create_response.get_json()
    assert created["name"] == "Test item"
    assert "id" in created
    assert "created_at" in created

    list_response = client.get("/items")
    assert list_response.status_code == 200
    items = list_response.get_json()["items"]
    assert len(items) == 1
    assert items[0]["name"] == "Test item"


def test_get_item_by_id(client):
    create_response = client.post("/items", json={"name": "Lookup item"})
    item_id = create_response.get_json()["id"]

    get_response = client.get(f"/items/{item_id}")
    assert get_response.status_code == 200
    assert get_response.get_json()["name"] == "Lookup item"


def test_get_item_returns_404_for_unknown_id(client):
    response = client.get("/items/507f1f77bcf86cd799439011")

    assert response.status_code == 404
    assert response.get_json() == {"error": "Item not found"}


def test_create_item_requires_name(client):
    response = client.post("/items", json={"name": "   "})

    assert response.status_code == 400
    assert response.get_json() == {"error": "Field 'name' is required"}


def test_items_are_cached_in_redis(client):
    client.post("/items", json={"name": "Cached item"})
    client.get("/items")

    assert extensions.redis_client.exists("items:all") == 1
