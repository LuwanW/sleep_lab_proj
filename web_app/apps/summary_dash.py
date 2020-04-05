import os
from datetime import datetime
import dash
import dash_table
import plotly
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
from dash import Dash, callback_context, no_update
import sqlite3
import traceback
import pandas as pd
import copy
import dash_bootstrap_components as dbc
from web_app.app import app
import statistics


#app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app_colors = {
    'background': '#FFFFFF',
    'text': '#00008b',
    'sentiment-plot':'#41EAD4',
    'volume-bar':'#FBFC74',
    'someothercolor':'#FF206E',
}
# Colours
color_1 = "#003399"
color_2 = "#00ffff"
color_3 = "#002277"
color_b = "#F8F8FF"

mapbox_access_token = 'pk.eyJ1IjoiamFja2x1byIsImEiOiJjajNlcnh3MzEwMHZtMzNueGw3NWw5ZXF5In0.fk8k06T96Ml9CLGgKmk81w'

layout = dict(
    autosize=True,
    automargin=True,
    margin=dict(
        l=30,
        r=30,
        b=20,
        t=40
    ),
    hovermode="closest",
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    legend=dict(font=dict(size=10), orientation='h'),
    title='Sleep Position Summary',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="light",
        center=dict(
            lon=-78.05,
            lat=42.54
        ),
        zoom=7,
    )
)
path = r'D:\\4th_year\sleep_lab\sleep_lab\data_processor\report.csv'
df = pd.read_csv(r'D:\\4th_year\sleep_lab\sleep_lab\data_processor\report.csv')
global last
last = os.stat(path).st_mtime

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
                                                        html.H5("The Sleep Report"),

                                                    ],
                                                    className="page-1b",
                                                ),


                                            ],
                                            className="page-1c",
                                        ),

                                        dbc.Row([
                                            dbc.Col(width=3),
                                            dbc.Col(html.A(html.Button('view live data',style = {'color':color_b}),
                                                           href='http://127.0.0.1:8050/apps/history_dash')
                                                            ,width={"size":3},

                                                    ),


                                        ]),
dbc.Row([
                                            dbc.Col(width=3),

                                            dbc.Col(html.A(html.Button('Home page ',style = {'color':color_b}),
                                                           href='http://127.0.0.1:8050/'),width={"size":3,"order": "last"}
                                                    ),

                                        ]),

                                    ],
                                    className="page-1d",
                                ),


                            ],
                            className="page-1g",
                        ),




                        dbc.Row([
                            dbc.Col(width =1),
                            dbc.Col(
                            html.Div(
                            dash_table.DataTable(
                                id = 'table',

                                columns=[{"name": i, "id": i} for i in df.columns],
                                data=df.to_dict('records'),
                                style_cell={

                                    'font_size': '20px',
                                    'text_align': 'center'
                                },

                                style_data_conditional=[
                                    {
                                        "if": {"row_index": "odd"},
                                        "backgroundColor": color_b,
                                    },
                                    {
                                        "if": {"column_id": ""},
                                        "backgroundColor": color_2,
                                        "color": "white",
                                    },
                                ],
                                export_format="csv",
                                # fixed_rows={"headers": True},
                                # style_cell={"width": "70px"},
                            ),

                            )

                            ),
                            dbc.Col(
                                html.Div([
                                html.H6(
                                           "Sleep Hygiene Checklist",
                                                    className="page-1h",
                                                ),
                                dbc.Row(),
                                dbc.Checklist(
                                 options=[
                                     {"label": "Healthy diet", "value": 1},
                                     {"label": "Avoid Caffeine 4hrs before bed", "value": 2},
                                     {"label": "Avoid smoking 4hrs before bed", "value": 3},
                                     {"label": "Avoided Alcohol 4hrs before bed", "value": 8},
                                     {"label": "Relaxation exercise", "value": 4},
                                     {"label": "Followed bedtime routine", "value": 5},
                                     {"label": "Avoided naps", "value": 6},
                                     {"label": "Woke up at set time", "value": 7},
                                     {"label": "Used bed only for sleep", "value": 9},
                                     {"label": "Got out of bed if not asleep within 20-30 mins", "value": 10},
                                     {"label": "Natural light in the morning ", "value": 12},

                                 ],
                                    style={'font_size': '30px',},
                                 id="radioitems-input",


                             ),
                                ])
                             ),


                        ],
                        dbc.Row(
                            dbc.Button("Submit", color="success", className="mr-1")),

                        ),
                        dcc.Interval(id='interval', interval=1000, n_intervals=0),
