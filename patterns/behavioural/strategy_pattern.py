"""
The strategy pattern enables selecting an algorithm at runtime, rather than implementing a single
algorithm directly.  Code receives runtime instructions as to which in a family of algorithms to
use.  Deferring the decision about which algorithm to use allows the calling to be more flexible
and maintainable.


The example below allows clients to sort a container of integers anyway they see fit.  It is extendible
by design.
"""
from typing import MutableSequence, Protocol


class Sortable(Protocol):
    """
    An interface that defines the behaviour for sorting data.
    """

    def sort(self, numbers: MutableSequence[int]) -> MutableSequence[int]:
        raise NotImplementedError


class MagicNumbers:
    """
    Representation of a simple container of integers that can be sorted
    in all sorts of weird and wonderful ways.  The importance here is that
    client code decides at runtime which way to sort things.  New sorting
    can be implemented easily without touching existing code.  This is a
    perfect example / implementation of the open closed principle which
    is what good use of the strategy pattern promotes; as well as a great
    example of relying on interfaces rather than concrete implementations.
    """

    def __init__(self, data: MutableSequence, sortable: Sortable):
        self.data = data
        self.sortable = sortable

    def sort_data(self) -> MutableSequence[int]:
        """

        :return:
        """
        return self.sortable.sort(self.data)


# -------------------------------- Strategy Implementations -------------------------------- #


class Reverse(Sortable):
    """
    A reversible strategy.
    """

    def sort(self, numbers: MutableSequence[int]) -> MutableSequence[int]:
        return list(reversed(sorted(numbers)))


class Sorted(Sortable):
    """
    A sorted strategy.
    """

    def sort(self, numbers: MutableSequence[int]) -> MutableSequence[int]:
        return list(sorted(numbers))


def main():
    """
    Here, the client can control how the data is sorted at runtime.  If a new sort needs to be
    put into place; the context (MagicNumbers) instance does not need to be touched, a new
    implementation of the Sortable interface can be passed at runtime.

    >>> import random
    >>> numbers = list(range(10))
    >>> random.shuffle(numbers)
    >>> context = MagicNumbers(numbers, Reverse())
    >>> context.sort_data()
    [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    >>> context = MagicNumbers(numbers, Sorted())
    >>> context.sort_data()
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    """


if __name__ == "__main__":
    from doctest import testmod

    testmod()
