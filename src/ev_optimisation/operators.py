import random


def _blx_alpha_bounds(gene_1: float, gene_2: float, alpha: float):
    """Calculates lower and upperbounds."""
    diff = abs(gene_1 - gene_2)
    diff_scaled = diff * alpha

    lower_bound = min(gene_1, gene_2) - diff_scaled
    upper_bound = max(gene_1, gene_2) + diff_scaled

    return (lower_bound, upper_bound)


def blx_alpha(gene_1: float, gene_2: float, alpha: float = 0.2) -> float:
    """Perform BLX-a crossover as proposed by Eshelman and Schaffer (1993).

    Larger alpha `a` values generate solutions further outside the parent range.
    """
    lower_bound, upper_bound = _blx_alpha_bounds(gene_1, gene_2, alpha)
    return random.uniform(lower_bound, upper_bound)
