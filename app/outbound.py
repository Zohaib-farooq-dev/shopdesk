import time

import httpx

from config.settings import WEBHOOK_RETRY_ATTEMPTS, WAREHOUSE_URL


def notify_warehouse(payload: dict) -> bool:
    delay = 0.5
    for attempt in range(WEBHOOK_RETRY_ATTEMPTS):
        try:
            r = httpx.post(WAREHOUSE_URL, json=payload, timeout=5)
            if r.status_code < 500:
                return r.status_code < 300
        except httpx.HTTPError:
            pass
        time.sleep(delay)
        delay *= 4
    return False
