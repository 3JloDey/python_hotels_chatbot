from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import Whenable


def is_settings_not_complite(data: dict, widget: Whenable, manager: DialogManager) -> bool:
    return manager.dialog_data.get("settings_complite") is None


def is_photo(data: dict, widget: Whenable, manager: DialogManager) -> bool:
    return len(manager.dialog_data["photos"]) > 0