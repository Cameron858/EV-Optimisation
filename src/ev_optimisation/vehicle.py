import logging
import random
from typing import Self

from ev_optimisation.operators import blx_alpha


type kg = float | int
type kW = float | int
type kWh = float | int


class Vehicle:
    """Vehicle Genome"""

    # not to be confused with mutation rate, which is determined outside this class
    # This defines the +-% that a mutation can possible change by
    # i.e. mutated_x = x * (1 + uniform(-0.1, 0.1))
    MUTATION_PERC_CHANGE = 0.05
    BATTERY_WEIGHT_RATIO = 6  # kg/kWh
    MOTOR_WEIGHT_RATIO = 4  # kg/kW

    def __init__(
        self,
        motor_power: kW,
        battery_capacity: kWh,
        frame_weight: kg,
        logger: logging.Logger | None = None,
    ):
        """
        motor_power: kW
        battery_capacity: kWh
        frame_weight: kg
        """
        self.motor_power = motor_power
        self.battery_capacity = battery_capacity
        self.frame_weight = frame_weight

        self._update_battery_weight()
        self._update_motor_weight()

        self.logger = logger or logging.getLogger("vehicle")

    def mutate(self, rate: float) -> None:
        """Mutate an instances genes inplace independantly from each other.

        Updates derived attributes, i.e. motor and battery weight.
        """
        if not 0 <= rate <= 1:
            raise ValueError(f"Mutation rate must be in range [0, 1]. Given: {rate}")

        # mutate motor power
        if random.random() < rate:
            self.motor_power *= 1 + random.uniform(
                -Vehicle.MUTATION_PERC_CHANGE, Vehicle.MUTATION_PERC_CHANGE
            )
            self._update_motor_weight()

        # mutate battery capacity
        if random.random() < rate:
            self.battery_capacity *= 1 + random.uniform(
                -Vehicle.MUTATION_PERC_CHANGE, Vehicle.MUTATION_PERC_CHANGE
            )
            self._update_battery_weight()

        # mutate frame weight
        if random.random() < rate:
            self.frame_weight *= 1 + random.uniform(
                -Vehicle.MUTATION_PERC_CHANGE, Vehicle.MUTATION_PERC_CHANGE
            )

    def crossover(self, other: Self) -> Self:
        """Perform genetic crossover between two genomes."""
        child = Vehicle(
            motor_power=blx_alpha(self.motor_power, other.motor_power),
            battery_capacity=blx_alpha(self.battery_capacity, other.battery_capacity),
            frame_weight=blx_alpha(self.frame_weight, other.frame_weight),
        )
        return child

    def _update_motor_weight(self):
        self.motor_weight: kg = self.motor_power * Vehicle.MOTOR_WEIGHT_RATIO

    def _update_battery_weight(self):
        self.battery_weight: kg = self.battery_capacity * Vehicle.BATTERY_WEIGHT_RATIO

    def mass(self):
        return self.motor_weight + self.battery_weight
