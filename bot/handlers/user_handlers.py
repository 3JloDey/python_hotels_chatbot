from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from bot.states import states


async def command_start(msg: Message, dialog_manager: DialogManager) -> None:
    await msg.delete()
    await dialog_manager.start(states.Dialog.MAIN, mode=StartMode.RESET_STACK)
