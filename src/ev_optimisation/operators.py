import random

import numpy as np

from ev_optimisation.vehicle import Vehicle


def polynomial_mutation(x: float, bounds: tuple, eta: int = 20) -> float:
    """
    Perform polynomial mutation on a given real encoded value.

    Clip mutated value to `bounds`.

    Parameters
    ----------
    x : float
        The input value to be mutated.
    bounds : tuple
        A tuple specifying the lower and upper bounds for the mutation
        (bounds[0] is the lower bound, bounds[1] is the upper bound).
    eta : int, optional
        The distribution index that controls the extent of the mutation.
        Higher values of `eta` result in smaller mutations. Default is 20.

    Returns
    -------
    float
        The mutated value.
    """
    u = random.uniform(0, 1)
    exponent = 1 / (1 + eta)
    if u < 0.5:
        delta = (2 * u) ** exponent - 1
    else:
        delta = 1 - (2 * (1 - u)) ** exponent

    x_mutated = x + delta * (bounds[1] - bounds[0])
    x_mutated = max(bounds[0], min(bounds[1], x_mutated))

    return x_mutated


def mutate(vehicle: Vehicle, rate: float, eta: int = 20) -> Vehicle:
    """
    Mutate the vehicle's attributes independently using polynomial mutation. Return new instance.

    Parameters
    ----------
    vehicle : Vehicle
        The vehicle object whose attributes will be mutated.
    rate : float
        The probability of mutation for each attribute. Must be in the range [0, 1].
    eta : int, optional
        The distribution index that controls the extent of the mutation.
        Higher values of `eta` result in smaller mutations. Default is 20.

    Returns
    -------
    Vehicle
        A new `Vehicle` object with mutated attributes.

    Raises
    ------
    ValueError
        If the mutation rate `rate` is not in the range [0, 1].
    """
    if not 0 <= rate <= 1:
        raise ValueError(f"Mutation rate must be in range [0, 1]. Given: {rate}")

    power, capacity = vehicle.motor_power, vehicle.battery_capacity

    if random.random() < rate:
        power = polynomial_mutation(power, Vehicle.MOTOR_POWER_BOUNDS, eta=eta)

    if random.random() < rate:
        capacity = polynomial_mutation(
            capacity, Vehicle.BATTERY_CAPACITY_BOUNDS, eta=eta
        )

    return Vehicle(motor_power=power, battery_capacity=capacity)


def sbx_crossover(parent1: Vehicle, parent2: Vehicle, eta=20) -> tuple[Vehicle]:
    """
    Performs Simulated Binary Crossover (SBX) on two parent `Vehicle` objects.

    Parameters
    ----------
    parent1 : Vehicle
        The first parent individual.
    parent2 : Vehicle
        The second parent individual.
    eta : int, optional
        The distribution index, which controls the spread of offspring solutions.
        Higher values result in offspring closer to the parents. Default is 20.

    Returns
    -------
    tuple[Vehicle]
        A tuple containing two offspring `Vehicle` objects generated from the
        crossover operation.
    """
    eta = 5
    u = np.random.uniform()

    exponent = 1 / (eta + 1)

    beta = np.where(u <= 0.5, (2 * u) ** exponent, (2 * (1 - u)) ** -exponent)

    c1_values = 0.5 * (
        (1 + beta) * parent1.to_array() + (1 - beta) * parent2.to_array()
    )
    c2_values = 0.5 * (
        (1 - beta) * parent1.to_array() + (1 + beta) * parent2.to_array()
    )

    c1 = Vehicle(*c1_values)
    c2 = Vehicle(*c2_values)

    return c1, c2
