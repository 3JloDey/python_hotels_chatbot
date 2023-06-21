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
    index = await pagination(clb, manager.dialog_data["index_photo"], manager.dialog_data["photos"])
    manager.dialog_data["index_photo"] = index
    manager.dialog_data["current_photo"] = manager.dialog_data["photos"][index]


async def get_data(dialog_manager: DialogManager, **kwargs) -> dict[str, Any]:
    return {
        "current_photo": dialog_manager.dialog_data["photos"][dialog_manager.dialog_data["index_photo"]],
        "current_counter": dialog_manager.dialog_data["index_photo"] + 1,
        "max_counter": len(dialog_manager.dialog_data["photos"]),
    }


def get_photo() -> Window:
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
