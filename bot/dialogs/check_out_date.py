from datetime import date

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, ManagedCalendarAdapter
from aiogram_dialog.widgets.text import Const

from bot.dialogs.misc.back import go_back
from bot.dialogs.misc.calendar import CustomCalendar
from bot.dialogs.misc.hide_buttons import is_settings_not_complite
from bot.states import states
from bot.utils.date_validation import check_out_date_validator, validation_error


async def date_confirm(
    clb: CallbackQuery,
    _: ManagedCalendarAdapter,
    manager: DialogManager,
    selected_date: date,
) -> None:
    """
    Handles the confirmation of a selected date in the check-out calendar.

    Args:
        clb (CallbackQuery): The aiogram CallbackQuery object.
        _: (ManagedCalendarAdapter): The adapter for the managed calendar.
        manager (DialogManager): The aiogram DialogManager object.
        selected_date (date): The selected date as a Python date object.

    Returns:
        None
    """
    date = str(selected_date)
    if check_out_date_validator(manager, date) is False:
        await validation_error(clb, date)
    else:
        manager.dialog_data["settings_complite"] = True
        manager.dialog_data["check_out_date"] = date
        await manager.switch_to(states.Dialog.MENU)


def check_out_date() -> Window:
    """
    Creates a window for selecting the check-out date.

    Returns:
        Window: The created aiogram Window object.
    """
    return Window(
        Const("Select check out date"),
        CustomCalendar(id="check_in", on_click=date_confirm),
        Button(
            Const("⬅️ Back"),
            id="back",
            on_click=go_back,
            when=is_settings_not_complite,
        ),
        state=states.Dialog.CHECK_OUT,
    )
