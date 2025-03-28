import os

COURIER_SECRETS = {
    "tcs": os.getenv("TCS_WEBHOOK_SECRET", ""),
    "leopards": os.getenv("LEOPARDS_WEBHOOK_SECRET", ""),
}
WEBHOOK_RETRY_ATTEMPTS = 3
