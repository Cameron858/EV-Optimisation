from ev_optimisation.physics_model import (
    coeff_rolling_resistance,
    drag_force,
    kmh_to_ms,
    rolling_resistance_force,
    time_to_battery_drain,
)

if __name__ == "__main__":

    # example for calculating range
    v_cruising_kmh = 100
    m_kg = 1500
    p_tire_bar = 2.5
    A_m2 = 2.2
    c_d = 0.25
    drivetrain_eff = 1.0
    battery_capacity_kWh = 80

    v_cruising_ms = kmh_to_ms(v_cruising_kmh)

    # rolling resistance
    c_r = coeff_rolling_resistance(p_tire_bar, v_cruising_kmh)
    F_rolling = rolling_resistance_force(c_r, m_kg)

    # drag (constant)
    F_drag = drag_force(c_d, v_cruising_ms, A_m2)

    # range
    F_total = F_drag + F_rolling
    battery_run_time_hrs = time_to_battery_drain(
        F_total, v_cruising_kmh, drivetrain_eff, battery_capacity_kWh
    )
    ev_range_km = battery_run_time_hrs * v_cruising_kmh
    print(f"{ev_range_km=:.2f}km")
