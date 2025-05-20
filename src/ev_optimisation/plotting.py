from typing import Any, Literal
import matplotlib.pyplot as plt
import numpy as np
from ev_optimisation.vehicle import GenerationResult, Vehicle
import pandas as pd
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
        x = data[:, 0]
        y = data[:, 1]
        hovertemplate = (
            "Power: %{x:.2f} kW<br>"
            "Capacity: %{y:.2f} kWh<br>"
            "Mass: %{meta[0]:.2f} kg<br>"
            "Range: %{meta[1]:.2f} km<br>"
            "Time: %{meta[2]:.2f} s<br>"
        )
        meta = data[:, 2:5]
    # mode == "objective"
    else:
        x = data[:, 3]
        y = data[:, 4]
        hovertemplate = (
            "Range: %{x:.2f} km<br>"
            "Time: %{y:.2f} s<br>"
            "Power: %{meta[0]:.2f} kW<br>"
            "Capacity: %{meta[1]:.2f} kWh<br>"
            "Mass: %{meta[2]:.2f} kg<br>"
        )
        meta = data[:, [0, 1, 2]]

    return go.Scatter(
        x=x,
        y=y,
        mode="markers",
        marker={"size": marker_sizes},
        name=trace_name,
        hovertemplate=hovertemplate,
        meta=meta,
        showlegend=True,
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


def _from_generation_result(r: GenerationResult) -> np.ndarray:
    """
    Create a pop_array from a GenerationResult.

    Returns a numpy array of shape (n_individuals, 6):
    [motor_power, battery_capacity, mass, range, time, front]
    """
    pop_array = np.array(
        [
            (
                v.motor_power,
                v.battery_capacity,
                v.mass(),
                -r.objectives[i, 0],  # Range (negated)
                r.objectives[i, 1],  # Time
                r.fronts[i],  # Front
            )
            for i, v in enumerate(r.population)
        ]
    )
    return pop_array


def _from_dataframe_group(df_gen: pd.DataFrame) -> np.ndarray:
    """
    Create a pop_array from a DataFrame group corresponding to one generation.

    Expects columns: 'Motor Power (kW)', 'Battery Capacity (kWh)', 'Mass (kg)', 'Front', 'Range', 'Time'
    """
    df_gen = df_gen.copy()
    df_gen["Range"] = -df_gen["Range"]
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


def extract_generation_populations(
    result: dict[int, GenerationResult] | pd.DataFrame,
) -> list[tuple[int, np.ndarray]]:
    """
    Extract generation-wise population arrays from input data.

    Parameters
    ----------
    result : dict[int, GenerationResult] | pd.DataFrame

    Returns
    -------
    List of (generation, pop_array) tuples, where pop_array includes:
    [motor_power, battery_capacity, mass, range, time, front]
    """
    generations_data = []

    if isinstance(result, dict):
        for gen, r in result.items():
            pop_array = _from_generation_result(r)
            generations_data.append((gen, pop_array))

    elif isinstance(result, pd.DataFrame):
        grouped = result.groupby("Generation")
        for gen, df_gen in grouped:
            pop_array = _from_dataframe_group(df_gen)
            generations_data.append((gen, pop_array))

    else:
        raise TypeError("Input must be a dict[int, GenerationResult] or a pd.DataFrame")

    return generations_data


def _create_frame(pop_array, generation, max_fronts, mode):
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

    return go.Frame(
        data=traces,
        layout=go.Layout(title_text=f"EV Optimisation - Generation: {generation}"),
    )


def create_ev_optimisation_animation(
    result: dict[int, GenerationResult] | pd.DataFrame,
    mode: Literal["real", "objective"] = "real",
):
    """
    Create an animated scatter plot for EV optimisation results across generations.

    This function visualises the algorithm over generations, using either raw
    `GenerationResult` objects or a pd.DataFrame reconstructed from stored JSON.
    Each generation's population is plotted with Pareto fronts highlighted.

    Parameters
    ----------
    result : dict[int, GenerationResult] or pd.DataFrame
        The optimisation results. Can be either:
        - A dictionary mapping generation number to GenerationResult objects.
        - A pandas DataFrame containing columns:
          ['Motor Power (kW)', 'Battery Capacity (kWh)', 'Mass (kg)', 'Front', 'Range', 'Time'].

    mode : Literal["real", "objective"], default="real"
        Defines the axis labels and plot dimensions:
        - "real": plots Battery Capacity (kWh) vs Motor Power (kW)
        - "objective": plots Time (s) vs Range (km)

    Returns
    -------
    go.Figure
        A Plotly Figure object containing the animated plot, with one frame per generation.
    """
    generations_data = extract_generation_populations(result)
    max_fronts = max(int(np.max(pop_array[:, -1])) for _, pop_array in generations_data)

    frames = []
    for generation, pop_array in generations_data:
        frame = _create_frame(pop_array, generation, max_fronts, mode)
        frames.append(frame)

    fig = go.Figure(
        data=frames[0].data,
        frames=frames,
        layout=go.Layout(
            xaxis={"autorange": True, "title": "Motor Power (kW)"},
            yaxis={"autorange": True, "title": "Battery Capacity (kWh)"},
            title={"text": "EV Optimisation - Generation 0"},
            updatemenus=[
                {
                    "type": "buttons",
                    "buttons": [
                        {"label": "Play", "method": "animate", "args": [None]},
                        {
                            "label": "Pause",
                            "method": "animate",
                            "args": [
                                [None],
                                {
                                    "mode": "immediate",
                                    "frame": {"duration": 0},
                                    "transition": {"duration": 0},
                                },
                            ],
                        },
                    ],
                }
            ],
        ),
    )
    return fig
