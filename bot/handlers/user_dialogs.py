# type: ignore
from datetime import date
from typing import Any

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

from bot.services.search_information import Search
from bot.states.user_states import SearchHotels
from bot.utils import (
    MyCalendar,
    check_in_date_validator,
    check_out_date_validator,
    delete_message,
    error_window,
)

search = Search()


# region City
async def get_city_from_user(
    msg: Message, widget: MessageInput, manager: DialogManager
) -> None:
    manager.show_mode = ShowMode.EDIT
    await delete_message(manager, msg)

    locations: list[tuple] = search.locations_id(msg.text)

    if locations:
        manager.dialog_data["locations"] = locations
        await manager.switch_to(SearchHotels.select_location)
    else:
        text = f"City {msg.text} not found. Please enter a valid location"
        msg = await msg.answer(text=text)
        manager.dialog_data["msg"] = msg


async def confirm_city(
    clb: CallbackQuery, widget: Any, manager: DialogManager, item_id: str
) -> None:
    location = dict(manager.dialog_data["locations"]).get(item_id)
    manager.dialog_data["city"] = location
    manager.dialog_data["id"] = item_id

    if manager.dialog_data.get("settings_complite"):
        return await manager.switch_to(SearchHotels.main_menu)
    await manager.switch_to(SearchHotels.check_in_date)


#  endregion City


# region Date
async def get_check_in_date(
    clb: CallbackQuery,
    widget: ManagedCalendarAdapter,
    manager: DialogManager,
    selected_date: date,
) -> None:
    selected_date_str = str(selected_date)
    if check_in_date_validator(manager, selected_date_str) is False:
        await error_window(clb, selected_date_str)
    else:
        manager.dialog_data["check_in_date"] = selected_date_str
        if manager.dialog_data.get("settings_complite"):
            return await manager.switch_to(SearchHotels.main_menu)

        await manager.switch_to(SearchHotels.check_out_date)


async def get_check_out_date(
    clb: CallbackQuery,
    widget: ManagedCalendarAdapter,
    manager: DialogManager,
    selected_date: date,
) -> None:
    selected_date_str = str(selected_date)
    if check_out_date_validator(manager, selected_date_str) is False:
        await error_window(clb, selected_date_str)
    else:
        manager.dialog_data["check_out_date"] = selected_date_str
        if manager.dialog_data.get("settings_complite"):
            return await manager.switch_to(SearchHotels.main_menu)

        await manager.switch_to(SearchHotels.photo_request)


# endregion Date


