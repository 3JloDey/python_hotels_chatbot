from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button


async def go_back(clb: CallbackQuery, button: Button, manager: DialogManager) -> None:
    await manager.back()
