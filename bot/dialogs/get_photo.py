from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Const, Format

from bot.dialogs.misc.back import go_back
from bot.dialogs.misc import pagination
from bot.states import states


async def switch_photo(clb: CallbackQuery, _: Button, manager: DialogManager) -> None:
    """
    Asynchronous function that switches the current photo displayed in the UI.

    Args:
        clb: A CallbackQuery object.
        _: A Button object (unused).
        manager: A DialogManager object.

    Returns:
        None
    """
    index = await pagination(clb, manager.dialog_data["index_photo"], manager.dialog_data["photos"])
    manager.dialog_data["index_photo"] = index
    manager.dialog_data["current_photo"] = manager.dialog_data["photos"][index]


async def get_data(dialog_manager: DialogManager, **kwargs) -> dict[str, Any]:
    """
    Asynchronous function that returns a dictionary of data to be displayed in the UI.

    Args:
        dialog_manager: A DialogManager object.
        **kwargs: Additional keyword arguments.

    Returns:
        A dictionary containing information about the current photo and counter.
    """
    return {
        "current_photo": dialog_manager.dialog_data["photos"][dialog_manager.dialog_data["index_photo"]],
        "current_counter": dialog_manager.dialog_data["index_photo"] + 1,
        "max_counter": len(dialog_manager.dialog_data["photos"]),
    }


def get_photo() -> Window:
    """
    Function that returns a window containing information about the current photo and buttons to navigate through them.

    Returns:
        A Window object containing the photo UI.
    """
    return Window(
        StaticMedia(url=Format("{current_photo[0]}")),
        Format("<b>{current_photo[1]}</b>"),
        Row(
            Button(Const("◀️ Prev"), id="prev", on_click=switch_photo),
            Button(Format("{current_counter}/{max_counter}"), id="count"),
            Button(Const("Next ▶️"), id="next", on_click=switch_photo),
        ),
        Button(
            Const("⬅️ Back"),
            id="back",
            on_click=go_back,
        ),
        state=states.Dialog.PHOTOS,
        getter=get_data,
    )
