import math


def rpm_to_rads(rpm):
    """Convert RPM to rads-1"""
    return (rpm * 2 * math.pi) / 60


def kmh_to_ms(kmh):
    """Convert kmh-1 to ms-1"""
    return kmh / 3.6


def ms_to_kmh(ms):
    """Convert ms-1 to kmh-1"""
    return ms * 3.6


def motor_driving_force(motor_power, motor_rads, gear_ratio, tire_radius):
    """Calculate the driving force at the wheels from the motor in N.

    F = P / wr

    Parameters
    -----------
    motor_power : float
        Power of motor in [W]
    motor_rads : float
        Angular velocity of motor in [rads-1]
    gear_ratio : float
        Final gear ratio of drivetrain.
    tire_radius : float
        Radius of tire in [m]
    """
    w_wheel_rads = motor_rads / gear_ratio
    return motor_power / (w_wheel_rads * tire_radius)


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


def drag_force(c, v, a, rho=1.2):
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
    return c * 0.5 * rho * (v**2) * a


def time_to_battery_drain(F, v_kmh, drivetrain_eff, battery_kWh):
    """Calculate the time in [hrs] for a battery to drain at a constant speed.

    Method:
        1. The power required is found from `P = F x v`
        2. Accounting for drive train efficiency: P = P / n
        3. Time is found via: t = E[kWh] / P[kW]

    Parameters
    -----------
    F : float
        The force required to maintain constant speed in [N]
    v_kmh : float
        The cruising speed of the vehicle in [kmh-1]
    drivetrain_eff : float
        The efficiency of the drivetrain. Must be in range 0 < eta <= 1 inclusive.
    battery_kWh : float
        The capacity of the battery in [kWh]

    Returns
    -------
    t_hrs : float
        Time in [hrs]
    """

    if not 0 < drivetrain_eff <= 1:
        raise ValueError(
            f"Drivetrain efficiency must be in range 0 < eta <= 1. Given: {drivetrain_eff}"
        )

    # P (W) = F (N) * v (ms-1)
    P_required_W = F * kmh_to_ms(v_kmh)

    P_required_kW = P_required_W / 1000

    # account for drivetrain efficiency
    P_required_kW = P_required_kW / drivetrain_eff

    t_hrs = battery_kWh / P_required_kW
    return t_hrs


def time_to_target_speed(
    F_drive,
    p_tire_bar,
    m_kg,
    A_m2,
    c_d,
    v_target_kmh=100,
    dt=0.01,
):
    """Calculate the time required for an EV to reach a target speed.

    This function uses an Euler integration.

    Parameters
    -----------
    F_drive : float
        Constant driving force from motor in [N]
    p_tire_bar : float
        Tire pressure in [bar].
    m_kg : float
        Mass of the vehicle in [kg].
    A_m2 : float
        Cross-sectional area of the vehicle in [m2].
    c_d : float
        Drag coefficient.
    v_target_kmh : float
        Target speed in [kmh-1] (default is 100kmh-1).
    dt : float, optional
        Time step in seconds (default is 0.01s).

    Returns
    -------
    float
        Time in seconds to reach the target speed.
    """
    v = 0  # ms-1
    v_max = kmh_to_ms(v_target_kmh)  # ms-1
    t = 0  # s

    while v < round(v_max, 2):

        # calculate resistive forces
        c_r = coeff_rolling_resistance(p_tire_bar, ms_to_kmh(v))
        F_rolling = rolling_resistance_force(c_r, m_kg)
        F_drag = drag_force(c_d, v, A_m2)

        F_net = F_drive - sum((F_drag, F_rolling))
        a = F_net / m_kg

        # update values
        v += a * dt
        t += dt

    return t


def range_of_ev(
    v_kmh, p_tire_bar, m_kg, battery_capacity_kWh, c_d, A_m2, drivetrain_eff
):
    """Calculate the range in [km] of a vehicle.

    This function uses the following assumptions:
    - The vehicle is travelling at constant speed
    - All energy consumption is used for maintaining speed
    - The vehicle is travelling in an infinite flat plane
    - No energy is lost in getting up to speed, i.e. the vehicle instantaneously accelerates to the given `v_kmh`

    Parameters
    -----------
    v_kmh : float
        The cruising speed of the vehicle in [kmh-1]
    p_tire_bar : float
        Tire pressure in [bar].
    m_kg : float
        Mass of the vehicle in [kg].
    battery_kWh : float
        The capacity of the battery in [kWh]
    A_m2 : float
        Cross-sectional area of the vehicle in [m2].
    c_d : float
        Drag coefficient.
    drivetrain_eff : float
        The efficiency of the drivetrain. Must be in range 0 < eta <= 1 inclusive.
    """
    v_cruising_ms = kmh_to_ms(v_kmh)

    # rolling resistance
    c_r = coeff_rolling_resistance(p_tire_bar, v_kmh)
    F_rolling = rolling_resistance_force(c_r, m_kg)

    # drag (constant)
    F_drag = drag_force(c_d, v_cruising_ms, A_m2)

    # range
    F_total = F_drag + F_rolling
    battery_run_time_hrs = time_to_battery_drain(
        F_total, v_kmh, drivetrain_eff, battery_capacity_kWh
    )
    ev_range_km = battery_run_time_hrs * v_kmh
    return ev_range_km
