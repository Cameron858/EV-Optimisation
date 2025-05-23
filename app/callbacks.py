from io import StringIO
from dash import Dash, callback, Input, Output, State
from ev_optimisation.adapters import result_to_json
from ev_optimisation.algorithm import optimise_ev_population
from ev_optimisation.plotting import create_ev_optimisation_animation
from ev_optimisation.vehicle import VehicleConfig
import plotly.graph_objects as go
import pandas as pd


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

    @callback(
        Output("result-store", "data"),
        Input("run-btn", "n_clicks"),
        State("n-pop-input", "value"),
        State("n-gens-input", "value"),
        prevent_initial_call=True,
    )
    def run_algorithm(n_clicks, n_pop, n_gens) -> dict:
        config = VehicleConfig()
        result = optimise_ev_population(config, n_gens, n_pop)
        json_result = result_to_json(result)
        return json_result

    @callback(
        Output("main-output-graph", "figure"),
        Input("result-store", "data"),
        prevent_initial_call=True,
    )
    def update_figures_from_store(data) -> go.Figure:
        df_reconstructed = pd.read_json(StringIO(data), orient="split")
        fig = create_ev_optimisation_animation(df_reconstructed)
        return fig

    return app
