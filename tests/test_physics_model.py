from ev_optimisation.physics_model import (
    drag_force,
    kmh_to_ms,
    rolling_resistance_force,
    rpm_to_rads,
    coeff_rolling_resistance,
    ev_range,
)
import pytest


@pytest.mark.parametrize("rpm, expected_rads", [(1, 0.10472), (6000, 628.3)])
def test_rpm_rads_conversion(rpm, expected_rads):

    rads = rpm_to_rads(rpm)

    assert rads == pytest.approx(expected_rads, 0.01)


@pytest.mark.parametrize("P, v, expected_c", [(2.9, 90, 0.011), (3.5, 90, 0.010)])
def test_coeff_rolling_resistance(P, v, expected_c):
    """Expected values are taking from 'engineeringtoolbox.com'."""
    c = coeff_rolling_resistance(P, v)

    assert c == pytest.approx(expected_c, 0.01)


@pytest.mark.parametrize("v1, v2", [(10, 100), (10, 11), (1, 1.1), (10, 10.1)])
def test_that_higher_velocity_reduces_range(v1, v2):
    """v1 range should be lower than v2 range."""
    # values are abitary. They are constant across both velocity cases
    m_kg = 1500
    p_tire_bar = 2.5
    A_m2 = 2.2
    c_d = 0.25
    drivetrain_eff = 1.0
    battery_capacity_kWh = 100

    def calc_range(v):
        c_r = coeff_rolling_resistance(p_tire_bar, v)
        F_rolling = rolling_resistance_force(c_r, m_kg)
        F_drag = drag_force(c_d, kmh_to_ms(v), A_m2)
        F_total = F_drag + F_rolling
        return ev_range(F_total, v, drivetrain_eff, battery_capacity_kWh)

    assert calc_range(v1) > calc_range(v2)


@pytest.mark.parametrize("b1, b2", [(1, 10), (10, 11), (10, 10.1)])
def test_that_larger_battery_capacity_increases_range(b1, b2):
    assert ev_range(1000, 100, 1, b1) < ev_range(1000, 100, 1, b2)


@pytest.mark.parametrize("eff1, eff2", [(1, 0.1), (1, 0.9), (1, 0.99), (0.5, 0.3)])
def test_that_lower_drivetrain_efficiencies_reduces_range(eff1, eff2):
    assert ev_range(1000, 100, eff1, 80) > ev_range(1000, 100, eff2, 80)


@pytest.mark.parametrize(
    "eta, raises", [(0, True), (0.5, False), (1, False), (1.1, True)]
)
def test_that_ev_range_raises_error_where_applicable(eta, raises):
    if raises:
        with pytest.raises(ValueError) as exc_info:
            ev_range(1000, 100, eta, 80)

            assert (
                str(exc_info.value)
                == f"Drivetrain efficiency must be in range 0 < eta <= 1. Given: {eta}"
            )
    else:
        ev_range(1000, 100, eta, 80)
