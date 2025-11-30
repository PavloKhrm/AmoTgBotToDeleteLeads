import os

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or ""
AMO_BASE_URL = (os.getenv("AMO_BASE_URL") or "").rstrip("/")
AMO_BEARER_TOKEN = os.getenv("AMO_BEARER_TOKEN") or ""

ALLOWED_USER_IDS = {
    int(x.strip())
    for x in (os.getenv("ALLOWED_USER_IDS") or "").split(",")
    if x.strip()
}

if not TELEGRAM_BOT_TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN is not set")
if not AMO_BASE_URL:
    raise RuntimeError("AMO_BASE_URL is not set")
if not AMO_BEARER_TOKEN:
    raise RuntimeError("AMO_BEARER_TOKEN is not set")
if not ALLOWED_USER_IDS:
    raise RuntimeError("ALLOWED_USER_IDS is empty or not set")
