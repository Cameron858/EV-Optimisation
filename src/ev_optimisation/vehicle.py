import logging
import random
from dataclasses import dataclass, field
from .operators import polynomial_mutation

type kg = float | int
type kW = float | int
type kWh = float | int


@dataclass
class Vehicle:
    # not to be confused with mutation rate, which is determined outside this class
    # This defines the +-% that a mutation can possible change by
    # i.e. mutated_x = x * (1 + uniform(-0.1, 0.1))
    MUTATION_PERC_CHANGE: float = field(default=0.05, init=False)

    BATTERY_CAPACITY_BOUNDS: tuple[float] = field(default=(30, 150), init=False)  # kWh
    MOTOR_WEIGHT_BOUNDS: tuple[float] = field(default=(50, 500), init=False)  # kW

    BATTERY_WEIGHT_RATIO: float = field(default=6, init=False)  # kg/kWh
    MOTOR_WEIGHT_RATIO: float = field(default=4, init=False)  # kg/kW

    motor_power: kW
    battery_capacity: kWh
    logger: logging.Logger = field(default=logging.getLogger("vehicle"))

    @property
    def motor_weight(self) -> kg:
        return self.motor_power * self.MOTOR_WEIGHT_RATIO

    @property
    def battery_weight(self) -> kg:
        return self.battery_capacity * self.BATTERY_WEIGHT_RATIO

    def mass(self) -> kg:
        return self.motor_weight + self.battery_weight

    def mutate(self, rate: float, eta: int = 5) -> None:
        """Mutate the vehicle's attributes inplace independently using polynomial mutation.

        Parameters
        -----------
        eta : int, optional
            The distribution index that controls the extent of the mutation.
            Higher values of `eta` result in smaller mutations. Default is 5.
        """
        if not 0 <= rate <= 1:
            raise ValueError(f"Mutation rate must be in range [0, 1]. Given: {rate}")

        if random.random() < rate:
            self.motor_power = polynomial_mutation(
                self.motor_power, self.MOTOR_WEIGHT_BOUNDS
            )

        if random.random() < rate:
            self.battery_capacity = polynomial_mutation(
                self.battery_capacity, self.BATTERY_CAPACITY_BOUNDS
            )
