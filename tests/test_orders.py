from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_and_get_order():
    r = client.post("/orders", json={"sku": "TSHIRT-M", "qty": 2})
    assert r.status_code == 200
    assert client.get(f"/orders/{r.json()['id']}").json()["status"] == "new"


def test_invalid_transition_is_409():
    order = client.post("/orders", json={"sku": "MUG", "qty": 1}).json()
    assert client.post(f"/orders/{order['id']}/transition", params={"to": "shipped"}).status_code == 409
