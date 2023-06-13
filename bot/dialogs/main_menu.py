# type: ignore
from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Row, SwitchTo
from aiogram_dialog.widgets.text import Const, Format

from bot.services.api_requests import detail_information, get_list_hotels_id
from bot.states import states


async def get_data(dialog_manager: DialogManager, **kwargs) -> dict[str, Any]:
    return {
        "city": dialog_manager.dialog_data["city"],
        "check_in": dialog_manager.dialog_data["check_in_date"],
        "check_out": dialog_manager.dialog_data["check_out_date"],
    }


async def select_hotels(clb: CallbackQuery, _: Button, manager: DialogManager) -> None:
    check_in: list[int] = list(map(int, manager.dialog_data["check_in_date"].split("-")))
    check_out: list[int] = list(map(int, manager.dialog_data["check_out_date"].split("-")))
    list_hotels: list[str] = get_list_hotels_id(
        id=manager.dialog_data["id"],
        sort=clb.data,
        check_in=check_in,
        check_out=check_out,
    )

    if not list_hotels:
        text = "Hotels not found. Please select another city or try again later"
        await clb.answer(text=text, show_alert=True)

    else:
        manager.dialog_data["list_hotels"] = list_hotels
        index = manager.dialog_data.get("index", 0)
        manager.dialog_data.update(detail_information(list_hotels[index]))
        await manager.switch_to(states.Dialog.HOTELS)


def main_menu() -> Window:
    return Window(
        Format("City: {city}\nCheck in: {check_in}\nCheck out: {check_out}"),
        Row(
            Button(
                Const("Lower Price 💸"), id="PRICE_LOW_TO_HIGH", on_click=select_hotels
            ),
            Button(
                Const("Hight price 💰"), id="PRICE_HIGH_TO_LOW", on_click=select_hotels
            ),
            Button(Const("Best deal 🔥"), id="PRICE_RELEVANT", on_click=select_hotels),
        ),
        Row(
            Button(Const("History 📜"), id="history"),
            SwitchTo(Const("Settings 🛠"), id="settings", state=states.Dialog.SETTINGS),
        ),
        state=states.Dialog.MENU,
        getter=get_data,
    )
