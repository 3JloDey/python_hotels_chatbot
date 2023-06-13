# type: ignore
from aiogram.types import CallbackQuery


def paginate(clb: CallbackQuery, index: int, lst: list) -> int:
    lenght = len(lst)
    if clb.data == "next" and 0 <= index < lenght - 1:
        index += 1
    elif clb.data == "prev" and 0 < index <= lenght - 1:
        index -= 1
    return index
