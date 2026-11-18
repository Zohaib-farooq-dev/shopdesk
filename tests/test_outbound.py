import httpx

from app import outbound


def test_4xx_not_retried(monkeypatch):
    calls = []

    def fake_post(url, json, timeout):
        calls.append(url)
        return httpx.Response(422)

    monkeypatch.setattr(outbound.httpx, "post", fake_post)
    assert outbound.notify_warehouse({"sku": "MUG"}) is False
    assert len(calls) == 1
