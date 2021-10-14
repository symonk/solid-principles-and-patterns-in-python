"""
To combat some of the issues in the `factory_pattern.py` example, we can use dynamic
registration to automatically have the factory function be 'aware' of `Localizer`
instances.  Let's revisit and see if we can improve things.  This can be done via a
`Metaclass` or via the `__init_subclass` new dunder method (python 3.6+).  For the
sake of simplicity, we will try with the `__init_subclass__` dunder.

Now any user defined code can avail of our factory function, as long as they implement
our interface and provide a language variable, the factory function no longer has to
change, it will automatically consider it an option for retrieving the values from.
"""
from __future__ import annotations

import typing
from abc import ABC, abstractmethod
from typing import Optional


class Localizable(ABC):
    registry: typing.Dict[str, typing.Type[Localizable]] = {}

    def __init_subclass__(cls, language: Optional[str], **kwargs):  # noqa
        """
        Any subclasses of `Localizable` will be automatically recorded in the registry
        if they specify a language that they can support.
        :param language: (Optional) language to store in the registry dictionary as the key.
        :param kwargs:
        :return:
        """
        super().__init_subclass__(**kwargs)  # type: ignore
        if language is not None:
            cls.registry[language.lower()] = cls

    @abstractmethod
    def localize(self, word: str) -> str:
        raise NotImplementedError


class EnglishLocalizer(Localizable, language="english"):
    def __init__(self) -> None:
        ...

    def localize(self, word: str) -> str:
        return word


class GreekLocalizer(Localizable, language="greek"):
    def __init__(self) -> None:
        self.translations = dict(hello="γεια σας", goodbye="αντιο σας", sunshine="λιακάδα")

    def localize(self, word: str) -> str:
        return self.translations[word]


class SpanishLocalizer(Localizable, language="spanish"):
    def __init__(self) -> None:
        self.translations = dict(hello="Hola", goodbye="adiós", sunshine="Brillo Solar")

    def localize(self, word: str) -> str:
        return self.translations[word]


def get_localizer(language: str) -> Localizable:
    return Localizable.registry[language]()


def main() -> None:
    """
    >>> english, greek, spanish = map(get_localizer, ("english", "greek", "spanish"))
    >>> english.localize("hello")
    'hello'
    >>> greek.localize("goodbye")
    'αντιο σας'
    >>> spanish.localize("sunshine")
    'Brillo Solar'
    """
    import doctest

    doctest.testmod()


if __name__ == "__main__":
    main()
