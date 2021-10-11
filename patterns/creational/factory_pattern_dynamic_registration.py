"""
To combat some of the issues in the `factory_pattern.py` example, we can use dynamic
registration to automatically have the factory function be 'aware' of `Localizer`
instances.  Let's revisit and see if we can improve things.  This can be done via a
`Metaclass` or via the `__init_subclass` new dunder method (python 3.6+).  For the
sake of simplicity, we will try with the `__init_subclass__` dunder.
"""


from abc import ABC
from abc import abstractmethod
from typing import Optional


class Localizable(ABC):
    registry = {}

    def __init_subclass__(cls, language: Optional[str], **kwargs):  # noqa
        """
        Any subclasses of `Localizable` will be automatically recorded in the registry
        if they specify a language that they can support.
        :param language: (Optional) language to store in the registry dictionary as the key.
        :param kwargs:
        :return:
        """
        super().__init_subclass__(**kwargs)
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
