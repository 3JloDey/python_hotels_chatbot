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
    """Checks if the location data is found in the dialog manager.
    
    Args:
    - data (dict): dictionary containing data to be checked
    - widget (Whenable): object used to check if a certain condition is met
    - manager (DialogManager): object that manages the dialog
    
    Returns:
    - bool: True if latitude and longitude are found in the dialog manager's data, False otherwise
    """
    if manager.dialog_data.get("latitude") and manager.dialog_data.get("longitude"):
        return True
    return False


def dislike(data: dict, widget: Whenable, manager: DialogManager) -> bool:
    """Checks if the current item is marked as not favorite in the dialog manager.
    
    Args:
    - data (dict): dictionary containing data to be checked
    - widget (Whenable): object used to check if a certain condition is met
    - manager (DialogManager): object that manages the dialog
    
    Returns:
    - bool: True if the current item is marked as not favorite in the dialog manager's data, False otherwise
    """
    return manager.dialog_data.get('is_favorite', False)


def like(data: dict, widget: Whenable, manager: DialogManager) -> bool:
    """Checks if the current item is marked as favorite in the dialog manager.
    
    Args:
    - data (dict): dictionary containing data to be checked
    - widget (Whenable): object used to check if a certain condition is met
    - manager (DialogManager): object that manages the dialog
    
    Returns:
    - bool: True if the current item is marked as favorite in the dialog manager's data, False otherwise
    """
    return not manager.dialog_data.get('is_favorite', False)
