from typing import Optional, Tuple

import aiohttp
import logging

from config import AMO_BASE_URL, AMO_BEARER_TOKEN

logger = logging.getLogger(__name__)


async def amo_get_lead(lead_id: int) -> Optional[dict]:
    url = f"{AMO_BASE_URL}/api/v4/leads/{lead_id}"
    headers = {
        "Authorization": f"Bearer {AMO_BEARER_TOKEN}",
        "Accept": "application/json",
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, timeout=10) as resp:
            if resp.status == 200:
                return await resp.json()
            if resp.status == 404:
                return None
            body = await resp.text()
            logger.warning("amo_get_lead %s status=%s body=%s", lead_id, resp.status, body)
            raise RuntimeError(f"Amo get lead error {resp.status}")


async def amo_delete_lead(lead_id: int) -> Tuple[bool, str | None]:
    url = f"{AMO_BASE_URL}/api/v4/leads/{lead_id}"
    headers = {
        "Authorization": f"Bearer {AMO_BEARER_TOKEN}",
        "Accept": "application/json",
    }
    async with aiohttp.ClientSession() as session:
        async with session.delete(url, headers=headers, timeout=10) as resp:
            if resp.status in (200, 202, 204):
                return True, None
            body = await resp.text()
            logger.warning("amo_delete_lead %s status=%s body=%s", lead_id, resp.status, body)
            if resp.status == 404:
                return False, "Сделка не найдена (404)."
            if resp.status == 403:
                return False, "У интеграции нет прав на удаление сделок (403)."
            return False, f"Ошибка AmoCRM: {resp.status}\n{body}"
