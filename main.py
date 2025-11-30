import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import TELEGRAM_BOT_TOKEN
from handlers import setup_routers


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


async def main():
    bot = Bot(token=TELEGRAM_BOT_TOKEN, parse_mode="HTML")
    dp = Dispatcher()

    dp.include_router(setup_routers())

    logger.info("Starting bot polling")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
