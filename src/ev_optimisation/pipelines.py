from ev_optimisation.vehicle import Vehicle, VehicleConfig
from ev_optimisation.physics_model import (
    coeff_rolling_resistance,
    drag_force,
    kmh_to_ms,
    rolling_resistance_force,
    time_to_battery_drain,
    motor_driving_force,
    rpm_to_rads,
    time_to_target_speed,
)
import numpy as np
from functools import partial


def vehicle_acc_time(vehicle: Vehicle, config: VehicleConfig) -> float:
    """
    Calculate the acceleration time of a vehicle to reach a target speed.

    Parameters
    ----------
    vehicle : Vehicle
        The vehicle object containing properties such as motor power and mass.
    config : VehicleConfig
        The configuration object containing parameters for the vehicle.

    Returns
    -------
    float
        The time (in seconds) required for the vehicle to reach the target speed.
    """
    F_drive = motor_driving_force(
        vehicle.motor_power * 1000,
        rpm_to_rads(config.motor_rpm),
        config.gear_ratio,
        config.r_tire_m,
    )

    time = time_to_target_speed(
        F_drive, config.p_tire_bar, vehicle.mass(), config.A_m2, config.c_d
    )

    return time


def vehicle_range(vehicle: Vehicle, config: VehicleConfig) -> float:
    """
    Calculate the estimated range of a vehicle based on its configuration and properties.

    Parameters
    ----------
    vehicle : Vehicle
        The vehicle object containing properties such as mass and battery capacity.
    config : VehicleConfig
        The configuration object containing parameters for the vehicle.

    Returns
    -------
    float
        The estimated range of the vehicle in kilometers.
    """
    # rolling resistance
    c_r = coeff_rolling_resistance(config.p_tire_bar, config.v_cruising_kmh)
    F_rolling = rolling_resistance_force(c_r, vehicle.mass())

    # drag (constant)
    v_cruising_ms = kmh_to_ms(config.v_cruising_kmh)
    F_drag = drag_force(config.c_d, v_cruising_ms, config.A_m2)

    # range
    F_total = F_drag + F_rolling
    battery_run_time_hrs = time_to_battery_drain(
        F_total, config.v_cruising_kmh, config.drivetrain_eff, vehicle.battery_capacity
    )
    range_km = battery_run_time_hrs * config.v_cruising_kmh

    return range_km


def objective(vehicle: Vehicle, config: VehicleConfig) -> tuple[float]:
    """
    Computes the objective function for vehicle optimisation, which includes
    minimising the negative range and the acceleration time.

    Parameters
    ----------
    vehicle : Vehicle
        The vehicle object containing its properties and state.
    config : VehicleConfig
        The configuration object containing parameters for the vehicle.

    Returns
    -------
    tuple[float]
        A tuple containing:
        - The negated range of the vehicle (to convert it into a minimisation problem).
        - The acceleration time of the vehicle.
    """
    time = vehicle_acc_time(vehicle, config)
    range = vehicle_range(vehicle, config)

    # negate the range to turn both into a minimisation problem
    return (-range, time)


def evaluate_population(p: list[Vehicle], config: VehicleConfig) -> np.ndarray:
    """
    Evaluates a population of vehicles based on a given configuration.

    Parameters
    ----------
    p : list[Vehicle]
        A list of Vehicle objects representing the population to evaluate.
    config : VehicleConfig
        Configuration object containing parameters for the evaluation.

    Returns
    -------
    np.ndarray
        An array of objective values for the evaluated population.
    """
    apply_objective = partial(objective, config=config)

    p_obj = list(map(apply_objective, p))

    return np.array(p_obj)
