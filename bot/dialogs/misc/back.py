from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button


async def go_back(clb: CallbackQuery, button: Button, manager: DialogManager) -> None:
    """
    A coroutine function that handles going back to the previous state in a conversation.

    Args:
        clb (CallbackQuery): The callback query from the user.
        button (Button): The button that triggered the callback query.
        manager (DialogManager): The dialog manager for managing conversation flow.

    Returns:
        None

    """
    await manager.back()
