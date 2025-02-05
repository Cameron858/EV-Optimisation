type kg = float | int
type kW = float | int
type kWh = float | int


class Vehicle:

    def __init__(self, motor_power: kW, battery_capacity: kWh, frame_weight: kg):
        """
        motor_power: kW
        battery_capacity: kWh
        frame_weight: kg
        """
        self.motor_power = motor_power
        self.motor_weight: kg = motor_power * 6
        self.battery_capacity = battery_capacity
        self.battery_weight: kg = battery_capacity * 4
        self.frame_weight = frame_weight


if __name__ == "__main__":

    v = Vehicle(100, 200, 500)
