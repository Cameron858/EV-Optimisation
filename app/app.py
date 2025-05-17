from dash import Dash, html
import dash_bootstrap_components as dbc
import logging

app = Dash(
    __name__,
    title="EV Optimiser",
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
)

app.layout = html.Div([html.H1("Hello world!")])
