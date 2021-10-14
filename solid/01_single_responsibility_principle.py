"""
The Single Responsibility Principle defines that a function, method, class or module
has only a single reason to change.  When adhering to this principle it makes maintaining
the software much easier, some of the reasons why are:

    * Easier to test your code with reduced coupling.
    * Easier to maintain the software and react to changes in requirements.
    * Easier to follow the code and it is more self documenting.
    * Many others...

Something to note, SRP can be taken to extreme cases if you take it too literally, finding the
sweet spot can sometimes be hard, but creating a bunch of classes with a single function and
composing them together etc can often lead to the opposite of what the principle aims to achieve.
Do not take it too literally, keep the goal of maintainability in mind at all times and a single
responsibility does not need to be taken literally, often the `Responsibility` here does not have
to be so granular.
"""

# ------------------------------------------ Violations ------------------------------------------


class Invoice:
    """
    A representation of an invoice.
    """

    def __init__(self, recipient: str, total: float) -> None:
        self.recipient = recipient
        self.total = total

    def send(self) -> None:
        print(f"Sending invoice in an email to: {self.recipient}")


class OrderManager:
    """
    Let's make a trivial example; You may want to build out a simple class
    that is responsible for calculating discount for orders and handle
    dispatching invoices, however I would consider these two different
    responsibilities and it's highly likely that each have an option to
    change independently, resulting in increased risk to breakages in the
    other code.  In the calculate discount function here, we also have
    some terrible violations of the single responsibility principle, depending
    on the recipient we apply a different discount... (Never do this).
    """

    def __init__(self, price: float, recipient: str) -> None:
        self.price = price
        self.recipient = recipient

    def calculate_discount(self) -> float:
        """
        Calculates discount, if appropriate for the recipient.  Again, this is horrible
        and this function is likely to require changing in future, for another special
        case.  Remember, special cases are not special enough,  polymorphism is the
        correct answer here.
        :return: The newly calculated price, post discount if applicable.
        """
        if self.recipient == "tenpercent@foobar.com":
            return self.price / 100 * 10
        elif self.recipient == "fiftypercent@foobar.com":
            return self.price / 100 * 50
        return self.price

    def dispatch_invoice(self) -> Invoice:
        """
        Dispatches an invoice to the customer, again another horrible violation of the
        single responsibility principle as this method in itself is responsible for two
        things, creating an invoice and dispatching it.
        :return:
        """
        invoice = Invoice(self.recipient, self.calculate_discount())
        invoice.send()
        return invoice


"""
To summarise the code above, and why it is suboptimal we have to think of a few different things,
for each of these we will look to solve them using various SOLID approaches and OOP principles:

    * calculate_discount is not closed for modification (OCP - see 02) and will constantly need modified.
    * dispatch_invoice is coupled to a concrete implementation by instantiating an `Invoice` directly (Testability/DIP?)
    * OrderManager has two reasons to change, calculating pricing or sending invoices (SRP).

So how can we go about fixing this to be more testable and more maintainable?

    * OrderManager can delegate its workload classes housing those single responsibilities.
    * Polymorphism can be an aid in better defining a discounting strategy, strategy pattern.
    * Using higher level abstract types and passing them in can increase testability w/r/t dispatching invoices.
"""

# ------------------------------------------ Rectifications ------------------------------------------

from typing import Protocol  # noqa
from typing import runtime_checkable  # noqa


@runtime_checkable
class Dispatchable(Protocol):
    def dispatch(self) -> None:
        ...


class InvoiceDispatcher:
    """
    An invoice dispatcher, solely responsible for shipping out invoices to customers.
    There may be multiple ways to dispatch.
    """

    def __init__(self, dispatchable: Dispatchable) -> None:
        self.dispatchable = dispatchable

    def send_invoice(self) -> Dispatchable:
        """
        Not relying on a concrete implementation, but an interface which describes the
        ability to send something, that could be via email or otherwise.
        :return: The dispatchable instance
        """
        self.dispatchable.dispatch()
        return self.dispatchable


class Invoice(Dispatchable):  # noqa
    """
    A simple representation of an invoice.  It is no longer responsible for calculating
    the total price, but merely storing some state in relation to an order and when
    required, sending the invoice / pricing to the customer.
    """

    def __init__(self, recipient: str, total: float):
        self.recipient = recipient
        self.total = total

    def __repr__(self) -> str:
        return f"Invoice(recipient={self.recipient}, total={self.total})"

    def dispatch(self) -> None:
        print(f"Emailing: {self.recipient} an invoice with the total of: {self.total}")


@runtime_checkable
class Discountable(Protocol):
    """
    A simple interface to benefit from polymorphism later, this provides the benefits of
    allowing new discounting strategies to be created, client code can subclass and
    implement their own if necessary and that's where the benefits and maintainability
    come into full effect.
    """

    def calculate(self, price: float) -> float:
        ...


class TenPercentDiscountStrategy(Discountable):
    """
    Simple implementation that reduces the price by 10%
    """

    def calculate(self, price: float) -> float:
        return price / 100 * 90


class FiftyPercentDiscountStrategy(Discountable):
    """
    Simple implementation that reduces the price by half.
    """

    def calculate(self, price: float) -> float:
        return price / 100 * 50


class Discounter:
    def __init__(self, discountable: Discountable) -> None:
        self.discountable = discountable

    def get_discount(self, price: float) -> float:
        return self.discountable.calculate(price)


def main():
    """
    >>> recipient = "foo@bar.com"
    >>> price = 875.00
    >>> discounter = Discounter(FiftyPercentDiscountStrategy())
    >>> invoice = Invoice(recipient, discounter.get_discount(price))
    >>> dispatcher = InvoiceDispatcher(invoice)
    >>> dispatcher.send_invoice()
    Emailing: foo@bar.com an invoice with the total of: 437.5
    Invoice(recipient=foo@bar.com, total=437.5)
    """
    ...


if __name__ == "__main__":
    import doctest

    doctest.testmod()
