from typing import Any, Awaitable, Callable, Coroutine, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message


class PrivatOnlyMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Coroutine[Any, Any, Any] | None:
        if event.chat.type == "private":
            return await handler(event, data)
