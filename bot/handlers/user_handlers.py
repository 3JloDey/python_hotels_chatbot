from aiogram import Dispatcher
from aiogram.filters.command import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from bot.states import states


async def command_start(msg: Message, dialog_manager: DialogManager) -> None:
    await msg.delete()
    await dialog_manager.start(states.Dialog.MAIN, mode=StartMode.RESET_STACK)


def register_user_handlers(dp: Dispatcher) -> None:
    dp.message.register(command_start, Command("start"))
