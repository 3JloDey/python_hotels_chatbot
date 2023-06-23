from typing import Any, Awaitable, Callable, Coroutine, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message


class PrivatOnlyMiddleware(BaseMiddleware):
    """
    Middleware that allows only private chat events to pass through.

    Attributes:
        None
    """
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Coroutine[Any, Any, Any] | None:
        """
            Calls the handler if the event is a private chat event.

            Args:
                handler (Callable): The handler function.
                event (Message): The event object.
                data (Dict): Additional data.

            Returns:
                awaitable: The result of calling the handler, or None.
            """
        if event.chat.type == "private":
            return await handler(event, data)
