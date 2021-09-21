"""
The open closed principle is a relatively simple one, it indicates that code should
be open for extension but closed for modification, this ties in nicely with
both the Interface Segregation Principle and the Single Responsibility Principle.

Client code should be able to extend the application easily and by design will
make maintaining code much easier.

    * (O)pen for extension.
    * (C)losed for modification.
"""

# ------------------------------------------ Violations ------------------------------------------


class Car:
    """
    A trivial representation of a car.
    """
    def __init__(self, fuel_type: str) -> None:
        self.fuel_type = fuel_type

    def __repr__(self) -> str:
        return f"Car(fuel_type={self.fuel_type})"


class FuelStation:
    """
    Here lies the crux of not following the open closed principle, The FuelStation class
    is responsible for refuelling cars, depending on their fuel type.  By design this
    implementation is horrible, for a number of reasons:

        * Any additional `Car` fuel types will require modification of this tightly coupled implementation.
        * Client code is unable to extend this code in a meaningful way.
        * Making such modifications runs the risk of breaking other related areas of the system.

    Based on the fuel type of the car, the station decides which underlying function to call in order to refuel
    it.
    """
    def refuel(self, car: Car) -> None:
        if car.fuel_type == "petrol":
            self._fill_with_petrol(car)
        elif car.fuel_type == "diesel":
            self._fill_with_diesel(car)

    @staticmethod
    def _fill_with_petrol(car: Car) -> None:
        """
        Refuel a petrol car.
        :param car: A car instance to fill with fuel.
        :return: None
        """
        print(f"Filling {car} with petrol..")

    @staticmethod
    def _fill_with_diesel(car: Car) -> None:
        """
        Refuel a diesel car.
        :param car: A car instance to fill with fuel.
        :return: None
        """
        print(f"Filling {car} with diesel..")


"""
Let's build on the above example, in current times we have seen a large uptake in electric
vehicles, we want to support a brand new tesla but what gives? we need to go back and modify
our existing code in order to support that, why does this suck?

    * It's only a matter of time until we need another fuel type in the future?
    * Clients code is in limbo really, core library function logic needs updated here?
    * We are touching unrelated code, always increasing the risk of breaking something unintentionally?
    
See below for the changes we would need to support our new electric car:
"""


class FuelStation:  # noqa
    """
    The same old `FuelStation` class, with added support for the electric car.
    How long until we need to do this yet again?
    """

    def refuel(self, car: Car) -> None:
        if car.fuel_type == "petrol":
            self._fill_with_petrol(car)
        elif car.fuel_type == "diesel":
            self._fill_with_diesel(car)
        elif car.fuel_type == "electric":
            self._fill_with_electric(car)

    @staticmethod
    def _fill_with_electric(car: Car) -> None:
        """
        Our new function to support electric cars within
        the application.
        :param car: A car instance to fill with fuel.
        :return: None
        """
        print(f"Charging {car} with electricity...")

    @staticmethod
    def _fill_with_petrol(car: Car) -> None:
        """
        Refuel a petrol car.
        :param car: A car instance to fill with fuel.
        :return: None
        """
        print(f"Filling {car} with petrol..")

    @staticmethod
    def _fill_with_diesel(car: Car) -> None:
        """
        Refuel a diesel car.
        :param car: A car instance to fill with fuel.
        :return: None
        """
        print(f"Filling {car} with diesel..")

"""
As you can see, this is horrible and an overly complex, unmaintainable coupled mess.
It is very likely to need to keep constantly changing, limits consumer code and
runs the risk of breaking other areas of the system unnecessarily.

Let's fix it, below is a better design to achieve the same outcome:

"""

# ------------------------------------------ Rectifications ------------------------------------------

from abc import ABC
from abc import abstractmethod


class Refuellable(ABC):
    """
    A simple interface, for anything that is 'refuellable'.
    """
    @abstractmethod
    def refuel(self):
        raise NotImplementedError


class Car(Refuellable):  # noqa
    """
    An abstract Car base class
    """
    def __init__(self, fuel_type: str) -> None:
        self.fuel_type = fuel_type

    @abstractmethod
    def refuel(self):
        raise NotImplementedError


class PetrolCar(Car):
    """
    Over simplified representation of a petrol fuelled car.
    """
    def __init__(self) -> None:
        super().__init__("petrol")

    def refuel(self) -> None:
        print(f"Refuelling the {self.fuel_type} car...")


class DieselCar(Car):
    """
    Over simplified representation of a diesel fuelled car.
    """
    def __init__(self) -> None:
        super().__init__("diesel")

    def refuel(self) -> None:
        print(f"Refuelling the {self.fuel_type} car...")


class ElectricCar(Car):
    """
    Over simplified representation of an electric powered car.
    """
    def __init__(self) -> None:
        super().__init__("electric")

    def refuel(self) -> None:
        print(f"Recharging the {self.fuel_type} car...")


class FuelStation:  # noqa
    """
    A simple implementation of the FuelStation.
    """

    def do_refuelling(self, refuellable: Refuellable) -> None:
        """
        The fuel station has now delegated the responsibility for refuelling to
        extendible, client controlled code.
        :param refuellable: An instance of something which adheres to the refuellable interface.
        :return: None
        """
        refuellable.refuel()


"""
There we have it, refuelling has now been opened up for extension, but closed for modification.
A new vehicle comes along later? or we open up support for different things other than cars?
no problem! they can implement the interface and we will be able to refuel them at the fuelstation.
Python supports duck typing so some would argue creating an ABC here is overkill, I like to keep
the intent clear personally, but as long as what is passed has a `refuel()` in python it would
work just fine.

Let's test that theory, requirements just changed as usual, we have to support the US military
fighter jets for refuelling.

    * Think about how this would be impacted based on our initial implementation?
        * Firstly, a new block in the `if` statement would be required!
        * Secondly an implementation for refuelling fighter jets would of been implemented in the FuelStation!

    * Now with our refactored approach?
        * Nothing, a FighterJet class needs implemented by the client and things will just work
        * No touching existing code, no limitations for the client and most importantly if the requirements
        change yet again, we have no work to do, our software by design is 100x more maintainable and designed properly.
"""


class FighterJet(Refuellable):
    """
    The client has added a new fighter jet that needs fuelled, no problem with our new design!
    """
    def __init__(self, horse_power: float, brand: str):
        self.horse_power = horse_power
        self.brand = brand

    def refuel(self):
        print("Refuelling the fighter jet!")


def main():
    """
    >>> station = FuelStation()
    >>> jet = FighterJet(1200, "Boeing")
    >>> station.do_refuelling(jet)
    Refuelling the fighter jet!
    >>> station.do_refuelling(PetrolCar())
    Refuelling the petrol car...
    >>> station.do_refuelling(DieselCar())
    Refuelling the diesel car...
    >>> station.do_refuelling(ElectricCar())
    Recharging the electric car...
    """


"""
Some closing notes, obviously this entire concept and design is extremely simplified,
but the same underlying core holds true in any software system, making things extensible
is crucial and reducing the need to go back and rewrite existing code is too, the open
closed principle aims to guide you towards achieving that, often through polymorphism.
"""


if __name__ == "__main__":
    import doctest

    doctest.testmod()