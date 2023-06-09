from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const, Format

from bot.database import add_hotel_to_favorite, delete_from_db, upload_hotels_from_db
from bot.dialogs.misc import pagination
from bot.dialogs.misc.geolocation import delete_geolocation, load_geolocation
from bot.dialogs.misc.hide_buttons import dislike, is_found_location, like
from bot.states import states


async def dislike_hotel(clb: CallbackQuery, _: Button, manager: DialogManager) -> None:
    """
    Asynchronous function that deletes the current hotel from user's favorites and updates the UI accordingly.

    Args:
        clb: A CallbackQuery object.
        _: A Button object (unused).
        manager: A DialogManager object.

    Returns:
        None
    """
    user_id = clb.from_user.id
    hotel_name = manager.dialog_data["hotel_name"]
    session_maker = manager.middleware_data["session"]

    # Delete from favorite
    await delete_from_db(
        user_id=user_id, hotel_name=hotel_name, session_maker=session_maker
    )
    await clb.answer("Hotel deleted successfully")

    # Update data
    list_hotels = await upload_hotels_from_db(
        user_id=user_id, session_maker=session_maker
    )
    
    if len(list_hotels) == 0:
        manager.dialog_data["is_favorite"] = False
        await manager.switch_to(states.Dialog.MENU)
    else:
        index = await pagination(clb, manager.dialog_data.get("index_hotel", 0), list_hotels)
   
        manager.dialog_data["index_hotel"] = index % len(list_hotels)
        manager.dialog_data["list_hotels"] = list_hotels
        manager.dialog_data.update(list_hotels[manager.dialog_data["index_hotel"]])


async def like_hotel(clb: CallbackQuery, _: Button, manager: DialogManager) -> None:
    """
    Asynchronous function that adds the current hotel to user's favorites and updates the UI accordingly.

    Args:
        clb: A CallbackQuery object.
        _: A Button object (unused).
        manager: A DialogManager object.

    Returns:
        None
    """
    async_session = manager.middleware_data["session"]
    await add_hotel_to_favorite(clb, manager, async_session)
    await clb.answer("Hotel saved!", show_alert=False)


async def search_photos(clb: CallbackQuery, _: Button, manager: DialogManager) -> None:
    """
    Asynchronous function that switches to the photos UI.

    Args:
        clb: A CallbackQuery object.
        _: A Button object (unused).
        manager: A DialogManager object.

    Returns:
        None
    """
    manager.dialog_data["index_photo"] = manager.dialog_data.get("index_photo", 0)
    await manager.switch_to(states.Dialog.PHOTOS)


async def back_to_main(clb: CallbackQuery, _: Button, manager: DialogManager) -> None:
    """
    Asynchronous function that switches back to the main menu and resets relevant dialog data.

    Args:
        clb: A CallbackQuery object.
        _: A Button object (unused).
        manager: A DialogManager object.

    Returns:
        None
    """
    manager.dialog_data["index_hotel"] = 0
    manager.dialog_data["index_photo"] = 0
    manager.dialog_data["is_favorite"] = False
    await delete_geolocation(manager)
    await manager.switch_to(states.Dialog.MENU)


async def switch_hotels(clb: CallbackQuery, _: Button, manager: DialogManager) -> None:
    """
    Asynchronous function that switches to the next or previous hotel in the list and updates the UI accordingly.

    Args:
        clb: A CallbackQuery object.
        _: A Button object (unused).
        manager: A DialogManager object.

    Returns:
        None
    """
    await delete_geolocation(manager)
    list_hotels = manager.dialog_data["list_hotels"]
    index = await pagination(
        clb, manager.dialog_data.get("index_hotel", 0), list_hotels
    )

    manager.dialog_data["index_hotel"] = index
    manager.dialog_data["index_photo"] = 0

    if manager.dialog_data.get("is_favorite"):
        manager.dialog_data.update(list_hotels[index])

    else:
        api = manager.middleware_data["api"]
        detail_info = await api.get_detail_information(list_hotels[index])
        manager.dialog_data.update(detail_info)


async def get_data(dialog_manager: DialogManager, **kwargs) -> dict[str, Any]:
    """
    Asynchronous function that returns a dictionary of data to be displayed in the UI.

    Args:
        dialog_manager: A DialogManager object.
        **kwargs: Additional keyword arguments.

    Returns:
        A dictionary containing information about the current hotel.
    """
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
    """
    Function that returns a window containing information about the current hotel and buttons to navigate through them.

    Returns:
        A Window object containing the hotel UI.
    """
    return Window(
        Format(
            "Hotel: <b>{hotel_name}</b>\nAddress: <code>{address}</code>\n\n"
            "<u>Rating:</u> {rating} ⭐️\n<u>Users rating:</u> {users_rating} 📈\n<u>Price:</u> {price}\n\n"
            "<i>About:</i> {about}\n\n<i>Around:</i> {around}"
        ),
        Row(
            Button(Const("◀️ Prev"), id="prev", on_click=switch_hotels),
            Button(Const("Like ❤️"), id="like", on_click=like_hotel, when=like),
            Button(
                Const("Dislike 💔"), id="dislike", on_click=dislike_hotel, when=dislike
            ),
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
