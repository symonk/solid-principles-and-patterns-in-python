"""
The liskov substitution principles is one of the simplest principles; in a nutshell it states
that if `S` is a subtype of `T`, then objects of type `T` may be replaced with objects of
type `S`.  This is the corner stone of inheritance and polymorphism.  Good implementations of
the single responsibility principle often result in liskov substitution principle being handled
cleanly too.
"""

# ------------------------------------------ Violations ------------------------------------------


class T:
    def __init__(self, number: int) -> None:
        self.number = number

    def calculate(self) -> int:
        return self.number * 2


class Y(T):
    ...


class S(T):
    """
    This subclass is a problem, it changes the 'API' of the `calculate()` method to accept
    an additional argument to configure the multiplication, this breaks clients expectations
    and calling code is likely to break when assuming it can accept instances of type `T`.
    """

    def calculate(self, multiplier) -> int:  # type: ignore # noqa
        return self.number * multiplier


def perform_calculations(obj: T) -> int:
    return obj.calculate()


# ------------------------------------------ Rectifications ------------------------------------------


class S2(T):
    ...


def main() -> None:
    """
    >>> one, two = Y(10), S(20)
    >>> perform_calculations(one)
    20
    >>> perform_calculations(two) # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    TypeError: calculate() missing 1 required positional argument: 'multiplier'
    >>> two_fixed = S2(150)
    >>> perform_calculations(two_fixed)
    300
    """


if __name__ == "__main__":
    import doctest

    doctest.testmod()
