from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class ConfigMiddleware(BaseMiddleware):
    def __init__(self, config, bot) -> None:
        super().__init__()
        self.config = config
        self.bot = bot

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        data["config"] = self.config
        data["bot"] = self.bot
        return await handler(event, data)
