from aiogram.types import ContentType, Message
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Const, Format

from bot.services import locations_id
from bot.states import states


async def get_data(dialog_manager: DialogManager, **kwargs) -> dict[str, str]:
    return {
        "greeting": ""
        if dialog_manager.dialog_data.get("settings_complite")
        else "Hello. I'm a hotel search assistant."
    }


async def geting_city_ids(
    msg: Message, _: MessageInput, manager: DialogManager
) -> None:
    locations: list[tuple[str, str]] = locations_id(msg.text)

    if locations:
        manager.dialog_data["locations"] = locations
        await manager.switch_to(states.Dialog.CONFIRM_LOCATION)
    else:
        await msg.answer(f"City {msg.text} not found. Please enter a valid location")


def city_request() -> Window:
    return Window(
        Format("{greeting}"),
        Const("Enter the city where you would like to search"),
        MessageInput(geting_city_ids, content_types=[ContentType.TEXT]),
        state=states.Dialog.MAIN,
        getter=get_data,
    )
