import hashlib
import hmac
import logging

from fastapi import APIRouter, Header, HTTPException, Request

from app.orders import transition
from config.settings import COURIER_SECRETS

router = APIRouter()
log = logging.getLogger(__name__)
EVENT_TO_STATUS = {"picked_up": "shipped", "attempted": "shipped", "delivered": "delivered", "returned_to_sender": "returned"}


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
    status = EVENT_TO_STATUS.get(event["type"])
    if status is None:
        log.warning("ignoring courier event %s from %s", event["type"], courier)
        return {"ignored": event["type"]}
    return transition(int(event["order_id"]), status)
