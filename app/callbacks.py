import logging
import random
from io import StringIO

import numpy as np
import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objects as go
from dash import Dash, Input, Output, State, callback, html

from app.components import placeholder_figure
from ev_optimisation.adapters import result_to_json
from ev_optimisation.adapters.dash_adapters import load_and_filter_generation
from ev_optimisation.algorithm import optimise_ev_population
from ev_optimisation.plotting import create_ev_optimisation_static_frame
from ev_optimisation.vehicle import VehicleConfig
import plotly.graph_objects as go
import plotly.figure_factory as ff
import pandas as pd
import random
import numpy as np
import logging

logger = logging.getLogger("main")


def register_callbacks(app: Dash) -> Dash:
    """Attatch callbacks to a dash app."""

    @app.callback(
        Output("run-btn", "disabled"),
        Input("n-pop-input", "value"),
        Input("n-gens-input", "value"),
    )
    def toggle_button_disabled(pop_size, n_gens):
        # Validate Population size: must be int, within [2, 50]
        if not isinstance(pop_size, (int, float)) or pop_size is None:
            return True
        if pop_size < 2 or pop_size > 50:
            return True

        # Validate Generations: must be int, within [1, 50]
        if not isinstance(n_gens, (int, float)) or n_gens is None:
            return True
        if n_gens < 1 or n_gens > 50:
            return True

        return False  # Enable button if all validations pass

    @app.callback(
        Output("gen-slider-input", "max"),
        Input("result-store", "data"),
    )
    def update_slider_max(data):
        if data:
            df_reconstructed = pd.read_json(StringIO(data), orient="split")
            return df_reconstructed["Generation"].max()
        return 0

    @app.callback(
        Output("gen-slider-input", "disabled"),
        Input("result-store", "data"),
    )
    def disable_slider_if_no_data(data):
        if not data:
            return True
        try:
            df = pd.read_json(StringIO(data), orient="split")
            return df.empty or "Generation" not in df.columns
        except Exception:
            return True

    @app.callback(
        Output("mode-toggle", "options"),
        Input("result-store", "data"),
    )
    def disable_mode_input_if_no_data(data):
        disabled = False if data else True
        options = [
            {"label": "Real", "value": "real", "disabled": disabled},
            {"label": "Objective", "value": "objective", "disabled": disabled},
        ]
        return options

    @callback(
        Output("result-store", "data"),
        Input("run-btn", "n_clicks"),
        State("n-pop-input", "value"),
        State("n-gens-input", "value"),
        State("mutation-input", "value"),
        State("crossover-input", "value"),
        State("seed-input", "value"),
        prevent_initial_call=True,
    )
    def run_algorithm(
        n_clicks, n_pop, n_gens, mutation_rate, crossover_rate, seed
    ) -> dict:
        logger.debug("Running algorithm")

        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)

        config = VehicleConfig()
        result = optimise_ev_population(
            config,
            n_gens,
            n_pop,
            crossover_rate=crossover_rate,
            mutate_rate=mutation_rate,
        )
        json_result = result_to_json(result)
        return json_result

    @callback(
        Output("main-output-graph", "figure"),
        Input("result-store", "data"),
        Input("gen-slider-input", "value"),
        Input("mode-toggle", "value"),
        prevent_initial_call=True,
    )
    def update_result_graph_from_store(data, generation, plot_mode) -> go.Figure:
        if data is None:
            return placeholder_figure()

        df_filtered = load_and_filter_generation(data, generation)
        fig = create_ev_optimisation_static_frame(df_filtered, generation, plot_mode)
        return fig

    @callback(
        Output("pop-stats-graph-1", "figure"),
        Input("result-store", "data"),
        Input("gen-slider-input", "value"),
        Input("mode-toggle", "value"),
        prevent_initial_call=True,
    )
    def update_pop_stats_graph_1(data, generation, plot_mode) -> go.Figure:
        if data is None:
            return placeholder_figure()

        df_filtered = load_and_filter_generation(data, generation)

        # set up vars based on plotting mode
        if plot_mode == "real":
            column = "Motor Power (kW)"
            xaxis_label = column
        else:
            column = "Range"
            xaxis_label = "Range (km)"

        fig = ff.create_distplot(
            [
                df_filtered[column].to_numpy(),
            ],
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

    @callback(
        Output("pop-stats-graph-2", "figure"),
        Input("result-store", "data"),
        Input("gen-slider-input", "value"),
        Input("mode-toggle", "value"),
        prevent_initial_call=True,
    )
    def update_pop_stats_graph_2(data, generation, plot_mode) -> go.Figure:
        if data is None:
            return placeholder_figure()

        df_filtered = load_and_filter_generation(data, generation)

        # set up vars based on plotting mode
        if plot_mode == "real":
            column = "Battery Capacity (kWh)"
            xaxis_label = column
        else:
            column = "Time"
            xaxis_label = "Time (s)"

        fig = ff.create_distplot(
            [
                df_filtered[column].to_numpy(),
            ],
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

    @app.callback(
        Output("offcanvas", "is_open"),
        Input("main-output-graph", "clickData"),
        prevent_initial_call=True,
    )
    def open_offcanvas(click_data):
        return True

    @app.callback(
        Output("main-output-graph", "clickData"),
        Output("offcanvas", "children"),
        Input("main-output-graph", "clickData"),
        State("result-store", "data"),
        State("gen-slider-input", "value"),
        prevent_initial_call=True,
    )
    def update_offcanvas_contents(click_data, data, generation):
        # power, capacity, mass, range, time
        custom_data = click_data["points"][0]["customdata"]
        meta_data_dict = {
            k: v
            for k, v in zip(["power", "capacity", "mass", "range", "time"], custom_data)
        }
        meta_data_dict["front"] = click_data["points"][0]["curveNumber"] + 1
        meta_data_dict["generation"] = generation

        return {}, html.Div(
            [
                html.Ul(
                    [
                        html.Li(f"Generation: {meta_data_dict['generation']}"),
                        html.Li(f"Front: {meta_data_dict['front']}"),
                        html.Li(f"Power: {meta_data_dict['power']} kW"),
                        html.Li(f"Capacity: {meta_data_dict['capacity']} kWh"),
                        html.Li(f"Mass: {meta_data_dict['mass']} kg"),
                        html.Li(f"Range: {meta_data_dict['range']} km"),
                        html.Li(f"Time: {meta_data_dict['time']} s"),
                    ]
                ),
            ]
        )

    @app.callback(
        Output("result-store", "data", allow_duplicate=True),
        Input("clear-store-btn", "n_clicks"),
        prevent_initial_call=True,
    )
    def clear_data_store(n_clicks):
        logger.debug(f"Clearing data store {n_clicks}")
        if n_clicks:
            return ""

    return app
