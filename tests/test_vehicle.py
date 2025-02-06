import pytest
from ev_optimisation.vehicle import Vehicle


@pytest.mark.parametrize("power, expected_weight", [(100, 400)])
def test_that_motor_weight_is_calculated_correctly_on_init(power, expected_weight):

    # 100 has been chosen as an arbitary value
    v = Vehicle(power, 100, 100)

    assert v.motor_weight == expected_weight


@pytest.mark.parametrize("capacity, expected_weight", [(100, 600)])
def test_that_battery_weight_is_calculated_correctly_on_init(capacity, expected_weight):

    # 100 has been chosen as an arbitary value
    v = Vehicle(100, capacity, 100)

    assert v.battery_weight == expected_weight


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

    v = Vehicle(100, 100, 100)

    if raises:
        with pytest.raises(ValueError) as exc_info:
            v.mutate(rate=rate)
            assert (
                str(exc_info.value)
                == f"Mutation rate must be in range [0, 1]. Given: {rate}"
            )
    else:
        v.mutate(rate=rate)
