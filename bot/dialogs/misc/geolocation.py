from contextlib import suppress
from typing import Any

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager


async def load_geolocation(clb: CallbackQuery, _: Any, manager: DialogManager) -> None:
    if isinstance(clb.message, Message):
        latitude = manager.dialog_data["latitude"]
        longitude = manager.dialog_data["longitude"]
        location = await clb.message.answer_location(
            latitude=latitude, longitude=longitude, disable_notification=True
        )
        manager.dialog_data["message_id"] = location.message_id
        manager.dialog_data["chat_id"] = location.chat.id


async def delete_geolocation(manager: DialogManager) -> None:
    with suppress(TelegramBadRequest):
        location = manager.dialog_data.get("message_id")
        if location is not None:
            chat_id = manager.dialog_data["chat_id"]
            message_id = manager.dialog_data["message_id"]
            bot = manager.middleware_data["bot"]
            await bot.delete_message(chat_id=chat_id, message_id=message_id)
