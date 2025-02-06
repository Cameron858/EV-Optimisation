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
