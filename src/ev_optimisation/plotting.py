from typing import Any, Literal

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objects as go
from pyprojroot import here

from ev_optimisation.vehicle import GenerationResult, Vehicle


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


def _create_scatter(
    data: np.ndarray, trace_name: str, mode: Literal["real", "objective"] = "real"
) -> go.Scatter:
    """
    Create a scatter plot trace for Plotly.

    Parameters
    ----------
    data : np.ndarray
        A 2D numpy array where:
        - Column 0: Power in kW
        - Column 1: Capacity in kWh
        - Column 2: Mass in kg
        - Column 3: Range in km (negative for minimization)
        - Column 4: Time in s
    trace_name : str
        The name of the trace to be displayed in the legend.
    mode : Literal["real", "objective"], optional
        If "real", plot Capacity vs Power. If "objective", plot Time vs Range.

    Returns
    -------
    go.Scatter
        A Plotly Scatter trace object.
    """
    marker_sizes = _calculate_marker_sizes(data[:, 2])

    if mode == "real":
        x = data[:, 0]  # Power
        y = data[:, 1]  # Capacity
        hovertemplate = (
            "Power: %{x:.2f} kW<br>"
            "Capacity: %{y:.2f} kWh<br>"
            "Mass: %{customdata[2]:.2f} kg<br>"
            "Range: %{customdata[3]:.2f} km<br>"
            "Time: %{customdata[4]:.2f} s<br><extra></extra>"
        )
    else:
        x = data[:, 3]  # Range
        y = data[:, 4]  # Time
        hovertemplate = (
            "Range: %{x:.2f} km<br>"
            "Time: %{y:.2f} s<br>"
            "Mass: %{customdata[2]:.2f} kg<br>"
            "Power: %{customdata[0]:.2f} kW<br>"
            "Capacity: %{customdata[1]:.2f} kWh<br><extra></extra>"
        )

    return go.Scatter(
        x=x,
        y=y,
        mode="markers",
        name=trace_name,
        marker={"size": marker_sizes},
        hovertemplate=hovertemplate,
        customdata=list(data),
    )


def plot_result(
    result: GenerationResult,
    fronts=False,
    fig=None,
    mode: Literal["real", "objective"] = "real",
) -> go.Figure:
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
    mode : Literal["real", "objective"], optional
        If "real", plot Capacity vs Power. If "objective", plot Time vs Range.

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
        if mode == "real":
            xaxis_title = "Motor Power [kW]"
            yaxis_title = "Battery Capacity [kWh]"
        else:
            xaxis_title = "Range [km]"
            yaxis_title = "Time [s]"
        fig.update_layout(
            title=f"Population {result.generation}{title_suffix}",
            xaxis_title=xaxis_title,
            yaxis_title=yaxis_title,
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
        fig.add_trace(_create_scatter(pop_array, "", mode=mode))
    else:
        pop_array = np.column_stack((pop_array, result.fronts))

        for front in set(result.fronts):
            front_idxs = np.where(pop_array[:, -1] == front)
            front_members = pop_array[front_idxs]

            fig.add_trace(
                _create_scatter(front_members, f"Front {int(front)}", mode=mode)
            )

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


def _from_dataframe_group(df_gen: pd.DataFrame) -> np.ndarray:
    """
    Create a pop_array from a DataFrame group corresponding to one generation.

    Expects columns: 'Motor Power (kW)', 'Battery Capacity (kWh)', 'Mass (kg)', 'Front', 'Range', 'Time'
    """
    df_gen = df_gen.copy()
    return df_gen[
        [
            "Motor Power (kW)",
            "Battery Capacity (kWh)",
            "Mass (kg)",
            "Range",
            "Time",
            "Front",
        ]
    ].to_numpy()


def create_ev_optimisation_static_frame(
    data: pd.DataFrame,
    generation: int,
    mode: Literal["real", "objective"] = "objective",
) -> go.Figure:
    """
    Creates a static Plotly figure for visualizing EV optimisation results for a specific generation.

    Parameters
    ----------
    data : pd.DataFrame
        DataFrame containing the population data, including objective values and front assignments.
    generation : int
        The generation number to display in the plot title.
    mode : {"real", "objective"}, optional
        Determines which axes to use for the plot:
        - "real": Plots real-world parameters (Motor Power vs Battery Capacity).
        - "objective": Plots objective values (Range vs Time).
        Default is "objective".

    Returns
    -------
    go.Figure
        A Plotly Figure object containing the scatter plot of the population, colored by Pareto front.

    Notes
    -----
    - The function expects the DataFrame to have a "Front" column indicating Pareto front membership.
    - Uses helper functions `_from_dataframe_group` and `_create_scatter` to process data and create traces.
    """
    pop_array = _from_dataframe_group(data)
    max_fronts = data["Front"].unique().shape[0]

    traces = []
    for front in range(1, max_fronts + 1):
        front_idxs = np.where(pop_array[:, -1] == front)
        name = f"Front {int(front)}"

        if front_idxs[0].size != 0:
            front_members = pop_array[front_idxs]
            trace = _create_scatter(front_members, name, mode=mode)
        else:
            trace = go.Scatter(name=name, x=[], y=[])

        traces.append(trace)

    xaxis_title = {
        "real": "Motor Power (kW)",
        "objective": "Range (km)",
    }[mode]
    yaxis_title = {
        "real": "Battery Capacity (kWh)",
        "objective": "Time (s)",
    }[mode]

    return go.Figure(
        data=traces,
        layout=go.Layout(
            xaxis={"autorange": True, "title": xaxis_title},
            yaxis={"autorange": True, "title": yaxis_title},
            title={"text": f"EV Optimisation - Generation {generation}"},
        ),
    )


def create_distribution_figure(
    df: pd.DataFrame, column: str, xaxis_label: str, generation: int
) -> go.Figure:
    """
    Create a distribution plot for a specified column in a DataFrame using Plotly.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame containing the data to plot.
    column : str
        The name of the column in the DataFrame to plot the distribution for.
    xaxis_label : str
        The label to display on the x-axis of the plot.
    generation : int
        The generation number to include in the plot title.

    Returns
    -------
    go.Figure
        A Plotly Figure object representing the distribution plot.
    """
    fig = ff.create_distplot(
        [df[column].to_numpy()],
        [column],
        bin_size=0.1,
        show_rug=False,
        show_hist=False,
    )

    fig.update_layout(
        title=f"{column} - Generation {generation}",
        showlegend=False,
        xaxis={"title": xaxis_label},
    )
    return fig
