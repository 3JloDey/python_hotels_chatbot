from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import Whenable


def is_settings_not_complite(
    data: dict, widget: Whenable, manager: DialogManager
) -> bool:
    """
    A function that checks whether user settings are complete.

    Args:
        data (dict): The data for the widget.
        widget (Whenable): The widget to check.
        manager (DialogManager): The dialog manager for managing conversation flow.

    Returns:
        bool: True if settings are not complete, False otherwise.

    """
    return manager.dialog_data.get("settings_complite") is None


def is_found_location(data: dict, widget: Whenable, manager: DialogManager) -> bool:
    if manager.dialog_data.get("latitude") and manager.dialog_data.get("longitude"):
        return True
    return False
