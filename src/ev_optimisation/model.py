import math


def rpm_to_rads(rpm):
    """Convert RPM to rads-1"""
    return (rpm * 2 * math.pi) / 60


def rolling_resistance_force(c: float, m: float, g=9.81):
    """Calculate the rolling resistance force in N.

    Parameters
    -----------
    c : float
        rolling resistance coefficient
    m : float
        mass in [kg]
    g : float = 9.81
        acceleration due to gravity [ms-2]
    """
    return c * m * g
