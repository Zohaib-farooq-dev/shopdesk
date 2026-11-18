from fastapi import FastAPI

from app.orders import router as orders_router
from app.inventory import router as inventory_router
from app.returns import router as returns_router
from app.webhooks import router as webhooks_router

app = FastAPI(title="ShopDesk")
app.include_router(orders_router, prefix="/orders")
app.include_router(inventory_router, prefix="/inventory")
app.include_router(returns_router, prefix="/returns")
app.include_router(webhooks_router, prefix="/webhooks")


@app.get("/health")
def health():
    return {"ok": True}
