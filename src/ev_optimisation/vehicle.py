import logging
import random


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

        if logger is None:
            self.logger = logging.getLogger("vehicle")

    def mutate(self, rate: float) -> None:
        """Mutate an instances genes."""
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

    def _update_motor_weight(self):
        self.motor_weight: kg = self.motor_power * Vehicle.MOTOR_WEIGHT_RATIO

    def _update_battery_weight(self):
        self.battery_weight: kg = self.battery_capacity * Vehicle.BATTERY_WEIGHT_RATIO


if __name__ == "__main__":

    v = Vehicle(100, 200, 500)
