import hashlib
import hmac
import json

from fastapi.testclient import TestClient

from app.main import app
from config import settings

client = TestClient(app)


def signed(body: dict, secret: str):
    raw = json.dumps(body).encode()
    return raw, hmac.new(secret.encode(), raw, hashlib.sha256).hexdigest()


def test_bad_signature_rejected(monkeypatch):
    monkeypatch.setitem(settings.COURIER_SECRETS, "tcs", "s3cret")
    raw, _ = signed({"order_id": 1, "type": "delivered"}, "s3cret")
    r = client.post("/webhooks/courier/tcs", content=raw, headers={"x-signature": "nope"})
    assert r.status_code == 401
