from dash import Dash, callback, Input, Output, State
from dash import Dash, Input, Output, State


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

    return app
