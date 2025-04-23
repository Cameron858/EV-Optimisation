from ev_optimisation.vehicle import Vehicle
from ev_optimisation.operators import mutate
import pytest


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
