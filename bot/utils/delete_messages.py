from contextlib import suppress

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message
from aiogram_dialog import DialogManager


async def delete_message(
    manager: DialogManager, message_from_user: Message | None = None
) -> None:
    with suppress(TelegramBadRequest):
        message_from_bot = manager.dialog_data.get("msg")
        if message_from_bot is not None:
            await manager.dialog_data["msg"].delete()
        if message_from_user is not None:
            await message_from_user.delete()