###here
html.Div(
                            [
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.H6(
                                                    "REM sleep efficiency",
                                                    className="page-1h",
                                                ),
                                                dcc.Markdown('''

                                                   [-] REM sleep efficiency determines “how efficient am I sleeping”
                                                   [-] REM sleep efficiency = period of REM sleep / period of total sleep”
                                                   '''),

                                            ],
                                            className="page-5",
                                        ),
                                        html.Div(
                                            [
                                                html.H6(
                                                    "REM sleep latency",
                                                    className="page-1h",
                                                ),
                                                dcc.Markdown('''
                                                
                                                    [-] Rapid Eye Movement is a sleep stage. The REM sleep latency is a benchmark parameter for “how fast am I falling asleep”
                                                    
                                                    [-] REM is calculated from the moment turning the lights off, to the moment REM is detected. The light intensity is detected by the sensor plugged to the computer, and the REM is detected by the electrodes (“stickers”) on the forehead.
                                                    
                                                    [-] The typical REM sleep latency is 90-120 minutes for a healthy person
                                                    
                                                    [-] Error can come from two sources, light intensity sensor and the REM detection sensor. The problem may be caused by a high light intensity, a misplaced electrode or REM sensor out of battery. Please make sure the light is off and REM can be detected, this can be checked from the live website    
                                                    '''),

                                            ],
                                            className="page-5a",
                                        ),
                                        html.Div(
                                            [

                                        html.H6(
                                            "Heart rate variation",
                                            className="page-1h",
                                        ),
                                        dcc.Markdown('''
                                        
                                    [-] Benchmarking parameter for stress, lower HRV (comparing to normal value) higher the stress

                                    [-] Heart rate variation is calculated from result of heart rate, measured from the sensor on the fingertip. The sensor works by shining light, measure the light absorption and process to heart rate.

                                    [-] The typical heart rate for a healthy person is around 60-100 beat per minute, same as the unit used in the device.

                                    [-] Instability light source may cause error in heart rate variation measurement. This means if the sensor is not hold tight against finger, large movement, and low battery on the sensor, the data may include errors. No harms to human will be done in any of the cases, and data processing technique has been done to recover the error.
                                    '''),
                                            ],
                                            className="page-5b",
                                        ),
                                        html.Div(
                                            [

                                                html.H6(
                                                    "Intermittent awakening",
                                                    className="page-1h",
                                                ),
                                                dcc.Markdown('''
                                                
                                    [-] Intermittent awakening shows how many times you awake during the night
                                    '''),
                                            ],
                                            className="page-5b",
                                        ),
                                    ],
                                    className="page-5c",
                                ),


                            ],
                            className="eleven columns row",
                        ),
####here
                    ],

                )
            ],
            className="page",
        )]
)

@app.callback(Output('table', 'data'), [Input('interval', 'n_intervals')])
def trigger_by_modify(n):
    global last
    if os.stat(path).st_mtime > last:
        print("modified")
        last = os.stat(path).st_mtime
        return pd.read_csv(path).to_dict('records')
    return no_update

