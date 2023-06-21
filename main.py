import asyncio

import betterlogging as logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters.command import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage

from bot.config import Config, load_config
from bot.dialogs import register_user_dialogs
from bot.handlers.user_handlers import command_start
from bot.middlewares.environment_middleware import EnvironmentMiddleware
from bot.middlewares.privat_middleware import PrivatOnlyMiddleware
from bot.services.api_requests import API_interface
from bot.utils import set_commands

logger = logging.getLogger(__name__)


async def on_startup(bot: Bot) -> None:
    logger.info("Starting bot")
    await set_commands(bot)


async def main() -> None:
    logging.basic_colorized_config(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )

    config: Config = load_config(".env")
    # Choosing FSM storage
    if config.tg_bot.use_redis is False:
        storage = MemoryStorage()
    else:
        storage = RedisStorage.from_url(config.redis.url, key_builder=DefaultKeyBuilder(with_destiny=True))

    bot = Bot(token=config.tg_bot.token, parse_mode=ParseMode.HTML)
    dp = Dispatcher(bot=bot, storage=storage)
    api = API_interface(config.tg_bot.api_token)

    # Register middlewares
    dp.message.middleware.register(PrivatOnlyMiddleware())
    dp.update.middleware.register(EnvironmentMiddleware(config=config, bot=bot, api=api))
    # Register handlers
    dp.startup.register(on_startup)
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
