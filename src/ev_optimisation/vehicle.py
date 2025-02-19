import logging
import random
from dataclasses import dataclass, field

type kg = float | int
type kW = float | int
type kWh = float | int


@dataclass
class Vehicle:
    # not to be confused with mutation rate, which is determined outside this class
    # This defines the +-% that a mutation can possible change by
    # i.e. mutated_x = x * (1 + uniform(-0.1, 0.1))
    MUTATION_PERC_CHANGE: float = field(default=0.05, init=False)
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

    def mutate(self, rate: float) -> None:
        """Mutate the vehicle's attributes independently based on a mutation rate."""
        if not 0 <= rate <= 1:
            raise ValueError(f"Mutation rate must be in range [0, 1]. Given: {rate}")

        if random.random() < rate:
            self.motor_power *= 1 + random.uniform(
                -self.MUTATION_PERC_CHANGE, self.MUTATION_PERC_CHANGE
            )

        if random.random() < rate:
            self.battery_capacity *= 1 + random.uniform(
                -self.MUTATION_PERC_CHANGE, self.MUTATION_PERC_CHANGE
            )
