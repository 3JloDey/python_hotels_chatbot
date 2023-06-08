from typing import Callable


class Formatting:
    def __init__(self, func: Callable) -> None:
        self.func = func

    def __call__(self, text: str) -> str:
        return f"<{self.func.__name__}>{self.func(text)}</{self.func.__name__}>"


class Html(Formatting):
    @staticmethod
    def b(text: str) -> str:
        return text

    @staticmethod
    def i(text: str) -> str:
        return text

    @staticmethod
    def u(text: str) -> str:
        return text
