from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

from app.callbacks import register_callbacks

app = Dash(
    __name__,
    title="EV Optimiser",
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
)

app.layout = html.Div(
    [
        dcc.Store(id="result-store"),
        dbc.NavbarSimple(brand="EV Optimiser", color="lightseagreen"),
        dbc.Row(
            [
                # left - inputs
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.H3(
                                            "Parameters",
                                            className="card-title",
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Label(
                                                    "Population size",
                                                    html_for="n-pop-input",
                                                ),
                                                dbc.Input(
                                                    type="number",
                                                    id="n-pop-input",
                                                    placeholder="Population size",
                                                    value=10,
                                                    min=2,
                                                    max=50,
                                                    step=2,
                                                    class_name="validate-input",
                                                ),
                                            ],
                                            class_name="input-group",
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Label(
                                                    "Generations",
                                                    html_for="n-gens-input",
                                                ),
                                                dbc.Input(
                                                    type="number",
                                                    id="n-gens-input",
                                                    placeholder="Number of generations",
                                                    value=10,
                                                    min=1,
                                                    max=50,
                                                    class_name="validate-input",
                                                ),
                                            ],
                                            class_name="input-group",
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Label(
                                                    "Mutation rate",
                                                    html_for="mutation-input",
                                                ),
                                                dbc.Input(
                                                    type="number",
                                                    id="mutation-input",
                                                    placeholder="Mutation rate",
                                                    value=0.05,
                                                    min=0,
                                                    max=1,
                                                    step=0.01,
                                                    class_name="validate-input",
                                                ),
                                            ],
                                            class_name="input-group",
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Label(
                                                    "Crossover rate",
                                                    html_for="crossover-input",
                                                ),
                                                dbc.Input(
                                                    type="number",
                                                    id="crossover-input",
                                                    placeholder="Crossover rate",
                                                    value=0.8,
                                                    min=0,
                                                    max=1,
                                                    step=0.01,
                                                    class_name="validate-input",
                                                ),
                                            ],
                                            class_name="input-group",
                                        ),
                                    ]
                                )
                            ],
                            class_name="m-3",
                        ),
                        dbc.Button(
                            "Run Optimiser",
                            id="run-btn",
                            class_name="m-1 btn-lightseagreen",
                        ),
                    ],
                    # takes up 1/3
                    width=4,
                ),
                # right - outputs
                dbc.Col([dcc.Graph(id="main-output-graph")]),
            ]
        ),
    ]
)


app = register_callbacks(app)
