from fastapi import APIRouter, HTTPException

from app import inventory
from app.ledger import record_refund
from app.orders import get_order

router = APIRouter()
RETURNS: list[dict] = []
FLOW = {"requested": "approved", "approved": "received"}


@router.post("")
def open_return(order_id: int, reason: str):
    order = get_order(order_id)
    item = {"id": len(RETURNS) + 1, "order_id": order_id, "sku": order["sku"], "qty": order["qty"], "reason": reason, "status": "requested"}
    RETURNS.append(item)
    return item


@router.post("/{return_id}/advance")
def advance(return_id: int, sellable: bool = True):
    item = next((r for r in RETURNS if r["id"] == return_id), None)
    if not item or item["status"] not in FLOW:
        raise HTTPException(409, "return cannot advance")
    item["status"] = FLOW[item["status"]]
    if item["status"] == "approved":
        record_refund(item, get_order(item["order_id"]).get("amount", 0.0))
    if item["status"] == "received" and sellable:
        inventory.adjust(item["sku"], item["qty"])
    return item
