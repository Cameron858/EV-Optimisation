import math


def rpm_to_rads(rpm):
    """Convert RPM to rads-1"""
    return (rpm * 2 * math.pi) / 60


def kmh_to_ms(kmh):
    """Convert kmh-1 to ms-1"""
    return kmh / 3.6


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


def aerodynamic_drag_force(c, v, a, p=1.2):
    """Calculate the drag force due to air resistance in N.

    Parameters
    -----------
    c : float
        Coefficient of drag
    v : float
        Velocity in [ms-1]
    a : float
        Frontal area in [m2]
    p : float, optional
        Density of fluid in [kgm-3]. Defaults to 1.2 for air at NTP.
    """
    return c * 0.5 * p * (v**2) * a
