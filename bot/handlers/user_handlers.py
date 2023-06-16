from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from bot.states import states


async def command_start(msg: Message, dialog_manager: DialogManager) -> None:
    """
    A function that handles the /start command.

    Args:
        msg (Message): The message object representing the /start command.
        dialog_manager (DialogManager): The dialog manager for handling user input.

    Returns:
        None

    """
    await msg.delete()
    await dialog_manager.start(states.Dialog.MAIN, mode=StartMode.RESET_STACK)
