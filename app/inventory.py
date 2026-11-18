from fastapi import APIRouter, HTTPException

router = APIRouter()
STOCK: dict[str, int] = {}
RESERVED: dict[str, int] = {}


@router.post("/adjust")
def adjust(sku: str, delta: int):
    STOCK[sku] = STOCK.get(sku, 0) + delta
    return {"sku": sku, "on_hand": STOCK[sku], "available": available(sku)}


@router.get("/low-stock")
def low_stock(threshold: int = 5):
    return [{"sku": sku, "available": available(sku)} for sku in sorted(STOCK) if available(sku) <= threshold]


def available(sku: str) -> int:
    return STOCK.get(sku, 0) - RESERVED.get(sku, 0)


def reserve(sku: str, qty: int) -> None:
    if available(sku) < qty:
        raise HTTPException(409, f"only {available(sku)} of {sku} available")
    RESERVED[sku] = RESERVED.get(sku, 0) + qty


def release(sku: str, qty: int) -> None:
    RESERVED[sku] = max(0, RESERVED.get(sku, 0) - qty)
