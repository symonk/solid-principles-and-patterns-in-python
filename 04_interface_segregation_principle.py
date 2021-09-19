"""
The (I)nterface Segregation Principle stipulates that classes should only implement
interfaces in which they can wholly fulfill.  Keeping interfaces smaller promotes
code reuse and helps prevent muddying the waters with regards to the single
responsibility principle.  A client should never be forced to implement an interface
that it does not use, only to implement noop methods in places.
"""

# ------------------------------------------ Violations ------------------------------------------

from abc import ABC
from abc import abstractmethod


class IDevice(ABC):
    """
    A clear violation of the interface segregation principle, by design this is forcing
    concrete implementations of the interface to violate the single responsibility principle.
    Concrete implementations will be required to provide implementation detail on how to
        * Have the ability to launch apps
        * Have the ability to send text messages
        * Have the ability to browser the web
    """

    @abstractmethod
    def launch_app(self, app_name: str) -> None:
        """
        Launch an app on the device.
        :param app_name: The app name to launch.
        :return: None
        """
        ...

    @abstractmethod
    def send_sms(self, content: str, recipient: str) -> None:
        """
        Send a simple text message to a recipient.
        :param content: The data to send in the sms body.
        :param recipient: The recipients phone number
        :return: None
        """
        ...

    @abstractmethod
    def view_webpage(self, target: str) -> None:
        """
        View a webpage.
        :param target: The url to view.
        :return: None
        """
        ...


class IPhone(IDevice):
    """
    A simple smart phone, capable of doing all of these things.
    """

    def launch_app(self, app_name: str) -> None:
        print(f"Launching: {app_name} now...")

    def send_sms(self, content: str, recipient: str) -> None:
        print(f"Sending message: {content} to: {recipient} now...")

    def view_webpage(self, target: str) -> None:
        print(f"loading website: {target}")


"""
So what's the problem you ask?  Firstly, wide interfaces promote violations of the single responsibility
principle, a class should not be responsible for all three of these things, each one has a segregated
reason to change.  The bigger problem however, appears when we look at adding a more basic device into
the mix:
"""


class LandLine(IDevice):
    """
    The problem, Code should not be forced into implementing methods and functionality
    that it cannot use.
    """

    def launch_app(self, app_name: str) -> None:
        """ No op; I cannot launch apps."""

    def send_sms(self, content: str, recipient: str) -> None:
        print(f"Sending message: {content} to: {recipient}")

    def view_webpage(self, target: str) -> None:
        """ No op; I cannot launch a browser."""


"""
Often as outlined here, violations of the interface segregation principle result in
violations of the single responsibility principle.  We can go about solving some 
of these problems by keeping our interfaces small.  Smaller interfaces promote much
better reusability and maintainability of our code.  Let's try solve this below:
"""

# ------------------------------------------ Violations ------------------------------------------


class ISendSms(ABC):
    """
    A simple interface for sending text based messages.
    """

    @abstractmethod
    def send_sms(self, content: str, recipient: str) -> None:
        raise NotImplementedError


class ILaunchApp(ABC):
    """
    A simple interface for launching apps.
    """

    @abstractmethod
    def launch_app(self, app_name: str) -> None:
        raise NotImplementedError


class IViewWebPage(ABC):
    """
    A simple interface for viewing web pages.
    """

    @abstractmethod
    def view_webpage(self, target: str) -> None:
        raise NotImplementedError

