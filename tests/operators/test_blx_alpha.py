import random
from ev_optimisation.operators import blx_alpha


def test_blx_alpha_within_bounds():
    random.seed(42)
    gene_1, gene_2 = 3.0, 7.0
    alpha = 0.2
    result = blx_alpha(gene_1, gene_2, alpha)

    lower_bound = min(gene_1, gene_2) - alpha * abs(gene_1 - gene_2)
    upper_bound = max(gene_1, gene_2) + alpha * abs(gene_1 - gene_2)

    assert lower_bound <= result <= upper_bound


def test_that_blx_alpha_is_symmetrical_for_swapped_inputs():
    random.seed(42)
    result1 = blx_alpha(3.0, 7.0, 0.2)
    result2 = blx_alpha(7.0, 3.0, 0.2)

    assert result1 == result2


def test_that_zero_alpha_always_produces_value_in_range():
    random.seed(42)

    result = blx_alpha(7.0, 3.0, 0.2)

    assert 7 <= result <= 3
