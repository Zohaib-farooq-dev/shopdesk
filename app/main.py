from fastapi import FastAPI

from app.orders import router as orders_router
from app.inventory import router as inventory_router

app = FastAPI(title="ShopDesk")
app.include_router(orders_router, prefix="/orders")
app.include_router(inventory_router, prefix="/inventory")


@app.get("/health")
def health():
    return {"ok": True}
