from datetime import datetime, timezone

LEDGER: list[dict] = []


def record_refund(return_item: dict, amount: float) -> dict:
    entry = {"return_id": return_item["id"], "order_id": return_item["order_id"], "amount": amount, "at": datetime.now(timezone.utc).isoformat()}
    LEDGER.append(entry)  # append-only: finance reconciles against this, never edit entries
    return entry
