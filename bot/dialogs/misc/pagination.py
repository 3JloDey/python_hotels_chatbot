# type: ignore
from aiogram.types import CallbackQuery


async def pagination(clb: CallbackQuery, index: int, lst: list) -> int:
    """
    A function that paginates through a list of items based on user input.

    Args:
        clb (CallbackQuery): The callback query object containing the user input.
        index (int): The current index of the item in the list.
        lst (list): The list of items to paginate through.

    Returns:
        int: The new index of the item in the list after pagination.

    """
    length = len(lst)
    if clb.data == "next" and 0 <= index < length - 1:
        index += 1
    elif clb.data == "prev" and 0 < index <= length - 1:
        index -= 1
    return index
