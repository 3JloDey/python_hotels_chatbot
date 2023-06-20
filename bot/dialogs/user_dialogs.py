# type: ignore
from aiogram import Dispatcher
from aiogram_dialog import Dialog, setup_dialogs

from bot.dialogs.check_in_date import check_in_date
from bot.dialogs.check_out_date import check_out_date
from bot.dialogs.city_confirm import city_confirm
from bot.dialogs.city_request import city_request
from bot.dialogs.get_hotels import get_hotels
from bot.dialogs.get_photo import get_photo
from bot.dialogs.main_menu import main_menu
from bot.dialogs.settings import settings


def register_user_dialogs(dp: Dispatcher) -> None:
    """
    Registers user dialogs in the dispatcher.

    Args:
        dp (Dispatcher): The aiogram Dispatcher object.
    """
    dialogs = Dialog(
        city_request(),
        city_confirm(),
        check_in_date(),
        check_out_date(),
        main_menu(),
        settings(),
        get_hotels(),
        get_photo(),
    )
    dp.include_routers(dialogs)
    setup_dialogs(dp)
