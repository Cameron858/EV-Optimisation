import logging
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

    BATTERY_CAPACITY_BOUNDS: tuple[float] = field(default=(30, 150), init=False)  # kWh
    MOTOR_POWER_BOUNDS: tuple[float] = field(default=(50, 500), init=False)  # kW

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

    def __repr__(self) -> str:
        return (
            f"Vehicle(motor_power={self.motor_power:0.2f} kW, "
            f"battery_capacity={self.battery_capacity:0.2f} kWh, "
            f"mass={self.mass():0.2f} kg)"
        )


@dataclass
class VehicleConfig:
    """Configurable metadata for vehicle physics simulations."""

    p_tire_bar: float = 2.5  # Tire pressure [bar]
    motor_rpm: int = 6000  # Motor max RPM
    r_tire_m: float = 0.65  # Tire radius [m]
    A_m2: float = 2.2  # Frontal area [m²]
    c_d: float = 0.25  # Drag coefficient
    gear_ratio: float = 10  # Gear ratio (unitless)
    v_cruising_kmh: float = 100  # Cruising speed [km/h]
    drivetrain_eff: float = 1.0  # Drivetrain efficiency [0-1]
