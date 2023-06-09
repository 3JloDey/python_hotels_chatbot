import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from bot.dialogs import register_user_dialogs
from bot.handlers import register_user_handlers

logger = logging.getLogger(__name__)


async def main() -> None:
    load_dotenv()

    logging.basicConfig(
        # filename=r"bot/logging/logging.log",
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
        # encoding="utf-8",
    )

    logger.info("Starting bot")
    token = os.getenv("BOT_TOKEN", '')

    storage = MemoryStorage()
    bot = Bot(token=token, parse_mode="HTML")
    dp = Dispatcher(bot=bot, storage=storage)

    register_user_handlers(dp)
    register_user_dialogs(dp)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)

    finally:
        await dp.storage.close()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
