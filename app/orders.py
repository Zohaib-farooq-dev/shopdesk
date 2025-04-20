from fastapi import APIRouter, HTTPException

from app import inventory

router = APIRouter()
ORDERS: dict[int, dict] = {}

# Allowed transitions. Anything else is a 409 so courier bugs show up instead of corrupting orders.
TRANSITIONS = {
    "new": {"paid", "cancelled"},
    "paid": {"packed", "cancelled"},
    "packed": {"shipped"},
    "shipped": {"delivered", "returned"},
    "delivered": {"returned"},
}


@router.post("")
def create_order(order: dict):
    order_id = len(ORDERS) + 1
    ORDERS[order_id] = {"id": order_id, "status": "new", **order}
    return ORDERS[order_id]


@router.get("/{order_id}")
def get_order(order_id: int):
    if order_id not in ORDERS:
        raise HTTPException(404, "order not found")
    return ORDERS[order_id]


@router.post("/{order_id}/transition")
def transition(order_id: int, to: str):
    order = get_order(order_id)
    if to not in TRANSITIONS.get(order["status"], set()):
        raise HTTPException(409, f"cannot go from {order['status']} to {to}")
    if to == "paid":
        inventory.reserve(order["sku"], order["qty"])
    if to == "cancelled" and order["status"] == "paid":
        inventory.release(order["sku"], order["qty"])
    order["status"] = to
    return order
