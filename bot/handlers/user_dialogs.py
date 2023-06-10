# type: ignore
from datetime import date
from typing import Any

from aiogram import F, types
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Dialog, DialogManager, ShowMode, Window
from aiogram_dialog.widgets.common import Whenable
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import (
    Button,
    Column,
    ManagedCalendarAdapter,
    Row,
    Select,
    SwitchTo,
)
from aiogram_dialog.widgets.text import Const, Format

from bot.services import api_requests
from bot.services.search_information import Search
from bot.states import states
from bot.utils import (
    MyCalendar,
    check_in_date_validator,
    check_out_date_validator,
    delete_message,
    error_window,
)

# # region Photo
# async def change_photo_counter(
#     clb: CallbackQuery, button: Button, manager: DialogManager
# ) -> None:
#     counter = manager.dialog_data.get("counter", 0)

#     if clb.data == "inc" and 0 <= counter < 5:
#         manager.dialog_data["counter"] = counter + 1
#     elif clb.data == "dec" and 0 < counter <= 5:
#         manager.dialog_data["counter"] = counter - 1


# async def confirm_photo(clb: CallbackQuery, widget, manager: DialogManager) -> None:
#     if clb.data == "no":
#         manager.dialog_data["counter"] = 0

#     manager.dialog_data["settings_complite"] = True
#     await manager.switch_to(SearchHotels.main_menu)


# # endregion Photo


# # region Hotels
# async def select_hotels(
#     clb: CallbackQuery, button: Button, manager: DialogManager
# ) -> None:
#     check_in = list(map(int, manager.dialog_data["check_in_date"].split("-")))
#     check_out = list(map(int, manager.dialog_data["check_out_date"].split("-")))
#     city_id = manager.dialog_data["id"]

#     list_hotels_id: list[str] = search.hotels_list_id(
#         city_id=city_id, sort=clb.data, check_in=check_in, check_out=check_out
#     )

#     if list_hotels_id:
#         manager.dialog_data["list_hotels_id"] = list_hotels_id
#         index = manager.dialog_data.get("index", 0)
#         manager.dialog_data.update(search.detail_information(list_hotels_id[index]))
#         await manager.switch_to(SearchHotels.hotels)

#     else:
#         text = "Hotels not found. Please select another city or try again later"
#         await clb.answer(text=text, show_alert=True)


# async def hotel_pagination(
#     clb: CallbackQuery, button: Button, manager: DialogManager
# ) -> None:
#     index = manager.dialog_data.get("index", 0)
#     list_hotels_id = manager.dialog_data.get("list_hotels_id")
#     # latitude = manager.dialog_data.get('latitude')[0]
#     # longitude = manager.dialog_data.get('longitude')[0]
#     # print(latitude, longitude)

#     if clb.data == "next" and 0 <= index < len(list_hotels_id):
#         index += 1
#     elif clb.data == "prev" and 0 < index <= len(list_hotels_id):
#         index -= 1
#     manager.dialog_data["index"] = index
#     detail_info: dict[str, Any] = search.detail_information(list_hotels_id[index])
#     if detail_info is not None:
#         # await clb.message.answer_location(latitude=latitude, longitude=longitude)
#         manager.dialog_data.update(detail_info)


# # endregion Hotels


# # region Misc
# async def get_data(dialog_manager: DialogManager, **kwargs) -> dict[str, Any]:
#     return {
#         "locations": dialog_manager.dialog_data.get("locations"),
#         "city": dialog_manager.dialog_data.get("city"),
#         "id": dialog_manager.dialog_data.get("id"),
#         "check_in": dialog_manager.dialog_data.get("check_in_date"),
#         "check_out": dialog_manager.dialog_data.get("check_out_date"),
#         "counter": dialog_manager.dialog_data.get("counter", 0),
#         "settings_complite": False,
#         "hotel_name": dialog_manager.dialog_data.get("hotel_name"),
#         "address": dialog_manager.dialog_data.get("address"),
#         "rating": dialog_manager.dialog_data.get("rating"),
#         "users_rating": dialog_manager.dialog_data.get("users_rating")
#         or "No user rating",
#         "around": dialog_manager.dialog_data.get("around"),
#         "about": dialog_manager.dialog_data.get("about"),
#         "photos": dialog_manager.dialog_data.get("photos"),
#         "longitude": dialog_manager.dialog_data.get("longitude"),
#         "latitude": dialog_manager.dialog_data.get("latitude"),
#     }


# def is_settings_not_complite(
#     data: dict, widget: Whenable, manager: DialogManager
# ) -> bool:
#     return manager.dialog_data.get("settings_complite") is not True


# async def go_back(clb: CallbackQuery, button: Button, manager: DialogManager) -> None:
#     await manager.back()


# endregion Misc


def main_dialogs() -> Dialog:
    list_dialogs = [
        # region Request photos
        Window(
            Const("Would you want to download photo?"),
            Row(
                SwitchTo(Const("Yes"), id="yes", state=SearchHotels.count_photo),
                SwitchTo(
                    Const("No"),
                    id="no",
                    state=SearchHotels.main_menu,
                    on_click=confirm_photo,
                ),
            ),
            Button(
                Const("⬅️ Back"),
                id="back",
                on_click=go_back,
                when=is_settings_not_complite,
            ),
            state=SearchHotels.photo_request,
        ),
        # endregion Request photos
        # region Count photo
        #     Window(
        #         Const("Choose the number of photos to upload"),
        #         Row(
        #             Button(Const("-"), id="dec", on_click=change_photo_counter),
        #             Button(Format("{counter}"), id="confirm"),
        #             Button(Const("+"), id="inc", on_click=change_photo_counter),
        #         ),
        #         Row(
        #             Button(Const("⬅️ Back"), id="back", on_click=go_back),
        #             Button(Const("Ok"), id="ok", on_click=confirm_photo),
        #         ),
        #         state=SearchHotels.count_photo,
        #         getter=get_data,
        #     ),
        #     # endregion Count photo

        #     # region Hotels
        #     Window(
        #         Format("Hotel: <b>{hotel_name}</b>\nAddress: <code>{address}</code>\n"),
        #         Format(
        #             "<u>Rating:</u> {rating} ⭐️\n<u>Users rating</u>: {users_rating} 📈\n"
        #         ),
        #         Format("<i>About</i>: {about}\n\n<i>Around</i>: {around}"),
        #         Row(
        #             Button(Const("◀️"), id="prev", on_click=hotel_pagination),
        #             Button(Const("❤️"), id="like"),
        #             Button(Const("▶️"), id="next", on_click=hotel_pagination),
        #         ),
        #         SwitchTo(
        #             Const("⬅️ Back to main menu"), id="main", state=SearchHotels.main_menu
        #         ),
        #         state=SearchHotels.hotels,
        #         getter=get_data,
        #     ),
        #     # endregion Hotels
    ]

    return Dialog(*list_dialogs)
