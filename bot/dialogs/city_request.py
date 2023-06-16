# type: ignore
from aiogram.types import ContentType, Message
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Const, Format

from bot.services.api_requests import API_interface
from bot.states import states


async def get_data(dialog_manager: DialogManager, **kwargs) -> dict[str, str]:
    """
    Gets data from the dialog manager.

    Args:
        dialog_manager (DialogManager): The dialog manager to get data from.
        **kwargs: Additional keyword arguments.

    Returns:
        dict[str, str]: A dictionary of data.
    """
    return {
        "greeting": ""
        if dialog_manager.dialog_data.get("settings_complite")
        else "Hello. I'm a hotel search assistant."
    }


async def geting_city_ids(
    msg: Message, _: MessageInput, manager: DialogManager
) -> None:
    """
    Gets city IDs from an API and saves them to the dialog manager.

    Args:
        msg (Message): The message containing the user's input.
        _: MessageInput: Unused argument.
        manager (DialogManager): The dialog manager to save data to.

    Returns:
        None
    """
    api: API_interface = manager.middleware_data["api"]
    locations: list[tuple[str, str]] = api.get_variants_locations(msg.text)

    if locations:
        manager.dialog_data["locations"] = locations
        await manager.switch_to(states.Dialog.CONFIRM_LOCATION)
    else:
        await msg.answer(f"City {msg.text} not found. Please enter a valid location")


def city_request() -> Window:
    """
    Creates a window for requesting the user's desired city.

    Returns:
        Window: A window for requesting the user's desired city.
    """
    return Window(
        Format("{greeting}"),
        Const("Enter the city where you would like to search"),
        MessageInput(geting_city_ids, content_types=[ContentType.TEXT]),
        state=states.Dialog.MAIN,
        getter=get_data,
    )
