from datetime import date

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, ManagedCalendarAdapter
from aiogram_dialog.widgets.text import Const

from bot.dialogs.misc import go_back, is_settings_not_complite
from bot.states import states
from bot.utils import CustomCalendar
from bot.utils.date_validation import check_out_date_validator, validation_error


async def date_confirm(
    clb: CallbackQuery,
    _: ManagedCalendarAdapter,
    manager: DialogManager,
    selected_date: date,
) -> None:
    date = str(selected_date)
    if check_out_date_validator(manager, date) is False:
        await validation_error(clb, date)
    else:
        manager.dialog_data['settings_complite'] = True
        manager.dialog_data["check_out_date"] = date
        await manager.switch_to(states.Dialog.MENU)


def check_out_date() -> Window:
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