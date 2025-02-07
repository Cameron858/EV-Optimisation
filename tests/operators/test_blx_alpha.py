import random
from ev_optimisation.operators import _blx_alpha_bounds, blx_alpha
import pytest


def test_that_for_zero_alpha_bounds_are_equal_to_input():
    lb, ub = _blx_alpha_bounds(5, 10, 0)

    assert lb == 5
    assert ub == 10


def test_that_blx_alpha_is_symmetrical_for_swapped_inputs():
    random.seed(42)
    result1 = blx_alpha(3.0, 7.0, 0.2)

    # set seed again to reset sequence random.uniform produces
    random.seed(42)
    result2 = blx_alpha(7.0, 3.0, 0.2)

    assert result1 == result2


@pytest.mark.parametrize("alpha", [0, 0.1, 0.5, 0.9, 1])
def test_that_bounds_are_equal_to_inputs_for_equal_gene_values_independant_of_alpha(
    alpha,
):
    lb, ub = _blx_alpha_bounds(10, 10, alpha)

    assert lb == 10
    assert ub == 10
