from datetime import date

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager


async def validation_error(clb: CallbackQuery, selected_date: str) -> None:
    """
    Shows an error message to the user when an invalid date is selected.

    Args:
    - clb (CallbackQuery): The callback query object.
    - selected_date (str): The selected date in string format.

    Returns:
    - None
    """
    text = f"Date {selected_date} is invalid.\nPlease select a valid date."
    await clb.answer(text=text, show_alert=True)


def check_in_date_validator(manager: DialogManager, selected_date: str) -> bool:
    """
    Validates the selected check-in date.

    Args:
    - manager (DialogManager): The dialog manager object.
    - selected_date (str): The selected check-in date in string format.

    Returns:
    - bool: True if the selected date is valid, False otherwise.
    """
    check_out_date = manager.dialog_data.get("check_out_date")
    today = str(date.today())
    if check_out_date and (selected_date < today or selected_date > check_out_date):
        return False
    elif selected_date < today:
        return False
    return True


def check_out_date_validator(manager: DialogManager, selected_date: str) -> bool:
    """
    Validates the selected check-out date.

    Args:
    - manager (DialogManager): The dialog manager object.
    - selected_date (str): The selected check-out date in string format.

    Returns:
    - bool: True if the selected date is valid, False otherwise.
    """
    check_in_date: str = manager.dialog_data["check_in_date"]
    today: str = str(date.today())

    if selected_date < today or selected_date < check_in_date:
        return False
    return True
