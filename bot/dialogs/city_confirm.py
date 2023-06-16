from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Column, Select
from aiogram_dialog.widgets.text import Const, Format

from bot.states import states


async def get_data(dialog_manager: DialogManager, **kwargs) -> dict[str, str]:
    """
    Retrieves data from the dialog manager.

    Args:
        dialog_manager (DialogManager): The dialog manager to retrieve data from.
        **kwargs: Additional keyword arguments.

    Returns:
        dict[str, str]: A dictionary containing the retrieved data.
    """
    return {"locations": dialog_manager.dialog_data["locations"]}


async def save_data(
    clb: CallbackQuery, _: Any, manager: DialogManager, item_id: str
) -> None:
    """
    Saves data to the dialog manager.

    Args:
        clb (CallbackQuery): The callback query.
        _: Any: Unused argument.
        manager (DialogManager): The dialog manager to save data to.
        item_id (str): The ID of the selected item.

    Returns:
        None
    """
    manager.dialog_data["city"] = dict(manager.dialog_data["locations"]).get(item_id)
    manager.dialog_data["id"] = item_id

    if manager.dialog_data.get("settings_complite") is True:
        return await manager.switch_to(states.Dialog.MENU)
    await manager.switch_to(states.Dialog.CHECK_IN)


def city_confirm() -> Window:
    """
    Creates a window for confirming the user's location.

    Returns:
        Window: A window for confirming the user's location.
    """
    return Window(
        Const("Please, specify the location"),
        Column(
            Select(
                Format("{item[1]}"),
                items="locations",
                item_id_getter=lambda x: x[0],
                on_click=save_data,
                id="s_location",
            )
        ),
        state=states.Dialog.CONFIRM_LOCATION,
        getter=get_data,
    )
