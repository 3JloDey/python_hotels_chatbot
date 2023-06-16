from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class EnvironmentMiddleware(BaseMiddleware):
    """
    A middleware that adds environment variables to the dialog manager's data dictionary.

    Args:
        config (dict): A dictionary of configuration settings.
        bot (Bot): The bot instance.
        api (API_interface): An API interface for accessing external services.
    """

    def __init__(self, config, bot, api) -> None:
        super().__init__()
        self.config = config
        self.bot = bot
        self.api = api

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        """
        Adds environment variables to the data dictionary and passes control to the next middleware or handler.

        Args:
            handler (Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]]): The next handler or middleware in the chain.
            event (TelegramObject): The incoming event.
            data (Dict[str, Any]): The dialog manager's data dictionary.

        Returns:
            Any: The result of the next handler or middleware in the chain.
        """
        data["config"] = self.config
        data["bot"] = self.bot
        data["api"] = self.api
        return await handler(event, data)
