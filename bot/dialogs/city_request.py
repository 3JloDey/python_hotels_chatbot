from aiogram.types import ContentType, Message
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Const

from bot.services import locations_id
from bot.states import states


async def geting_city_ids(
    msg: Message, _: MessageInput, manager: DialogManager
) -> None:
    locations: list[tuple] = locations_id(msg.text)

    if locations:
        manager.dialog_data["locations"] = locations
        await manager.switch_to(states.Settings.CONFIRM_LOCATION)
    else:
        await msg.answer(f"City {msg.text} not found. Please enter a valid location")


def city_request() -> Window:
    return Window(
        Const(
            "Hello. I'm a hotel search assistant.\n"
            "Enter the city where you would like to search"
        ),
        MessageInput(geting_city_ids, content_types=[ContentType.TEXT]),
        state=states.Settings.MAIN,
    )
