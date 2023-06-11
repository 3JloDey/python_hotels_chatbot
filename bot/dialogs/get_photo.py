from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Const, Format

from bot.dialogs.misc import go_back
from bot.states import states


async def pagination(clb: CallbackQuery, _: Button, manager: DialogManager) -> None:
    index = manager.dialog_data.get("index_p", 0)
    count_photos = len(manager.dialog_data["photos"])
    if count_photos > 1:
        index = manager.dialog_data.get("index_p", 0)

        if clb.data == "next" and 0 <= index < count_photos - 1:
            index += 1
        elif clb.data == "prev" and 0 < index <= count_photos - 1:
            index -= 1
        manager.dialog_data["index_p"] = index
        manager.dialog_data['current_photo'] = manager.dialog_data['photos'][index]


async def get_data(dialog_manager: DialogManager, **kwargs) -> dict[str, Any]:
    return {
        "photos": dialog_manager.dialog_data["photos"],
        "current_photo": dialog_manager.dialog_data["photos"][dialog_manager.dialog_data.get('index_p', 0)],
    }


def get_photo() -> Window:
    return Window(
        StaticMedia(url=Format("{current_photo[0]}")),
        Format("<b>{current_photo[1]}</b>"),
        Row(
            Button(Const("◀️ Prev"), id="prev", on_click=pagination),
            Button(Const("Next ▶️"), id="next", on_click=pagination),
        ),
        Button(
            Const("⬅️ Back"),
            id="back",
            on_click=go_back,
        ),
        state=states.Dialog.PHOTOS,
        getter=get_data,
    )
