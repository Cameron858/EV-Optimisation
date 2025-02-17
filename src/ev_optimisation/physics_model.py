import math


def rpm_to_rads(rpm):
    """Convert RPM to rads-1"""
    return (rpm * 2 * math.pi) / 60


def kmh_to_ms(kmh):
    """Convert kmh-1 to ms-1"""
    return kmh / 3.6


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


def ev_range(F, v_kmh, drivetrain_eff, battery_kWh):
    """Calculate the range of an EV at a constant velocity.

    This function uses the following assumptions:
    - The vehicle is travelling at constant speed
    - All energy consumption is used for maintaining speed
    - The vehicle is travelling in an infinite flat plane
    - No energy is lost in getting up to speed, i.e. the vehicle instantaneously accelerates to the given `v_kmh`

    Parameters
    -----------
    F : float
        The force required to maintain constant speed in [N]
    v_kmh : float
        The cruising speed of the vehicle in [kmh-1]
    drivetrain_eff : float
        The efficiency of the drivetrain. Must be in range [0, 1] inclusive.
    battery_kWh : float
        The capacity of the battery in [kWh]

    Returns
    -------
    float
        Range in [km]
    """
    # P (W) = F (N) * v (ms-1)
    P_required_W = F * kmh_to_ms(v_kmh)

    P_required_kW = P_required_W / 1000

    # account for drivetrain efficiency
    P_required_kW = P_required_kW / drivetrain_eff

    t_hrs = battery_kWh / P_required_kW
    return v_kmh * t_hrs


if __name__ == "__main__":

    # example for calculating range
    v_cruising_kmh = 100
    m_kg = 1500
    p_tire_bar = 2.5
    motor_rpm = 6000
    motor_power_W = 50_000
    r_tire_m = 0.65
    A_m2 = 2.2
    c_d = 0.25
    gear_ratio = 10
    drivetrain_eff = 1.0
    battery_capacity_kWh = 80

    v_cruising_ms = kmh_to_ms(v_cruising_kmh)

    # driving force from motor
    w_motor_rads = rpm_to_rads(motor_rpm)
    F_drive = motor_driving_force(motor_power_W, w_motor_rads, gear_ratio, r_tire_m)

    # rolling resistance
    c_r = coeff_rolling_resistance(p_tire_bar, v_cruising_kmh)
    F_rolling = rolling_resistance_force(c_r, m_kg)

    # drag (constant)
    F_drag = drag_force(c_d, v_cruising_ms, A_m2)

    # range
    F_total = F_drag + F_rolling
    ev_range_km = ev_range(
        F_total, v_cruising_kmh, drivetrain_eff, battery_capacity_kWh
    )
    print(f"{ev_range_km=:.2f}km")
