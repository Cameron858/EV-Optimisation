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


def parameter_input(title: str, input_component: dbc.Input):
    try:
        input_id = getattr(input_component, "id")
    except AttributeError:
        input_id = None
    return dbc.Row(
        [
            dbc.Label(
                title,
                html_for=input_id,
            ),
            input_component,
        ],
        class_name="input-group",
    )
