"""
The factory pattern is a means to create new objects, without explicitly having to
specify the exactly class or object that will be created.  Typically this is handled
via calling a factory function/method (either through an interface implementation or overriding
a method in a derived class.

An example is outlined below, where depending on a language given to a factory function,
words are converted.  The caller is not required to know which class needs to be
instantiated, that is part of the responsibility of the factory function.

At a glance, the default implementation tends to be be a direct violation of the single
responsibility principle; later here we will demonstrate how we can potentially use
automatic registration of class instances to make the factory function aware of them.
"""

from abc import ABC
from abc import abstractmethod


class Localizable(ABC):

    @abstractmethod
    def localize(self, word: str) -> str:
        raise NotImplementedError


class EnglishLocalizer(Localizable):
    def __init__(self) -> None:
        ...

    def localize(self, word: str) -> str:
        return word


class GreekLocalizer(Localizable):
    def __init__(self) -> None:
        self.translations = dict(hello="γεια σας", goodbye="αντιο σας", sunshine="λιακάδα")

    def localize(self, word: str) -> str:
        return self.translations[word]


def get_localizer(language: str) -> Localizable:
    """
    Initial attempt at the factory function, notice here how
    the factories need to be 'known' upfront, resulting in a
    single responsibility principle violation, as new ways to
    handle the instantiation will require modification of this
    function (dict).
    """
    mapping = {"english": EnglishLocalizer,
               "greek": GreekLocalizer}
    return mapping[language.lower()]()


def main() -> None:
    """
    >>> english, greek = get_localizer("english"), get_localizer("greek")
    >>> english.localize("hello")
    'hello'
    >>> greek.localize("hello")
    'γεια σας'
    >>> english.localize("goodbye")
    'goodbye'
    >>> greek.localize("goodbye")
    'αντιο σας'
    """
    import doctest
    doctest.testmod()


if __name__ == "__main__":
    main()

# --------------------------------------------------------------------------------------------------------------




