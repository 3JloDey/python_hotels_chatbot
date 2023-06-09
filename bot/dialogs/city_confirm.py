from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Column, Select
from aiogram_dialog.widgets.text import Const, Format

from bot.states import states


async def get_data(dialog_manager: DialogManager, **kwargs) -> dict[str, str]:
    return {"locations": dialog_manager.dialog_data["locations"]}


async def save_data(clb: CallbackQuery, _: Any, manager: DialogManager, item_id: str) -> None:
    manager.dialog_data["city"] = dict(manager.dialog_data["locations"]).get(item_id)
    manager.dialog_data["id"] = item_id

    if manager.dialog_data.get("settings_complite") is True:
        return await manager.switch_to(states.Main.MENU)
    await manager.switch_to(states.Settings.CHECK_IN)


def city_confirm() -> Window:
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
        state=states.Settings.CONFIRM_LOCATION,
        getter=get_data,
    )
