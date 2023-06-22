# type: ignore
from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, Window, StartMode
from aiogram_dialog.widgets.kbd import Button, Row, SwitchTo, Start
from aiogram_dialog.widgets.text import Const, Format

from bot.database.select_base import get_hotels_by_user_id
from bot.services.api_requests import API_interface
from bot.states import states


async def get_favorites(clb: CallbackQuery, _: Button, manager: DialogManager) -> None:
    session_maker = manager.middleware_data['session']
    await get_hotels_by_user_id(user_id=clb.from_user.id, session_maker=session_maker)


async def select_hotels(clb: CallbackQuery, _: Button, manager: DialogManager) -> None:
    check_in = list(map(int, manager.dialog_data["check_in_date"].split("-")))
    check_out = list(map(int, manager.dialog_data["check_out_date"].split("-")))

    api: API_interface = manager.middleware_data["api"]
    list_hotels: list[tuple[str, str]] = await api.get_list_hotels_id(
        regId=manager.dialog_data["id"],
        sort=clb.data,
        check_in=check_in,
        check_out=check_out,
    )

    if not list_hotels:
        text = "Hotels not found. Please select another city or try again later"
        await clb.answer(text=text, show_alert=True)

    else:
        manager.dialog_data["list_hotels"] = list_hotels
        manager.dialog_data["index"] = 0
        manager.dialog_data.update(await api.get_detail_information(list_hotels[manager.dialog_data["index"]]))
        await manager.switch_to(states.Dialog.HOTELS)


async def get_data(dialog_manager: DialogManager, **kwargs) -> dict[str, Any]:
    return {
        "city": dialog_manager.dialog_data["city"],
        "check_in": dialog_manager.dialog_data["check_in_date"],
        "check_out": dialog_manager.dialog_data["check_out_date"],
    }


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
            Button(Const("Favorites ❤️"), id="favorite", on_click=get_favorites),
            SwitchTo(Const("Settings ⚙️"), id="settings", state=states.Dialog.SETTINGS),
        ),
        Start(Const("Re-entering data again 🗒"), id="start", state=states.Dialog.MAIN, mode=StartMode.RESET_STACK),
        state=states.Dialog.MENU,
        getter=get_data,
    )
