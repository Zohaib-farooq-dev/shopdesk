import hashlib
import hmac
import logging
import time

from fastapi import APIRouter, Header, HTTPException, Request

from app.orders import transition
from config.settings import COURIER_SECRETS

router = APIRouter()
log = logging.getLogger(__name__)
EVENT_TO_STATUS = {"picked_up": "shipped", "attempted": "shipped", "delivered": "delivered", "returned_to_sender": "returned"}
SEEN: dict[str, float] = {}  # event id -> time seen; couriers retry with the same id for up to an hour


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
    event_id = f"{courier}:{event.get('id', '')}"
    now = time.time()
    for k, t in list(SEEN.items()):
        if now - t > 3600:
            del SEEN[k]
    if event_id in SEEN:
        log.info("duplicate courier event %s", event_id)
        return {"duplicate": True}
    SEEN[event_id] = now
    status = EVENT_TO_STATUS.get(event["type"])
    if status is None:
        log.warning("ignoring courier event %s from %s", event["type"], courier)
        return {"ignored": event["type"]}
    return transition(int(event["order_id"]), status)
