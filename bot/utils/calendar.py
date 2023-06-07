from calendar import monthcalendar
from datetime import date
from time import mktime
from typing import Any, List

from aiogram.types import InlineKeyboardButton
from aiogram_dialog.widgets.kbd import Calendar

# Constants for managing widget rendering scope
SCOPE_DAYS = "SCOPE_DAYS"
SCOPE_MONTHS = "SCOPE_MONTHS"
SCOPE_YEARS = "SCOPE_YEARS"

# Constants for scrolling months
MONTH_NEXT = "+"
MONTH_PREV = "-"

# Constants for prefixing month and year values
PREFIX_MONTH = "MONTH"
PREFIX_YEAR = "YEAR"

MONTHS_NUMBERS = [(1, 2, 3), (4, 5, 6), (7, 8, 9), (10, 11, 12)]


class MyCalendar(Calendar):
    def __init__(self, *args: Any, **kwds: Any) -> None:
        super().__init__(*args, **kwds)

    def days_kbd(self, offset) -> List[List[InlineKeyboardButton]]:
        header_week = offset.strftime("%B %Y")
        weekheader = [
            InlineKeyboardButton(text=dayname, callback_data=" ")
            for dayname in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        ]
        days = []
        for week in monthcalendar(offset.year, offset.month):
            week_row = []
            for day in week:
                if day == 0:
                    week_row.append(
                        InlineKeyboardButton(
                            text=" ",
                            callback_data=" ",
                        ),
                    )
                else:
                    raw_date = int(
                        mktime(
                            date(offset.year, offset.month, day).timetuple(),
                        ),
                    )

                    week_row.append(
                        InlineKeyboardButton(
                            text=f"{day} 🗓"
                            if date(offset.year, offset.month, day) == date.today()
                            else str(day),
                            callback_data=self._item_callback_data(raw_date),
                        ),
                    )
            days.append(week_row)
        return [
            [
                InlineKeyboardButton(
                    text=header_week,
                    callback_data=self._item_callback_data(SCOPE_MONTHS),
                ),
            ],
            weekheader,
            *days,
            [
                InlineKeyboardButton(
                    text="◀️ Prev month",
                    callback_data=self._item_callback_data(MONTH_PREV),
                ),
                InlineKeyboardButton(
                    text="🔍 Zoom out",
                    callback_data=self._item_callback_data(SCOPE_MONTHS),
                ),
                InlineKeyboardButton(
                    text="Next month ▶️",
                    callback_data=self._item_callback_data(MONTH_NEXT),
                ),
            ],
        ]

    def months_kbd(self, offset) -> List[List[InlineKeyboardButton]]:
        header_year = offset.strftime("Year %Y")
        months = []
        for n in MONTHS_NUMBERS:
            season = []
            for month in n:
                month_text = date(offset.year, month, 1).strftime("%B")
                season.append(
                    InlineKeyboardButton(
                        text=month_text,
                        callback_data=self._item_callback_data(
                            f"{PREFIX_MONTH}{month}",
                        ),
                    ),
                )
            months.append(season)
        return [
            [
                InlineKeyboardButton(
                    text=header_year,
                    callback_data=self._item_callback_data(SCOPE_YEARS),
                ),
            ],
            *months,
        ]
