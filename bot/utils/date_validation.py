from datetime import date

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager


async def validation_error(clb: CallbackQuery, selected_date: str) -> None:
    text = f"Date {selected_date} is invalid.\nPlease select a valid date."
    await clb.answer(text=text, show_alert=True)


def check_in_date_validator(manager: DialogManager, selected_date: str) -> bool:
    check_out_date = manager.dialog_data.get("check_out_date")
    today = str(date.today())
    if check_out_date and (selected_date < today or selected_date > check_out_date):
        return False
    elif selected_date < today:
        return False
    return True


def check_out_date_validator(manager: DialogManager, selected_date: str) -> bool:
    check_in_date: str = manager.dialog_data["check_in_date"]
    today: str = str(date.today())

    if selected_date < today or selected_date < check_in_date:
        return False
    return True
