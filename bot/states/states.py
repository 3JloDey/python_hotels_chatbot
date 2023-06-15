from aiogram.fsm.state import State, StatesGroup


class Dialog(StatesGroup):
    MAIN = State()
    CONFIRM_LOCATION = State()
    CHECK_IN = State()
    CHECK_OUT = State()
    MENU = State()
    SETTINGS = State()
    HOTELS = State()
    PHOTOS = State()