# app_layout = html.Div(
#
#      [
#          dbc.Row([
#              dbc.Col(html.A(html.Button('Check live data', className='three columns'),
#               href='http://127.0.0.1:8050/apps/history_dash')),
#          ]),
#          dbc.Row([
#              dbc.Col(html.Div(html.H2('Sleep Report'),
#                               style={'display': 'flex', 'justify-content': 'center'})),
#          ]),
#
#          dbc.Row([
#              dbc.Col(html.Div(dcc.Graph(id='heart_variation'), style={'margin-bottom': '20px', 'margin-top': '20px'}, )),
#              dbc.Col(
#
#             dbc.Row(
#                  html.Div(
#                      html.H4(id='ave_heart_rate_variation')
#                  ), style={'margin-bottom': '20px', 'margin-top': '20px'}
#                  ),width=4
#              ),
#          ]),
#          dbc.Row(
#              html.Div(
#                  html.H4(id='ave_heart_rate')
#              ), style={'margin-bottom': '20px', 'margin-top': '20px'}
#          ),
#
#          dbc.Row([
#              dbc.Col(html.Div(dcc.Graph(id="sleep_efficiency"), style={'margin-bottom': '20px', 'margin-top': '20px'}),
#                      width=8),
#              dbc.Col(
#                  html.Div(
#                      html.H4(id='sleep_efficiency_text')
#                  ), style={'margin-bottom': '20px', 'margin-top': '20px'}
#              ),
#          ]),
#
#          dbc.Row([
#              dbc.Col(
#                  html.Div(
#                      html.H4(id='sleep_latency')
#                  ), style={'margin-bottom': '20px', 'margin-top': '20px'}
#              ),
#          ]),
#
#          dbc.Row([
#              dbc.Col(
#                  html.Div(
#                      html.H4(id='time_in_bed')
#                  ), style={'margin-bottom': '20px', 'margin-top': '20px'}
#              ),
#          ]),
#
#          dbc.Row([
#              dbc.Col(
#                  html.Div(
#                      html.H4(id='flip_count')
#                  ), style={'margin-bottom': '20px', 'margin-top': '20px'}
#              ),
#          ]),
#          dbc.Row([
#              dbc.Col(html.Div(html.H2('Sleep Hygiene Checklist'),
#                               style={'display': 'flex', 'justify-content': 'center'})),
#          ]),
#          dbc.Checklist(
#              options=[
#                  {"label": "Healthy diet", "value": 1},
#                  {"label": "Avoid Caffeine 4hrs before bed", "value": 2},
#                  {"label": "Avoid smoking 4hrs before bed", "value": 3},
#                  {"label": "Avoided Alcohol 4hrs before bed", "value": 8},
#                  {"label": "Relaxation exercise", "value": 4},
#                  {"label": "Followed bedtime routine", "value": 5},
#                  {"label": "Avoided naps", "value": 6},
#                  {"label": "Woke up at set time", "value": 7},
#                  {"label": "Used bed only for sleep", "value": 9},
#                  {"label": "Got out of bed if not asleep within 20-30 mins", "value": 10},
#                  {"label": "Natural light in the morning ", "value": 12},
#
#              ],
#              id="radioitems-input",
#          ),
#          dbc.Row([
#              dbc.Button("Submit", color="success", className="mr-1")]
#          ),
#          dcc.Interval(
#              id='report_update',
#              interval=5 * 1000,  # in milliseconds
#              n_intervals=0,
#          ),
#      ],
#     id="mainContainer",
#     style={'backgroundColor': app_colors['background'], 'margin-top': '50px', 'height': '2000px',
#            'margin-bottom': '20px',
#             'margin-left': '30px',
#             'margin-right': '30px',
#             'display':'flex',
#             "flex-direction": "column",
#                },
# )
#
#
# @app.callback(Output('sleep_efficiency', 'figure'),
#               [Input('report_update', 'n_intervals')])
# def update_pie_chart(n):
#     try:
#         conn = sqlite3.connect(r'D:\\4th_year\sleep_lab\sleep_lab\data_processor\sleep_lab.db')
#
#         moving = pd.read_sql("SELECT count(*) FROM rem_info WHERE eye_movement = 'moving' ", conn)
#         steady = pd.read_sql("SELECT count(*) FROM rem_info WHERE eye_movement = 'steady'", conn)
#         values = [moving.at[0,'count(*)'], steady.at[0,'count(*)']]
#
#         labels = ['Deep sleep', 'regular sleep']
#         print('updating eye movement')
#
#         data = dict(
#             type='pie',
#             labels=labels,
#             values=values,
#             name='Production Breakdown',
#             hoverinfo="label+value+percent",
#             textinfo="label+percent+name",
#             hole=0.3,
#             marker=dict(
#                 colors=['#FFA500','#66CDAA','#708090','#FFB6C1']
#             ),
#             domain={"x": [0, 0.5], 'y': [0.1, 0.8]},
#
#         )
#
#         layout_pie = copy.deepcopy(layout)
#         layout_pie['title'] = 'Deep sleep summary'
#         layout_pie['font'] = dict(color='#777777')
#         layout_pie['legend'] = dict(
#             font=dict(color='#CCCCCC', size='10'),
#             orientation='h',
#             bgcolor='rgba(0,0,0,0)'
#         )
#         return {"data": [data], 'layout': layout_pie}
#
#     except Exception as e:
#         with open('errors.txt','a') as f:
#             f.write(str(e))
#             traceback.print_exc()
#             f.write('\n')
#
# @app.callback(Output('heart_variation', 'figure'),
#               [Input('report_update', 'n_intervals')])
# def update_graph_scatter(n):
#     try:
#         conn = sqlite3.connect(r'D:\\4th_year\sleep_lab\sleep_lab\data_processor\sleep_lab.db')
#
#         df = pd.read_sql("SELECT * FROM heart_info ORDER BY id DESC", conn)
#
#         bpm = df['bpm'].tolist()
#         time = pd.to_datetime(df['time_stamp'])
#         vari_bpm = [abs(j-i) for i,j in zip(bpm, bpm[1:])]
#         print(vari_bpm)
#         print(time)
#
#         data = plotly.graph_objs.Scatter(
#                 x=time,
#                 y=vari_bpm,
#                 name='Scatter',
#                 mode= 'lines+markers'
#                 )
#         app.logger.info('updating heart_info')
#
#         layout_aggregate = copy.deepcopy(layout)
#         layout_aggregate['xaxis']=dict(range=[min(time),max(time)])
#         layout_aggregate['yaxis']=dict(range=[min(vari_bpm),150])
#         layout_aggregate['title']='Heart Rate Variation'
#
#         return dict(data=[data], layout=layout_aggregate)
#
#     except Exception as e:
#         with open('errors.txt','a') as f:
#             f.write(str(e))
#             traceback.print_exc()
#             f.write('\n')
#
#
# @app.callback(Output('ave_heart_rate_variation', "children"),
#               [Input('report_update', 'n_intervals')])
# def update_sleep_pos(n):
#
#     conn = sqlite3.connect(r'D:\\4th_year\sleep_lab\sleep_lab\data_processor\sleep_lab.db')
#     df = pd.read_sql("SELECT * FROM heart_info ORDER BY id DESC", conn)
#
#     bpm = df['bpm'].tolist()
#     vari_bpm = [abs(j - i) for i, j in zip(bpm, bpm[1:])]
#     vari_bpm_ave = statistics.mean(vari_bpm)
#     return 'Average heart rate variation: {0:.2f}'.format(vari_bpm_ave)
#
#
# @app.callback(Output('ave_heart_rate', "children"),
#               [Input('report_update', 'n_intervals')])
# def update_sleep_pos(n):
#
#     conn = sqlite3.connect(r'D:\\4th_year\sleep_lab\sleep_lab\data_processor\sleep_lab.db')
#     df = pd.read_sql("SELECT avg(bpm) FROM heart_info ORDER BY id", conn)
#     HR = df['avg(bpm)'][0]
#     return 'Average heart rate: {0:.2f}'.format(HR)
#
#
# @app.callback(Output('sleep_latency', "children"),
#               [Input('report_update', 'n_intervals')])
# def update_sleep_pos(n):
#     # you can not distinguish rem and actual eye movement
#     # here use first rem - first light off
#     conn = sqlite3.connect(r'D:\\4th_year\sleep_lab\sleep_lab\data_processor\sleep_lab_serial.db')
#     df_first_light_off = pd.read_sql("SELECT * FROM env_info WHERE r < 10 LIMIT 1", conn)
#     time_first = df_first_light_off['time_stamp'][0]
#     time_first_time = datetime.strptime(time_first, "%m-%d-%Y %H:%M:%S")
#
#     conn_rem = sqlite3.connect(r'D:\\4th_year\sleep_lab\sleep_lab\data_processor\sleep_lab.db')
#     df_first_rem = pd.read_sql("SELECT * FROM rem_info WHERE eye_movement = 'moving' LIMIT 1", conn_rem)
#     time_last = df_first_rem['time_stamp'][0]
#     time_first_time = datetime.strptime(time_first, "%m-%d-%Y %H:%M:%S")
#
#     time_last_time = datetime.strptime(time_last, "%m-%d-%Y %H:%M:%S")
#     time_diff = time_last_time - time_first_time
#
#     return 'REM sleep latency: ' + str(time_diff)
#
#
# @app.callback(Output('time_in_bed', "children"),
#               [Input('report_update', 'n_intervals')])
# def update_sleep_pos(n):
#
#     conn = sqlite3.connect(r'D:\\4th_year\sleep_lab\sleep_lab\data_processor\sleep_lab_serial.db')
#     df_first = pd.read_sql("SELECT * FROM env_info WHERE r < 10 LIMIT 1", conn)
#     df_last = pd.read_sql("SELECT * FROM env_info ORDER BY id DESC LIMIT 1", conn)
#
#     time_first = df_first['time_stamp'][0]
#     time_last = df_last['time_stamp'][0]
#     time_first_time = datetime.strptime(time_first, "%m-%d-%Y %H:%M:%S")
#     time_last_time = datetime.strptime(time_last, "%m-%d-%Y %H:%M:%S")
#     time_diff = time_last_time - time_first_time
#     return 'Time in bed after light off: ' + str(time_diff)
#
#
#
# @app.callback(Output('flip_count', "children"),
#               [Input('report_update', 'n_intervals')])
# def update_sleep_pos(n):
#
#     conn = sqlite3.connect(r'D:\\4th_year\sleep_lab\sleep_lab\data_processor\sleep_lab.db')
#     df = pd.read_sql("SELECT * FROM position_info ORDER BY id", conn)
#     positions = df['position'].tolist()
#     counter = 0
#     for index,pos in enumerate(positions):
#         if index == len(positions)-1:
#             break
#         if positions[index] != positions[index+1]:
#             counter += 1
#     return 'Number of flips: ' + str(counter)
#


if __name__ == '__main__':
    app.run_server(debug=True)
