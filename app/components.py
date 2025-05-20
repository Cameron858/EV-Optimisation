from dash import html
import dash_bootstrap_components as dbc

plot_mode_select = html.Div(
    [
        dbc.Label("Plot mode", html_for="mode-select"),
        dbc.Select(
            options=[
                {
                    "label": "Real",
                    "value": "real",
                },
                {
                    "label": "Objectives",
                    "value": "objective",
                },
            ],
            id="mode-select",
            value="real",
        ),
    ]
)
