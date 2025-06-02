from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

from app.callbacks import register_callbacks
from app.components import parameter_input, placeholder_figure

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
                        # button "toolbar"
                        dbc.Row(
                            [
                                dbc.Button(
                                    "Run Optimiser",
                                    id="run-btn",
                                    class_name="m-1 btn-lightseagreen",
                                    style={"max-width": "200px"},
                                ),
                            ],
                            class_name="m-3",
                        ),
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.H3(
                                            "Parameters",
                                            className="card-title",
                                        ),
                                        dbc.Accordion(
                                            [
                                                dbc.AccordionItem(
                                                    [
                                                        parameter_input(
                                                            "Population size",
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
                                                        ),
                                                        parameter_input(
                                                            "Generations",
                                                            dbc.Input(
                                                                type="number",
                                                                id="n-gens-input",
                                                                placeholder="Number of generations",
                                                                value=10,
                                                                min=1,
                                                                max=50,
                                                                class_name="validate-input",
                                                            ),
                                                        ),
                                                        parameter_input(
                                                            "Mutation rate",
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
                                                        ),
                                                        parameter_input(
                                                            "Crossover rate",
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
                                                        ),
                                                        parameter_input(
                                                            "Random seed",
                                                            dbc.Input(
                                                                type="number",
                                                                id="seed-input",
                                                                placeholder="Random seed",
                                                                # What other value would I use?
                                                                value=42,
                                                                min=0,
                                                                step=1,
                                                                class_name="validate-input",
                                                            ),
                                                        ),
                                                    ],
                                                    title="Algorithm",
                                                ),
                                                dbc.AccordionItem(
                                                    [
                                                        parameter_input(
                                                            "Tire pressure [bar]",
                                                            dbc.Input(
                                                                type="number",
                                                                id="p-tire-bar-input",
                                                                placeholder="Tire pressure [bar]",
                                                                value=2.5,
                                                                min=1.0,
                                                                max=5.0,
                                                                step=0.1,
                                                                class_name="validate-input",
                                                            ),
                                                        ),
                                                        parameter_input(
                                                            "Motor max RPM",
                                                            dbc.Input(
                                                                type="number",
                                                                id="motor-rpm-input",
                                                                placeholder="Motor max RPM",
                                                                value=6000,
                                                                min=1000,
                                                                max=20000,
                                                                step=100,
                                                                class_name="validate-input",
                                                            ),
                                                        ),
                                                        parameter_input(
                                                            "Tire radius [m]",
                                                            dbc.Input(
                                                                type="number",
                                                                id="r-tire-m-input",
                                                                placeholder="Tire radius [m]",
                                                                value=0.65,
                                                                min=0.2,
                                                                max=1.0,
                                                                step=0.01,
                                                                class_name="validate-input",
                                                            ),
                                                        ),
                                                        parameter_input(
                                                            "Frontal area [m²]",
                                                            dbc.Input(
                                                                type="number",
                                                                id="A-m2-input",
                                                                placeholder="Frontal area [m²]",
                                                                value=2.2,
                                                                min=1.0,
                                                                max=4.0,
                                                                step=0.01,
                                                                class_name="validate-input",
                                                            ),
                                                        ),
                                                        parameter_input(
                                                            "Drag coefficient",
                                                            dbc.Input(
                                                                type="number",
                                                                id="c-d-input",
                                                                placeholder="Drag coefficient",
                                                                value=0.25,
                                                                min=0.1,
                                                                max=0.5,
                                                                step=0.01,
                                                                class_name="validate-input",
                                                            ),
                                                        ),
                                                        parameter_input(
                                                            "Gear ratio",
                                                            dbc.Input(
                                                                type="number",
                                                                id="gear-ratio-input",
                                                                placeholder="Gear ratio",
                                                                value=10,
                                                                min=1,
                                                                max=20,
                                                                step=0.1,
                                                                class_name="validate-input",
                                                            ),
                                                        ),
                                                        parameter_input(
                                                            "Cruising speed [km/h]",
                                                            dbc.Input(
                                                                type="number",
                                                                id="v-cruising-kmh-input",
                                                                placeholder="Cruising speed [km/h]",
                                                                value=100,
                                                                min=10,
                                                                max=300,
                                                                step=1,
                                                                class_name="validate-input",
                                                            ),
                                                        ),
                                                        parameter_input(
                                                            "Drivetrain efficiency [0-1]",
                                                            dbc.Input(
                                                                type="number",
                                                                id="drivetrain-eff-input",
                                                                placeholder="Drivetrain efficiency [0-1]",
                                                                value=1.0,
                                                                min=0.5,
                                                                max=1.0,
                                                                step=0.01,
                                                                class_name="validate-input",
                                                            ),
                                                        ),
                                                    ],
                                                    title="Vehicle",
                                                ),
                                            ],
                                            always_open=True,
                                        ),
                                    ]
                                )
                            ],
                            class_name="m-3",
                        ),
                    ],
                    # takes up 1/3
                    width=4,
                ),
                # right - outputs
                dbc.Col(
                    [
                        dcc.Graph(id="main-output-graph", figure=placeholder_figure()),
                        html.Div(
                            [
                                dbc.RadioItems(
                                    # default to disabled
                                    options=[
                                        {
                                            "label": "Real",
                                            "value": "real",
                                            "disabled": True,
                                        },
                                        {
                                            "label": "Objective",
                                            "value": "objective",
                                            "disabled": True,
                                        },
                                    ],
                                    value="objective",
                                    id="mode-toggle",
                                    inline=True,
                                    style={"margin-right": "20px"},
                                ),
                                html.Div(
                                    dcc.Slider(
                                        id="gen-slider-input",
                                        min=0,
                                        max=10,
                                        step=1,
                                        value=0,
                                        # default to disabled
                                        disabled=True,
                                    ),
                                    style={"flex": "1"},
                                ),
                            ],
                            style={
                                "display": "flex",
                                "align-items": "center",
                                "gap": "20px",
                            },
                        ),
                        # pop stats graphs
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dcc.Graph(
                                            id="pop-stats-graph-1",
                                            figure=placeholder_figure(font_size=20),
                                        ),
                                    ],
                                    width=6,
                                ),
                                dbc.Col(
                                    [
                                        dcc.Graph(
                                            id="pop-stats-graph-2",
                                            figure=placeholder_figure(font_size=20),
                                        ),
                                    ],
                                    width=6,
                                ),
                            ],
                            class_name="justify-content-between",
                        ),
                    ],
                    width=8,
                ),
            ]
        ),
    ]
)


app = register_callbacks(app)
