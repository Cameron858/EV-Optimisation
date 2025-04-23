import random
from typing import Callable

from ev_optimisation.vehicle import Vehicle


def _blx_alpha_bounds(gene_1: float, gene_2: float, alpha: float):
    """Calculates lower and upperbounds."""
    diff = abs(gene_1 - gene_2)
    diff_scaled = diff * alpha

    lower_bound = min(gene_1, gene_2) - diff_scaled
    upper_bound = max(gene_1, gene_2) + diff_scaled

    return (lower_bound, upper_bound)


def blx_alpha(gene_1: float, gene_2: float, alpha: float = 0.2) -> float:
    """Perform BLX-a crossover as proposed by Eshelman and Schaffer (1993).

    Larger alpha `a` values generate solutions further outside the parent range.
    """
    lower_bound, upper_bound = _blx_alpha_bounds(gene_1, gene_2, alpha)
    return random.uniform(lower_bound, upper_bound)


def crossover(
    parent_1: Vehicle,
    parent_2: Vehicle,
    operator: Callable = blx_alpha,
    **operator_kwargs,
) -> Vehicle:
    """Perform genetic crossover from two parents."""
    return Vehicle(
        motor_power=operator(
            parent_1.motor_power, parent_2.motor_power, **operator_kwargs
        ),
        battery_capacity=operator(
            parent_1.battery_capacity, parent_2.battery_capacity, **operator_kwargs
        ),
    )


def polynomial_mutation(x: float, bounds: tuple, eta=5) -> float:
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
        Higher values of `eta` result in smaller mutations. Default is 5.

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


def mutate(vehicle: Vehicle, rate: float, eta: int = 5) -> Vehicle:
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
        Higher values of `eta` result in smaller mutations. Default is 5.

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
