"""
The publish subscribe pattern is very similar to the observer pattern, however it keeps a
loose coupling between both the publishers and the subsribers, they are even unaware of
each other and a message queue sits in between them.

To see the differences in the observer pattern vs the pub-sub pattern, reference the `observer.py`
file in this directory. (Typically an observer has a list of observers and iterates across them
to notify them in a synchronous way, pub sub typically uses a message queue / broker and works in
an asynchronous fashion.


Todo: In the example outlined below, use of interfaces could make things more extensible as well
as provide better typing support, arguably there is a violation of the dependency inversion
principle here as things are relying on concrete implementations, e.g `Provider` and `Subscriber`.

"""
import typing


class Provider:
    """
    The Provider acts like a middle man between both the subscribers and publishers.  It retains
    a mapping of message:Sequence of subscribers.
    """

    def __init__(self) -> None:
        self.message_queue: typing.List[str] = []
        self.subscribers: typing.Dict[str, typing.List[Subscriber]] = {}

    def notify(self, message: str) -> None:
        self.message_queue.append(message)

    def subscribe(self, message: str, subscriber) -> None:
        self.subscribers.setdefault(message, []).append(subscriber)

    def unsubscribe(self, message: str, subscriber) -> None:
        self.subscribers[message].remove(subscriber)

    def update(self) -> None:
        for message in self.message_queue:
            for subscriber in self.subscribers.get(message, ()):
                subscriber.run(message)
        self.message_queue.clear()


class Publisher:
    """
    A simple publisher, responsible for sending messages to the provider.  In a publish
    subscribe setting, the publish is not aware of the subscribers and the subscribers
    have no awareness of the publisher, they both use the message broker / message queue
    middleman.
    """
    def __init__(self, provider: Provider) -> None:
        self.provider = provider

    def publish(self, message: str) -> None:
        self.provider.notify(message)


class Subscriber:
    """
    A simple subscriber, responsible for subscribing to the provider
    for a given message.
    """

    def __init__(self, name: str, provider: Provider) -> None:
        self.name = name
        self.provider = provider

    def subscribe(self, message: str) -> None:
        self.provider.subscribe(message, self)

    def unsubscribe(self) -> None:
        self.provider.unsubscribe(self)

    def run(self, message: str) -> None:
        print(f"Subscriber: {self.name} received message: {message}")


def main() -> None:
    """

    """
    import doctest
    doctest.testmod()


if __name__ == "__main__":
    main()