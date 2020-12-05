import pytest
import json
from app import app


@pytest.fixture
def client():
    return app.test_client()


def test_json_list(client):
    req = client.get("/api/list")
    text_contents = req.data.decode()
    assert json.loads(text_contents) == {"scores": []}


def test_json_add(client):
    req = client.put("/api/new", json={"name": "Test", "score": 100})

    assert req.status_code == 204

    req = client.get("/api/list")
    assert req.get_json() == {"scores": [{"name": "Test", "score": 100}]}


def test_json_remove(client):
    for _ in range(0, 5):
        client.put("/api/new", json={"name": "Test", "score": 100})

    req = client.delete("/api/list", json={"name": "Test"})

    req = client.get("/api/list")
    assert req.get_json() == {"scores": []}


def test_invalid_add_empty_json(client):
    req = client.put("/api/new")
    assert req.status_code == 400


def test_invalid_add_json(client):
    req = client.put("/api/new", json={"name": "invalid"})
    assert req.status_code == 400


def test_invalid_delete_empty_json(client):
    req = client.delete("/api/list")
    assert req.status_code == 400


def test_invalid_delete_json(client):
    req = client.put("/api/new", json={"score": "invalid"})
    assert req.status_code == 400


def test_invalid_http_method_list(client):
    req = client.post("/api/list")
    assert req.status_code == 405
