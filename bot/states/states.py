from aiogram.fsm.state import State, StatesGroup

# class SearchHotels(StatesGroup):
#     start = State()
#     city_request = State()
#     select_location = State()
#     check_in_date = State()
#     check_out_date = State()
#     photo_request = State()
#     count_photo = State()
#     main_menu = State()
#     settings = State()
#     hotels = State()


class Settings(StatesGroup):
    MAIN = State()
    CONFIRM_LOCATION = State()
    CHECK_IN = State()
    CHECK_OUT = State()


class Main(StatesGroup):
    MENU = State()
    SETTINGS = State()
    HOTELS = State()
