from ev_optimisation.model import rpm_to_rads, coeff_rolling_resistance
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
