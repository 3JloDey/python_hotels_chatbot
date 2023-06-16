import asyncio
from typing import Union
from aiogram.filters.command import CommandStart

import betterlogging as logging
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage

from bot.config import Config, load_config
from bot.dialogs import register_user_dialogs
from bot.handlers.user_handlers import command_start
from bot.middlewares.config_middleware import ConfigMiddleware

logger = logging.getLogger(__name__)


async def main() -> None:
    logging.basic_colorized_config(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )

    logger.info("Starting bot")
    config: Config = load_config(".env")

    storage: Union[MemoryStorage, RedisStorage]
    # Choosing FSM storage
    if config.bot_fsm_storage == "memory":
        storage = MemoryStorage()
    else:
        storage = RedisStorage.from_url(
            config.redis_dsn, key_builder=DefaultKeyBuilder(with_destiny=True)
        )

    bot = Bot(token=config.bot_token, parse_mode=ParseMode.HTML)
    dp = Dispatcher(bot=bot, storage=storage)

    # Allow interaction in private chats (not groups or channels) only
    dp.message.filter(F.chat.type == "private")
    # Register middlewares
    dp.callback_query.middleware.register(ConfigMiddleware(config=config, bot=bot))
    # Register handlers
    dp.message.register(command_start, CommandStart())
    # Register dialogs
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
