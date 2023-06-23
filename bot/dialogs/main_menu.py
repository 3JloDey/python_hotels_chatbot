# type: ignore
from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode, Window
from aiogram_dialog.widgets.kbd import Button, Row, Start, SwitchTo
from aiogram_dialog.widgets.text import Const, Format

from bot.database import upload_hotels_from_db
from bot.states import states


async def get_favorites(clb: CallbackQuery, _: Button, manager: DialogManager) -> None:
    """
    Async function that retrieves the user's favorite hotels and switches to the HOTELS state.

    Args:
        clb (CallbackQuery): The callback query object.
        _ (Button): The button object.
        manager (DialogManager): The dialog manager object.

    Returns:
        None
    """
    session_maker = manager.middleware_data["session"]
    list_hotels = await upload_hotels_from_db(
        user_id=clb.from_user.id, session_maker=session_maker
    )
    if len(list_hotels) > 0:
        manager.dialog_data["is_favorite"] = True
        manager.dialog_data["list_hotels"] = list_hotels
        manager.dialog_data.update(list_hotels[0])
        await manager.switch_to(states.Dialog.HOTELS)
    else:
        await clb.answer("Favorites not found", show_alert=True)


async def hotel_selection(
    clb: CallbackQuery, _: Button, manager: DialogManager
) -> None:
    """
    Async function that retrieves the list of hotels and switches to the HOTELS state.

    Args:
        clb (CallbackQuery): The callback query object.
        _ (Button): The button object.
        manager (DialogManager): The dialog manager object.

    Returns:
        None
    """
    api = manager.middleware_data["api"]
    list_hotels = await api.get_list_hotels_id(
        regId=manager.dialog_data["id"],
        sort=clb.data,
        check_in=manager.dialog_data["check_in_date"],
        check_out=manager.dialog_data["check_out_date"],
    )

    if len(list_hotels) > 0:
        manager.dialog_data["list_hotels"] = list_hotels
        manager.dialog_data.update(await api.get_detail_information(list_hotels[0]))
        await manager.switch_to(states.Dialog.HOTELS)

    else:
        text = "Hotels not found. Please select another city or try again later"
        await clb.answer(text=text, show_alert=True)


async def get_data(dialog_manager: DialogManager, **kwargs) -> dict[str, Any]:
    """
    Async function that retrieves the necessary data from the dialog manager.

    Args:
        dialog_manager (DialogManager): The dialog manager object.
        **kwargs: Additional keyword arguments.

    Returns:
        A dictionary containing the city, check-in and check-out dates.
    """
    return {
        "city": dialog_manager.dialog_data["city"],
        "check_in_date": dialog_manager.dialog_data["check_in_date"],
        "check_out_date": dialog_manager.dialog_data["check_out_date"],
    }


def main_menu() -> Window:
    """
    Function that returns the main menu window with buttons for different options.

    Returns:
        A Window object containing the main menu UI.
    """
    return Window(
        Format("City: {city}\nCheck in: {check_in_date}\nCheck out: {check_out_date}"),
        Row(
            Button(
                Const("Low Price 💸"),
                id="PRICE_LOW_TO_HIGH",
                on_click=hotel_selection,
            ),
            Button(
                Const("High Price 💰"),
                id="PRICE_HIGH_TO_LOW",
                on_click=hotel_selection,
            ),
            Button(
                Const("Best Deal 🔥"),
                id="PRICE_RELEVANT",
                on_click=hotel_selection,
            ),
        ),
        Row(
            Button(Const("Favorites ❤️"), id="favorite", on_click=get_favorites),
            SwitchTo(Const("Settings ⚙️"), id="settings", state=states.Dialog.SETTINGS),
        ),
        Start(
            Const("Re-enter data 🗒"),
            id="start",
            state=states.Dialog.MAIN,
            mode=StartMode.RESET_STACK,
        ),
        state=states.Dialog.MENU,
        getter=get_data,
    )
