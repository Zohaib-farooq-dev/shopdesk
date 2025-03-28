import hashlib
import hmac

from fastapi import APIRouter, Header, HTTPException, Request

from app.orders import transition
from config.settings import COURIER_SECRETS

router = APIRouter()
EVENT_TO_STATUS = {"picked_up": "shipped", "delivered": "delivered", "returned_to_sender": "returned"}


@router.post("/courier/{courier}")
async def courier_event(courier: str, request: Request, x_signature: str = Header(default="")):
    secret = COURIER_SECRETS.get(courier)
    if not secret:
        raise HTTPException(404, "unknown courier")
    body = await request.body()
    expected = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, x_signature):
        raise HTTPException(401, "bad signature")
    event = await request.json()
    return transition(int(event["order_id"]), EVENT_TO_STATUS[event["type"]])
