from datetime import datetime, timezone

LEDGER: list[dict] = []


def record_refund(return_item: dict, amount: float) -> dict:
    entry = {"return_id": return_item["id"], "order_id": return_item["order_id"], "amount": amount, "at": datetime.now(timezone.utc).isoformat()}
    LEDGER.append(entry)  # append-only: finance reconciles against this, never edit entries
    return entry


def reverse_refund(return_item: dict) -> dict:
    original = next(e for e in LEDGER if e["return_id"] == return_item["id"])
    entry = {**original, "amount": -original["amount"], "at": datetime.now(timezone.utc).isoformat(), "reversal_of": original["return_id"]}
    LEDGER.append(entry)
    return entry
