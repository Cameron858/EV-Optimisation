from typing import Any
import matplotlib.pyplot as plt
import numpy as np
from ev_optimisation.vehicle import GenerationResult, Vehicle
import plotly.graph_objects as go


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
    for i, (x, y, mass) in enumerate(zip(powers, capacities, masses)):
        plt.annotate(
            f"{i}: {mass:.0f}kg",
            (x, y),
            textcoords="offset points",
            xytext=(5, 5),
            ha="left",
            fontsize=8,
        )

    # update axis labels
    plt.title("Power [kW] vs Capacity [kWh] (Size = Mass, Label = Index: Mass)")
    plt.xlabel("Motor Power [kW]")
    plt.ylabel("Battery Capacity [kWh]")
    plt.grid(True)

    return fig, ax


def plot_result(result: GenerationResult, fig=None):
    """
    Plot the result of a generation.

    Parameters
    ----------
    result : GenerationResult
        The result of a generation containing the population to be plotted.
    fig : plotly.graph_objects.Figure, optional
        An existing figure to which the population will be added. If None, a new figure is created.

    Returns
    -------
    plotly.graph_objects.Figure
        The figure containing the plotted population.

    Notes
    -----
    The size of the markers is proportional to the square of the normalised mass of the vehicles.
    """
    if fig is None:
        fig = go.Figure()
        fig.update_layout(
            title=f"Population {result.generation}",
            xaxis_title="Motor Power [kW]",
            yaxis_title="Battery Capacity [kWh]",
        )

    pop_array = np.array(
        [(v.motor_power, v.battery_capacity, v.mass()) for v in result.population]
    )

    marker_sizes = 75 * ((pop_array[:, 2] / pop_array[:, 2].max()) ** 2 + 0.1)

    fig.add_trace(
        go.Scatter(
            # power
            x=pop_array[:, 0],
            # capacity
            y=pop_array[:, 1],
            mode="markers",
            marker={"size": marker_sizes},
            name="",
            hovertemplate=(
                "Power: %{x:.2f} kW<br>"
                "Capacity: %{y:.2f} kWh<br>"
                "Mass: %{meta:.2f} kg<br>"
            ),
            meta=pop_array[:, 2],
        )
    )

    return fig
