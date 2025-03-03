from fastapi import APIRouter, HTTPException

router = APIRouter()
ORDERS: dict[int, dict] = {}


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
