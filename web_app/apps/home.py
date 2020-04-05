import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from web_app.app import app
import dash_bootstrap_components as dbc

# Colours
color_1 = "#003399"
color_2 = "#00ffff"
color_3 = "#002277"
color_b = "#F8F8FF"

app_layout = html.Div(


    children=[
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.Div(
                                                    html.Img(

                                                        className="page-1a",
                                                    )
                                                ),
                                                html.Div(
                                                    [
                                                        html.H6("4th year project"),
                                                        html.H5("The Portable Sleep Lab"),
                                                        html.H6("Department of computer system"),
                                                    ],
                                                    className="page-1b",
                                                ),
                                            ],
                                            className="page-1c",
                                        )
                                    ],
                                    className="page-1d",
                                ),
                                html.Div(
                                    [
                                        html.H1(
                                            [
                                                html.Span("group", className="page-1e"),
                                                html.Span("57"),
                                            ]
                                        ),
                                        html.H6("Supervisor Andy Adler"),
                                    ],
                                    className="page-1f",
                                ),
                            ],
                            className="page-1g",
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H6("Bill Hou", className="page-1h"),
                                        html.P("xxxxxxxxxx"),
                                    ],
                                    className="page-1i",
                                ),
                                html.Div(
                                    [
                                        html.H6("Luwan Wang", className="page-1h"),
                                        html.P("xxxxxxxxxx"),
                                    ],
                                    className="page-1i",
                                ),
                                html.Div(
                                    [
                                        html.H6(
                                            "Kan Wang", className="page-1h"
                                        ),
                                        html.P("xxxxxxxxxx"),
                                    ],
                                    className="page-1i",
                                ),
                                html.Div(
                                    [
                                        html.H6("Ziqiang Wang", className="page-1h"),
                                        html.P("xxxxxxxxxx"),
                                    ],
                                    className="page-1i",
                                ),
                            ],
                            className="page-1j",
                        ),

                        dbc.Row([
                            dbc.Col(html.A(html.Button('view live data'),
                                           href='http://127.0.0.1:8050/apps/history_dash')),
                            dbc.Col(html.A(html.Button('view report '),
                                           href='http://127.0.0.1:8050/apps/summary_dash')),
                        ]),

                        html.Div(
                            [
                                html.Div(
                                    [

                                        html.H6(
                                            "Do you have a sleep problem? ",
                                            className="page-1h",
                                        ),
                                        html.Img(
                                            src=app.get_asset_url("canadian_sleep_problem.jpg"),
                                            style={'height':'90%', 'width':'90%'}
                                        ),
                                    ],
                                    className="page-1k",
                                ),
                                html.Div(
                                    [
                                        html.H6(
                                            "Sleep problem can cause",
                                            className="page-1h",
                                        ),
                                        html.Img(
                                            src=app.get_asset_url("sleep_problem.PNG"),
                                            style={'height':'90%', 'width':'90%'}
                                        ),

                                    ],
                                    className="page-1k",
                                ),
                                html.Div(
                                    [
                                        html.H6(
                                            "However, most people will not go to professionals because",
                                            className="page-1h",
                                        ),
                                        dcc.Markdown('''
                                    [-] An individual aware the potential sleep problems/problem associated with people in the family

                                    [-] The problem is not serious enough to invest a large amount of time and money into it

                                    [-] The problem itself is not clear, in term of cause and effects
                                    [-] There’s no measure (feedback) of whether the improvements are effective in solving the problem

                                    '''),
                                    ],
                                    className="page-1l",
                                ),
                                html.Div(
                                    [
                                        html.H6(
                                            "The portable sleep lab can solve your problem!",
                                            className="page-1h",
                                        ),
                                        dcc.Markdown('''
                                    [-] Act as a family fitness device, aim at optimizing sleep quality for individuals

                                    [-] The device should not be discomfort and not costly in time and money

                                    [-] The device should help clarify the problem

                                    [-] The device should provide solution in term of correlations

                                    '''),

                                    ],
                                    className="page-1m",
                                ),

                            ],
                            className="page-1n",
                        ),
                    ],
                    className="subpage",
                )
            ],
            className="page",
        )]
)
