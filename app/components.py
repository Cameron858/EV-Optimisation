from dash import html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

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


def placeholder_figure() -> go.Figure:
    """
    Creates a placeholder Plotly figure with no data and a 'No results found. Run model to display data.' annotation.

    Returns
    -------
    go.Figure
        A Plotly Figure object with hidden axes, grey background, and a centered 'No results found. Run model to display data.' message.
    """
    fig = go.Figure(
        layout={
            "xaxis": {
                "showticklabels": False,
                "showgrid": False,
                "zeroline": False,
            },
            "yaxis": {
                "showticklabels": False,
                "showgrid": False,
                "zeroline": False,
            },
            "plot_bgcolor": "#888888",
            "annotations": [
                {
                    "text": "No results found. Run model to display data.",  # Customize as needed
                    "x": 0.5,
                    "y": 0.5,
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                    "font": {"size": 32, "color": "white"},
                    "align": "center",
                }
            ],
        }
    )
    return fig
