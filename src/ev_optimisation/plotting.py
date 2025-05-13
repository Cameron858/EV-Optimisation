from typing import Any
import matplotlib.pyplot as plt
import numpy as np
from ev_optimisation.vehicle import GenerationResult, Vehicle
from pyprojroot import here
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


def _calculate_marker_sizes(masses):
    """
    Calculate marker sizes based on the given masses.

    The marker sizes are scaled proportionally to the square of the normalized masses,
    with a small offset added to ensure a minimum size.

    Parameters
    ----------
    masses : numpy.ndarray
        Array or series of masses.

    Returns
    -------
    numpy.ndarray
        Array of calculated marker sizes.
    """
    offset = 0.1
    return 75 * ((masses / masses.max()) ** 2 + offset)


def _add_scatter(fig: go.Figure, data: np.ndarray, trace_name: str):
    """
    Add a scatter plot to the given Plotly figure inplace.

    Parameters
    ----------
    fig : go.Figure
        The Plotly figure to which the scatter plot will be added.
    data : np.ndarray
        A 2D numpy array where:
        - Column 0 represents the x-axis values (Power in kW).
        - Column 1 represents the y-axis values (Capacity in kWh).
        - Columns 2 and beyond represent metadata (Mass in kg, Range in km, Time in s).
    trace_name : str
        The name of the trace to be displayed in the legend.

    Returns
    -------
    None
        This function modifies the input `fig` in place by adding a scatter trace.
    """
    marker_sizes = _calculate_marker_sizes(data[:, 2])
    fig.add_trace(
        go.Scatter(
            x=data[:, 0],
            y=data[:, 1],
            mode="markers",
            marker={"size": marker_sizes},
            name=trace_name,
            hovertemplate=(
                "Power: %{x:.2f} kW<br>"
                "Capacity: %{y:.2f} kWh<br>"
                "Mass: %{meta[0]:.2f} kg<br>"
                "Range: %{meta[1]:.2f} km<br>"
                "Time: %{meta[2]:.2f} s<br>"
            ),
            meta=data[:, 2:],
            showlegend=True,
        )
    )


def plot_result(result: GenerationResult, fronts=False, fig=None) -> go.Figure:
    """
    Plot the result of a generation.

    Parameters
    ----------
    result : GenerationResult
        The result of a generation containing the population to be plotted.
    fronts: bool, optional
        Add fronts to the plot. Defaults to False
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
        title_suffix = " with Pareto Fronts" if fronts else ""
        fig = go.Figure()
        fig.update_layout(
            title=f"Population {result.generation}{title_suffix}",
            xaxis_title="Motor Power [kW]",
            yaxis_title="Battery Capacity [kWh]",
        )

    # Convert the population and objectives into a structured numpy array for plotting.
    pop_array = np.array(
        [
            (
                v.motor_power,
                v.battery_capacity,
                v.mass(),
                -result.objectives[i, 0],  # Range (km)
                result.objectives[i, 1],  # Time (s)
            )
            for i, v in enumerate(result.population)
        ]
    )

    if not fronts:
        _add_scatter(fig, pop_array, "")
    else:
        pop_array = np.column_stack((pop_array, result.fronts))

        for front in set(result.fronts):
            front_idxs = np.where(pop_array[:, -1] == front)
            front_members = pop_array[front_idxs]

            _add_scatter(fig, front_members, f"Front {int(front)}")

    return fig


def save_plotly_figure(fig: go.Figure, file_name: str) -> None:
    """
    Save a Plotly figure to a file in the default "figures" directory.

    Parameters
    ----------
    fig : plotly.graph_objects.Figure
        The Plotly figure to save.
    file_name : str
        The file name where the figure will be saved. The format is inferred from the file extension.

    Notes
    -----
    Supported file formats include: 'png', 'jpg', 'jpeg', 'webp', 'svg', 'pdf', 'eps', 'json', etc.
    """
    # this can be needed to be explicitly imported for the
    # save operation to run correctly
    import kaleido

    figures_dir = here() / "figures"
    file_path = figures_dir / file_name

    try:
        fig.write_image(str(file_path))
        print(f"Figure saved successfully to {file_path}")
    except ValueError as e:
        print(f"Error saving figure: {e}")
