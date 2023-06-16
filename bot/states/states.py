from aiogram.fsm.state import State, StatesGroup


class Dialog(StatesGroup):
    """
    A finite state machine for managing conversation flow in a chatbot.

    States:
        MAIN: The main state of the conversation.
        CONFIRM_LOCATION: The state for confirming the user's location.
        CHECK_IN: The state for asking the user for their check-in date.
        CHECK_OUT: The state for asking the user for their check-out date.
        MENU: The state for displaying a menu of options to the user.
        SETTINGS: The state for changing the bot's settings.
        HOTELS: The state for displaying information about hotels.
        PHOTOS: The state for displaying photos.

    """

    MAIN = State()
    CONFIRM_LOCATION = State()
    CHECK_IN = State()
    CHECK_OUT = State()
    MENU = State()
    SETTINGS = State()
    HOTELS = State()
    PHOTOS = State()
