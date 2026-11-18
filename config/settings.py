import os

COURIER_SECRETS = {
    "tcs": os.getenv("TCS_WEBHOOK_SECRET", ""),
    "leopards": os.getenv("LEOPARDS_WEBHOOK_SECRET", ""),
}
WAREHOUSE_URL = os.getenv("WAREHOUSE_URL", "http://warehouse.internal/sync")
WEBHOOK_RETRY_ATTEMPTS = 5
