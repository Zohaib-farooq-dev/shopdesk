from fastapi import APIRouter

router = APIRouter()
RETURNS: list[dict] = []


@router.post("")
def open_return(order_id: int, reason: str):
    item = {"order_id": order_id, "reason": reason, "status": "requested"}
    RETURNS.append(item)
    return item
