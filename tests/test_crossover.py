import random
from ev_optimisation.operators import _blx_alpha_bounds, crossover
from ev_optimisation.vehicle import Vehicle


def test_that_crossover_creates_valid_vehicle():
    parent_1 = Vehicle(motor_power=100, battery_capacity=50)
    parent_2 = Vehicle(motor_power=120, battery_capacity=60)

    child = crossover(parent_1, parent_2)

    assert isinstance(child, Vehicle)


def test_that_crossover_produces_varied_offspring():
    parent_1 = Vehicle(motor_power=100, battery_capacity=50)
    parent_2 = Vehicle(motor_power=120, battery_capacity=60)

    random.seed(42)
    child_1 = crossover(parent_1, parent_2)
    child_2 = crossover(parent_1, parent_2)

    assert child_1 != child_2


def test_that_crossover_produces_offspring_withing_correct_gene_bounds():
    """Check that BLX-alpha crossover generates offspring within the expected range."""
    parent_1 = Vehicle(motor_power=100, battery_capacity=50)
    parent_2 = Vehicle(motor_power=120, battery_capacity=60)

    alpha = 0.2
    child = crossover(parent_1, parent_2, alpha=alpha)

    lower_motor, upper_motor = _blx_alpha_bounds(
        parent_1.motor_power, parent_2.motor_power, alpha
    )
    lower_battery, upper_battery = _blx_alpha_bounds(
        parent_1.battery_capacity, parent_2.battery_capacity, alpha
    )

    assert lower_motor <= child.motor_power <= upper_motor
    assert lower_battery <= child.battery_capacity <= upper_battery
