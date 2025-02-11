import math


def rpm_to_rads(rpm):
    """Convert RPM to rads-1"""
    return (rpm * 2 * math.pi) / 60


def coeff_rolling_resistance(tire_pressure: float, velocity: float):
    """Calculate the coefficient of rolling resistance.

    Parameters
    -----------
    tire_pressure : float
        Tire pressure in [bar]
    velocity : float
        Velocity of vehicle in [kmh-1]
    """
    velocity_term = 0.0095 * (velocity / 100) ** 2
    return 0.005 + (1 / tire_pressure) * (0.01 + velocity_term)


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
