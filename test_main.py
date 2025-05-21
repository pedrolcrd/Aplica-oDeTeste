from fastapi.testclient import TestClient
from main import app, db

client = TestClient(app)

def setup_function():
    # Limpa coleção antes de cada teste
    db.items.delete_many({})


def test_get_items_empty():
    response = client.get("/items")
    assert response.status_code == 200
    assert response.json() == []


def test_create_item_and_get():
    # Cria item
    response = client.post("/items", json={"name": "Test Item"})
    assert response.status_code == 201
    data = response.json()
    assert data["id"]
    assert data["name"] == "Test Item"

    # Recupera
    response = client.get("/items")
    assert response.status_code == 200
    items = response.json()
    assert len(items) == 1
    assert items[0] == data
