from ev_optimisation.model import coeff_rolling_resistance
import pytest


@pytest.mark.parametrize("P, v, expected_c", [(2.9, 90, 0.011), (3.5, 90, 0.010)])
def test_coeff_rolling_resistance(P, v, expected_c):
    """Expected values are taking from 'engineeringtoolbox.com'."""
    c = coeff_rolling_resistance(P, v)

    assert c == pytest.approx(expected_c, abs=1e-3)
