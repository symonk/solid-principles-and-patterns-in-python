"""
The borg pattern is an alternative take on the `Singleton` pattern.  In the
borg pattern, instances of a class share the same state.  Whereas the Singleton
pattern tries to manage that only a single instance is ever created, instances
using the borg pattern can be created freely.  The `Borg` pattern can also be
known as the `monostate` pattern and it focuses on sharing state, rather than
sharing instance identity.

To best understand the `Borg` pattern, we need to understand how `__dict__` works
in python for instance attributes, when we create a class, instance attributes
are stored in a mapping known as `obj.__dict__`.  The same `__dict__` exists at
the class level (class state; not instance state).
"""
import typing


class BorgMixin:
    __monostate = {}

    def __init__(self) -> None:
        """
        Assign the shared state in any subclasses.
        """
        self.__dict__ = self.__monostate


class SharedState(BorgMixin):
    """
    A trivial example that manages some shared string state between multiple
    instantiations.  There is no longer a single instance of `SharedState`,
    instead we can create as many as we like, updating the state freely and
    guaranteeing that all existing instances will all be kept in sync.
    """
    def __init__(self, state: typing.Optional[typing.Any] = None) -> None:
        super().__init__()
        if state is not None:
            self.state = state
        else:
            if not hasattr(self, "state"):
                self.state = "initialized"

    def __str__(self) -> str:
        return self.state


def main() -> None:
    """
    >>> one = SharedState(state='foo')
    >>> one.state
    'foo'
    >>> two = SharedState(state='bar')
    >>> two.state
    'bar'
    >>> one.state
    'bar'
    >>> three = SharedState()
    >>> three.state
    'bar'
    >>> three.state = 'how now brown cow'
    >>> one.state
    'how now brown cow'
    >>> two.state, three.state
    ('how now brown cow', 'how now brown cow')
    """
    import doctest
    doctest.testmod()


if __name__ == "__main__":
    main()
