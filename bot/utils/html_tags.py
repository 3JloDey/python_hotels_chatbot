from typing import Callable


def formatting(func) -> Callable:
    def wrapper(text) -> str:
        return f"<{func.__name__}>{func(text)}</{func.__name__}>"

    return wrapper


class Html:
    @staticmethod
    @formatting
    def b(text) -> str:
        """Жирный текст"""
        return text

    @staticmethod
    @formatting
    def i(text) -> str:
        """Курсивный текст"""
        return text

    @staticmethod
    @formatting
    def u(text) -> str:
        """Подчеркнутый текст"""
        return text
