# type: ignore
from aiogram import Dispatcher
from aiogram_dialog import Dialog, setup_dialogs

from bot.dialogs.check_in_date import check_in_date
from bot.dialogs.city_confirm import city_confirm
from bot.dialogs.city_request import city_request


def register_user_dialogs(dp: Dispatcher) -> None:
    dialogs = Dialog(*[city_request(), city_confirm(), check_in_date()])
    dp.include_router(dialogs)
    setup_dialogs(dp)
