import random
from ev_optimisation.vehicle import Vehicle


def create_population(size: int) -> list[Vehicle]:
    """
    Creates a population of Vehicle instances with random motor power and battery capacity.

    Parameters
    ----------
    size : int
        The number of Vehicle instances to create.

    Returns
    -------
    list[Vehicle]
        A list of Vehicle instances with randomly generated attributes.
    """
    p = []
    for _ in range(size):

        power = random.uniform(*Vehicle.MOTOR_POWER_BOUNDS)
        power = round(power, 2)

        capacity = random.uniform(*Vehicle.BATTERY_CAPACITY_BOUNDS)
        capacity = round(capacity, 2)

        v = Vehicle(motor_power=power, battery_capacity=capacity)
        p.append(v)

    return p
