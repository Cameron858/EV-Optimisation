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
    **operator_kwargs
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
