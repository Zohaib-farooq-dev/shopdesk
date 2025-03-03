from fastapi import APIRouter

router = APIRouter()
STOCK: dict[str, int] = {}


@router.post("/adjust")
def adjust(sku: str, delta: int):
    STOCK[sku] = STOCK.get(sku, 0) + delta
    return {"sku": sku, "on_hand": STOCK[sku]}