# region Photo
async def change_photo_counter(
    clb: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    counter = manager.dialog_data.get("counter", 0)

    if clb.data == "inc" and 0 <= counter < 5:
        manager.dialog_data["counter"] = counter + 1
    elif clb.data == "dec" and 0 < counter <= 5:
        manager.dialog_data["counter"] = counter - 1


async def confirm_photo(clb: CallbackQuery, widget, manager: DialogManager) -> None:
    if clb.data == "no":
        manager.dialog_data["counter"] = 0

    manager.dialog_data["settings_complite"] = True
    await manager.switch_to(SearchHotels.main_menu)


# endregion Photo


# region Hotels
async def select_hotels(clb: CallbackQuery, button: Button, manager: DialogManager) -> None:
    check_in = list(map(int, manager.dialog_data["check_in_date"].split('-')))
    check_out = list(map(int, manager.dialog_data["check_out_date"].split('-')))
    city_id = manager.dialog_data["id"]

    list_hotels_id: list[str] = search.hotels_list_id(
        city_id=city_id, sort=clb.data, check_in=check_in, check_out=check_out
            )

    if list_hotels_id:
        manager.dialog_data["list_hotels_id"] = list_hotels_id
        index = manager.dialog_data.get("index", 0)
        manager.dialog_data.update(search.detail_information(list_hotels_id[index]))
        await manager.switch_to(SearchHotels.hotels)
    else:
        text = "Hotels not found. Please select another city or try again later"
        await clb.answer(text=text, show_alert=True)


async def hotel_pagination(clb: CallbackQuery, button: Button, manager: DialogManager) -> None:
    manager.dialog_data["index"] = manager.dialog_data.get("index", 0)
    index = manager.dialog_data["index"]
    list_hotels_id = manager.dialog_data.get("list_hotels_id")

    if clb.data == "next" and 0 <= index < len(list_hotels_id):
        index += 1
    elif clb.data == "prev" and 0 < index <= len(list_hotels_id):
        index -= 1

    manager.dialog_data["index"] = index
    detail_info: dict[str, Any] = search.detail_information(list_hotels_id[index])
    if detail_info is not None:
        manager.dialog_data.update(detail_info)


# endregion Hotels


# region Misc
async def get_data(dialog_manager: DialogManager, **kwargs) -> dict[str, Any]:
    return {
        "locations": dialog_manager.dialog_data.get("locations"),
        "city": dialog_manager.dialog_data.get("city"),
        "id": dialog_manager.dialog_data.get("id"),
        "check_in": dialog_manager.dialog_data.get("check_in_date"),
        "check_out": dialog_manager.dialog_data.get("check_out_date"),
        "counter": dialog_manager.dialog_data.get("counter", 0),
        "settings_complite": False,
        "hotel_name": dialog_manager.dialog_data.get("hotel_name"),
        "address": dialog_manager.dialog_data.get("address"),
        "rating": dialog_manager.dialog_data.get("rating"),
        'users_rating': dialog_manager.dialog_data.get("users_rating") or 'No user rating',
        'around': dialog_manager.dialog_data.get('around'),
        'about': dialog_manager.dialog_data.get('about'),
    }


def is_settings_not_complite(
    data: dict, widget: Whenable, manager: DialogManager
) -> bool:
    return manager.dialog_data.get("settings_complite") is not True


async def go_back(clb: CallbackQuery, button: Button, manager: DialogManager) -> None:
    await manager.back()


# endregion Misc


def main_dialogs() -> Dialog:
    list_dialogs = [
        # region Greeting
        Window(
            Const("Hello this is assisten to find hotels"),
            SwitchTo(Const("Enter city"), id="start", state=SearchHotels.city_request),
            state=SearchHotels.start,
        ),
        # endregion Greeting
        # region City request
        Window(
            Const("Enter city when you want to search hotels"),
            MessageInput(get_city_from_user),
            state=SearchHotels.city_request,
        ),
        # endregion City request
        # region Select Location
        Window(
            Const("Please, select location"),
            Column(
                Select(
                    Format("{item[1]}"),
                    items="locations",
                    item_id_getter=lambda x: x[0],
                    on_click=confirm_city,
                    id="s_location",
                )
            ),
            state=SearchHotels.select_location,
            getter=get_data,
        ),
        # endregion Select Location
        # region Check in
        Window(
            Const("Select check in date"),
            MyCalendar(id="check_in", on_click=get_check_in_date),
            Button(
                Const("⬅️ Back"),
                id="back",
                on_click=go_back,
                when=is_settings_not_complite,
            ),
            state=SearchHotels.check_in_date,
        ),
        # endregion Check in
        # region Check out
        Window(
            Const("Select check out date"),
            MyCalendar(id="check_out", on_click=get_check_out_date),
            Button(
                Const("⬅️ Back"),
                id="back",
                on_click=go_back,
                when=is_settings_not_complite,
            ),
            state=SearchHotels.check_out_date,
        ),
        # endregion Check out
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
        Window(
            Const("Choose the number of photos to upload"),
            Row(
                Button(Const("-"), id="dec", on_click=change_photo_counter),
                Button(Format("{counter}"), id="confirm"),
                Button(Const("+"), id="inc", on_click=change_photo_counter),
            ),
            Row(
                Button(Const("⬅️ Back"), id="back", on_click=go_back),
                Button(Const("Ok"), id="ok", on_click=confirm_photo),
            ),
            state=SearchHotels.count_photo,
            getter=get_data,
        ),
        # endregion Count photo
        # region Main menu
        Window(
            Format(
                "City: {city}\nCheck in: {check_in}\nCheck out: {check_out}\nCount photo: {counter}"
            ),
            Row(
                Button(Const("Lower Price"), id="PRICE_LOW_TO_HIGH", on_click=select_hotels),
                Button(Const("Hight price"), id="PRICE_HIGH_TO_LOW", on_click=select_hotels),
                Button(Const("Best deal"), id="PRICE_RELEVANT", on_click=select_hotels),
            ),
            Row(
                Button(Const("History"), id="history"),
                SwitchTo(Const("Setting"), id="settings", state=SearchHotels.settings),
            ),
            state=SearchHotels.main_menu,
            getter=get_data,
        ),
        # endregion Main menu
        # region Settings
        Window(
            Const("Settings menu"),
            Row(
                SwitchTo(
                    Const("Change city"),
                    id="change_city",
                    state=SearchHotels.city_request,
                ),
                SwitchTo(
                    Const("Change count of photos"),
                    id="change_photo",
                    state=SearchHotels.photo_request,
                ),
            ),
            Row(
                SwitchTo(
                    Const("Change check in date"),
                    id="change_check_in",
                    state=SearchHotels.check_in_date,
                ),
                SwitchTo(
                    Const("Change check out date"),
                    id="change_check_out",
                    state=SearchHotels.check_out_date,
                ),
            ),
            Button(Const("Back"), id="back", on_click=go_back),
            state=SearchHotels.settings,
        ),
        # endregion Settings
        # region Hotels
        Window(
            Format("Hotel: <b>{hotel_name}</b>\nAddress: <code>{address}</code>\n"),
            Format("<u>Rating:</u> {rating} ⭐️\n<u>Users rating</u>: {users_rating} 📈\n"),
            Format('<i>About</i>: {about}\n\n<i>Around</i>: {around}'),
            Row(
                Button(Const("◀️"), id="prev", on_click=hotel_pagination),
                Button(Const("❤️"), id="like"),
                Button(Const("▶️"), id="next", on_click=hotel_pagination),
            ),
            SwitchTo(
                Const("⬅️ Back to main menu"), id="main", state=SearchHotels.main_menu
            ),
            state=SearchHotels.hotels,
            getter=get_data,
        )
        # endregion Hotels
    ]

    return Dialog(*list_dialogs)
