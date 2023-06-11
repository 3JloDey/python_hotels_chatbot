from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button, Row, SwitchTo
from aiogram_dialog.widgets.text import Const

from bot.dialogs.misc import go_back
from bot.states import states


def settings() -> Window:
    return Window(
        Const("Settings menu"),
        Row(
            SwitchTo(
                Const("Change city"),
                id="change_city",
                state=states.Dialog.MAIN,
            ),
            # SwitchTo(
            #     Const("Change count of photos"),
            #     id="change_photo",
            #     state=SearchHotels.photo_request,
            # ),
        ),
        Row(
            SwitchTo(
                Const("Change check in date"),
                id="change_check_in",
                state=states.Dialog.CHECK_IN,
            ),
            SwitchTo(
                Const("Change check out date"),
                id="change_check_out",
                state=states.Dialog.CHECK_OUT,
            ),
        ),
        Button(Const("Back"), id="back", on_click=go_back),
        state=states.Dialog.SETTINGS,
    )
