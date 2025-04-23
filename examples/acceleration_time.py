from ev_optimisation.physics_model import (
    motor_driving_force,
    rpm_to_rads,
    time_to_target_speed,
)

if __name__ == "__main__":

    # example for calculating acceleration speed
    m_kg = 1500
    p_tire_bar = 2.5
    motor_rpm = 6000
    motor_power_W = 50_000
    r_tire_m = 0.65
    A_m2 = 2.2
    c_d = 0.25
    gear_ratio = 10

    # acceleration time
    F_drive = motor_driving_force(
        motor_power_W, rpm_to_rads(motor_rpm), gear_ratio, r_tire_m
    )
    ev_time = time_to_target_speed(F_drive, p_tire_bar, m_kg, A_m2, c_d)
    print(f"{ev_time=:0.2f}")
