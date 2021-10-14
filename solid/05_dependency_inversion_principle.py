"""
The Dependency Inversion Principle outlines a means of avoiding unnecessary
hard coupling between objects, High level modules should not depend on low
level modules, but instead should depend on abstractions (e.g an interface).
Why? - This allows code to be closed for modification but remain open for
extension.

Abstractions themselves should NOT depend on details.  Concrete implementations
should instead depend on abstractions.  Let's dive into this with a simple
example.

In this example we own a comic book company that ships batches of comic books
to our customers; however our comics need to be stamped with a special 10th
anniversary sticker prior to shipping.
"""

import typing
from dataclasses import dataclass


# -------------------------------------------- Violations --------------------------------------------
class ComicBook:
    def __init__(self, title: str, pages: int, content: str) -> None:
        self.title = title
        self.pages = pages
        self.content = content


class Stamper:
    def __init__(self) -> None:
        self.label = "10th anniversary label"

    def stamp(self, book: ComicBook) -> None:
        print(f"Stamping: {book.title} with: {self.label}")


class Shipper:
    def __init__(self) -> None:
        self.stamper = Stamper()

    def ship_it(self, book: ComicBook) -> None:
        self.stamper.stamp(book)
        print(f"Shipping: {book.title} to the customer..")


"""
In the example above, there are high level modules depending on low level modules
rather than abstractions.  An overview of the problems here are:

    * `Shipper` is reliant upon the `Stamper` class explicitly making it much harder to extend.
    * `Shipper` is instantiating a `Stamper` instance in its `__init__` making it much harder to test.
    * Everything is reliant upon a concrete `ComicBook` directly making it much harder to extend.
"""

# ------------------------------------------ Rectifications ------------------------------------------


@dataclass()  # type: ignore
class ContainsContent(typing.Protocol):
    title: str
    content: str
    pages: int


class ImprovedComicBook(ContainsContent):
    def __init__(self, title: str, content: str, pages: int) -> None:
        self.title = title
        self.content = content
        self.pages = pages


class Shippable(typing.Protocol):
    def ship(self, book: ContainsContent) -> None:
        raise NotImplementedError


class Stampable(typing.Protocol):
    def stamp(self, book: ContainsContent) -> None:
        raise NotImplementedError


class ImprovedStamper(Stampable):
    def __init__(self, label: str) -> None:
        self.label = label

    def stamp(self, book: ContainsContent) -> None:
        print(f"Stamping: {book.title} with: {self.label}")


class AirMailShipper(Shippable):
    def __init__(self, stamper: Stampable) -> None:
        self.stamper = stamper

    def ship(self, book: ContainsContent) -> None:
        print(f"Shipping: {book.title} via air mail")


"""
The main differences here are the additional protocol/interafaces we have defined.
This buys us the following benefits:

    * `AirMailShipper` and `ImprovedStamper` rely on some sort of `content` that can be provided at runtime.
    * `AirMailShipper` is reliant on something `stampable` which can be extended and supplied at runtime.
    * Another shipping class could be used easily, `TrainShipper` for example without the need to refactor.
    * Another stamped could be used easily without the need to refactor.
    * `ContainsContent` allows other things to be stamped and printed without refactoring, e.g a `Magazine` class.
    * Testability has improved ten fold.
"""


def main() -> None:
    """
    >>> Shipper().ship_it(ComicBook(title="Spiderman", pages=435, content="the itsy witsy spider..."))
    Stamping: Spiderman with: 10th anniversary label
    Shipping: Spiderman to the customer..

    >>> book = ComicBook(title="Hulk", pages=500, content="Hulk smash!")
    >>> AirMailShipper(ImprovedStamper(label="10th Anniversary!")).ship(book)
    Shipping: Hulk via air mail
    """


if __name__ == "__main__":
    import doctest

    doctest.testmod()
