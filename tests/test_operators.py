from itertools import permutations

import numpy as np
import pytest

from ev_optimisation.operators import mutate, sbx_crossover
from ev_optimisation.vehicle import Vehicle


@pytest.mark.parametrize(
    "rate, raises",
    [
        (-1, True),
        (-0.01, True),
        (0, False),
        (0.01, False),
        (0.5, False),
        (0.99, False),
        (1, False),
        (1.01, True),
        (10, True),
    ],
)
def test_that_mutation_rate_raises_value_error_where_applicable(rate, raises):

    v = Vehicle(100, 100)

    if raises:
        with pytest.raises(ValueError) as exc_info:
            v = mutate(v, rate)
            assert (
                str(exc_info.value)
                == f"Mutation rate must be in range [0, 1]. Given: {rate}"
            )
    else:
        v = mutate(v, rate)


def test_that_zero_mutation_rate_produces_no_mutations():
    v = Vehicle(100, 100)

    before_motor_power = v.motor_power
    before_battery_capacity = v.battery_capacity

    v = mutate(v, 0)

    # core attributes
    assert v.motor_power == before_motor_power
    assert v.battery_capacity == before_battery_capacity


def test_that_one_mutation_rate_always_produces_mutations(mocker):
    """This test also checks that derived attributes such as component weights are updated."""

    v = Vehicle(100, 100)

    before_motor_power = v.motor_power
    before_battery_capacity = v.battery_capacity

    v = mutate(v, 1)

    # core attributes
    assert v.motor_power != before_motor_power
    assert v.battery_capacity != before_battery_capacity


def test_that_sbx_crossover_is_symmetrical(mocker):

    # Ensure the crossover operation is deterministic for testing
    mocker.patch("numpy.random.uniform", return_value=0.5)

    parent1 = Vehicle(motor_power=100, battery_capacity=50)
    parent2 = Vehicle(motor_power=200, battery_capacity=100)

    c1, c2 = sbx_crossover(parent1, parent2)
    c3, c4 = sbx_crossover(parent2, parent1)

    assert np.allclose(c1.to_array(), c4.to_array())
    assert np.allclose(c2.to_array(), c3.to_array())


def test_that_sbx_crossover_produces_diverse_offspring_for_low_eta_value():

    parent1 = Vehicle(motor_power=100, battery_capacity=50)
    parent2 = Vehicle(motor_power=200, battery_capacity=100)

    # a low eta values ensures that the child are far from the parents
    c1, c2 = sbx_crossover(parent1, parent2, eta=1)

    assert not np.allclose(c1.to_array(), parent1.to_array())
    assert not np.allclose(c2.to_array(), parent2.to_array())


def test_that_eta_value_effects_the_diversty_of_sbx_crossover_offspring():
    parent1 = Vehicle(motor_power=100, battery_capacity=50)
    parent2 = Vehicle(motor_power=200, battery_capacity=100)

    # lower eta -> more diverse offspring
    c1_low, c2_low = sbx_crossover(parent1, parent2, eta=1)

    # higher eta -> less diverse offspring
    c1_high, c2_high = sbx_crossover(parent1, parent2, eta=50)

    # Check that offspring with low eta are more diverse from parents
    assert not np.allclose(c1_low.to_array(), parent1.to_array())
    assert not np.allclose(c2_low.to_array(), parent2.to_array())

    # Check that offspring with high eta are closer to parents
    assert np.allclose(c1_high.to_array(), parent1.to_array(), atol=10)
    assert np.allclose(c2_high.to_array(), parent2.to_array(), atol=10)


def test_that_sbx_crossover_exhibits_randomness():

    parent1 = Vehicle(motor_power=100, battery_capacity=50)
    parent2 = Vehicle(motor_power=200, battery_capacity=100)

    c1, c2 = sbx_crossover(parent1, parent2)
    c3, c4 = sbx_crossover(parent1, parent2)

    for ci, cj in permutations([c1, c2, c3, c4], 2):
        assert not np.allclose(ci.to_array(), cj.to_array())
