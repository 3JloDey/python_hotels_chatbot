from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const, Format

from bot.dialogs.misc import pagination
from bot.dialogs.misc.geolocation import delete_geolocation, load_geolocation
from bot.dialogs.misc.hide_buttons import is_found_location
from bot.services.api_requests import API_interface
from bot.states import states


async def like_hotel(clb: CallbackQuery, _: Button, manager: DialogManager) -> None:
    await clb.answer("Hotel saved!", show_alert=False)


async def search_photos(clb: CallbackQuery, _: Button, manager: DialogManager) -> None:
    manager.dialog_data["index_photo"] = manager.dialog_data.get("index_photo", 0)
    await manager.switch_to(states.Dialog.PHOTOS)


async def back_to_main(clb: CallbackQuery, _: Button, manager: DialogManager) -> None:
    manager.dialog_data["index_photo"] = 0
    await delete_geolocation(manager)
    await manager.switch_to(states.Dialog.MENU)


async def switch_hotels(clb: CallbackQuery, _: Button, manager: DialogManager) -> None:
    await delete_geolocation(manager)
    list_hotels = manager.dialog_data["list_hotels"]
    index = await pagination(clb, manager.dialog_data["index"], list_hotels)

    manager.dialog_data["index"] = index
    manager.dialog_data["index_photo"] = 0
    api: API_interface = manager.middleware_data["api"]
    detail_info: dict[str, Any] = await api.get_detail_information(list_hotels[index])
    manager.dialog_data.update(detail_info)


async def get_data(dialog_manager: DialogManager, **kwargs) -> dict[str, Any]:
    return {
        "hotel_name": dialog_manager.dialog_data["hotel_name"],
        "address": dialog_manager.dialog_data["address"],
        "rating": dialog_manager.dialog_data["rating"],
        "users_rating": dialog_manager.dialog_data["users_rating"],
        "price": dialog_manager.dialog_data["price"],
        "about": dialog_manager.dialog_data["about"],
        "around": dialog_manager.dialog_data["around"],
    }


def get_hotels() -> Window:
    return Window(
        Format(
            "Hotel: <b>{hotel_name}</b>\nAddress: <code>{address}</code>\n\n"
            "<u>Rating:</u> {rating} ⭐️\n<u>Users rating:</u> {users_rating} 📈\n<u>Price:</u> {price}\n\n"
            "<i>About:</i> {about}\n\n<i>Around:</i> {around}"
        ),
        Row(
            Button(Const("◀️ Prev"), id="prev", on_click=switch_hotels),
            Button(Const("Like ❤️"), id="like", on_click=like_hotel),
            Button(Const("Next ▶️"), id="next", on_click=switch_hotels),
        ),
        Row(
            Button(
                Const("Search Photos 📸"),
                id="photos",
                on_click=search_photos,
            ),
            Button(
                Const("Send geolocation 🗺"),
                id="location",
                on_click=load_geolocation,
                when=is_found_location,
            ),
        ),
        Button(Const("⬅️ Back to main menu"), id="main", on_click=back_to_main),
        state=states.Dialog.HOTELS,
        getter=get_data,
    )
