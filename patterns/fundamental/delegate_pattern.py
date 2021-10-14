"""
The delegation pattern is a simple pattern that allows composition to achieve the same
code use as inheritance.  In delegation two objects are involved in handling and
dispatching a request.  A receiving object delegates it's operations to it's delegate.
"""


from typing import Any, Callable, Union


class Mobile:
    def __init__(self, memory: int) -> None:
        self.memory = memory

    def make_call(self, number: int) -> None:
        print(f"Calling: {number}")

    def launch_app(self, app: str) -> None:
        print(f"Launching: {app}")


class SmartMobile:
    def __init__(self, delegate: Mobile) -> None:
        self.delegate = delegate

    def __getattr__(self, item: str) -> Union[Any, Callable]:
        attr = getattr(self.delegate, item)
        if not callable(attr):
            return attr

        def wrapper(*args, **kwargs):
            return attr(*args, **kwargs)

        return wrapper

    def download_updates(self) -> None:
        print("downloading updates...")


def main():
    """
    >>> mobile = Mobile(256)
    >>> s = SmartMobile(mobile)
    >>> s.make_call(123456789)
    Calling: 123456789
    >>> s.launch_app("tetris")
    Launching: tetris
    >>> s.download_updates()
    downloading updates...
    """


if __name__ == "__main__":
    from doctest import testmod

    testmod()
