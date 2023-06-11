from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const, Format

from bot.dialogs.misc import is_photo
from bot.dialogs.misc.geolocation import delete_geolocation, load_geolocation
from bot.services import detail_information
from bot.states import states


async def search_photos(clb: CallbackQuery, _: Button, manager: DialogManager) -> None:
    await delete_geolocation(manager)
    await manager.switch_to(states.Dialog.PHOTOS)


async def back_to_main(clb: CallbackQuery, _: Button, manager: DialogManager) -> None:
    await delete_geolocation(manager)
    await manager.switch_to(states.Dialog.MENU)


async def pagination(clb: CallbackQuery, _: Button, manager: DialogManager) -> None:
    await delete_geolocation(manager)
    index = manager.dialog_data.get("index", 0)
    list_hotels_id = manager.dialog_data["list_hotels_id"]

    if clb.data == "next" and 0 <= index < len(list_hotels_id) - 1:
        index += 1
    elif clb.data == "prev" and 0 < index <= len(list_hotels_id) - 1:
        index -= 1
    manager.dialog_data["index"] = index
    manager.dialog_data['index_p'] = 0
    detail_info: dict[str, Any] = detail_information(list_hotels_id[index])
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
            "Hotel: <b>{hotel_name}</b>\nAddress: <code>{address}</code>\n"
            "<u>Rating:</u> {rating} ⭐️\n<u>Users rating:</u> {users_rating} 📈\n<u>Price:</u> {price}\n\n"
            "<i>About:</i> {about}\n\n<i>Around:</i> {around}"
        ),
        Row(
            Button(Const("◀️ Prev"), id="prev", on_click=pagination),
            Button(Const("Like ❤️"), id="like"),
            Button(Const("Next ▶️"), id="next", on_click=pagination),
        ),
        Row(
            Button(
                Const("Search Photos 📸"),
                id="photos",
                on_click=search_photos,
                when=is_photo,
            ),
            Button(
                Const("Send geolocation 🗺"), id="location", on_click=load_geolocation
            ),
        ),
        Button(Const("⬅️ Back to main menu"), id="main", on_click=back_to_main),
        state=states.Dialog.HOTELS,
        getter=get_data,
    )
