from typing import Any
import matplotlib.pyplot as plt
import numpy as np
from ev_optimisation.vehicle import Vehicle


def plot_population(p: list[Vehicle], marker_scaler=75) -> tuple[plt.Figure, Any]:

    fig, ax = plt.subplots(figsize=(8, 5))

    # extract pop values as arrays
    powers = [v.motor_power for v in p]
    capacities = [v.battery_capacity for v in p]
    masses = [v.mass() / 5 for v in p]

    # scale masses for marker size
    sizes = [np.exp(m / marker_scaler) for m in masses]

    # plot values
    plt.scatter(x=powers, y=capacities, s=sizes)

    # annotate the masses
    for x, y, mass in zip(powers, capacities, masses):
        plt.annotate(
            f"{mass:.0f}kg",
            (x, y),
            textcoords="offset points",
            xytext=(5, 5),
            ha="left",
            fontsize=8,
        )

    # update axis labels
    plt.title("Power [kW] vs Capacity [kWh] (Size = Mass, Label = Mass)")
    plt.xlabel("Motor Power [kW]")
    plt.ylabel("Battery Capacity [kWh]")
    plt.grid(True)

    return fig, ax
