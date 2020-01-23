import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
from collections import deque
import sqlite3
import traceback
import pandas as pd
import copy
import dash_bootstrap_components as dbc


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app_colors = {
    'background': '#FFFFFF',
    'text': '#00008b',
    'sentiment-plot':'#41EAD4',
    'volume-bar':'#FBFC74',
    'someothercolor':'#FF206E',
}

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

app.layout = html.Div(

     [

         dbc.Row([
             dbc.Col(html.Div(html.H2('Sleep lab dashboard '),
                              style={'display': 'flex', 'justify-content': 'center'})),
         ]),
         dbc.Row([
             dbc.Col(html.Div(html.H4('Human Factors '),
                              style={'display': 'flex', 'justify-content': 'center'})),
         ]),
         dbc.Row([
            dbc.Col(html.Div(dcc.Graph(id='live-graph'),style={'margin-bottom': '20px', 'margin-top': '20px'},),width=8),
            dbc.Col(
             html.Div(
                 html.H4(id='heart_rate')
             ),style={'margin-bottom': '20px', 'margin-top': '20px'}
            ),
             ]),

         dbc.Row([
             dbc.Col(html.Div(dcc.Graph(id="sentiment-pie"),style={'margin-bottom': '20px', 'margin-top': '20px' }),width=8),
             dbc.Col(html.Div(
                 html.Img(id="sleep-pos")
             )),

         ]),

         dbc.Row([
             dbc.Col(html.Div(dcc.Graph(id="REM-pie"), style={'margin-bottom': '20px', 'margin-top': '20px'}),
                     width=8),
             dbc.Col(
                 html.Div(
                     html.H4(id='REM-text')
                 ), style={'margin-bottom': '20px', 'margin-top': '20px'}
             ),

         ]),
         dbc.Row([
             dbc.Col(html.Div(html.H4('Environment factors'),
                              style={'display': 'flex', 'justify-content': 'center'})),
         ]
         ),
         dbc.Row([
            dbc.Col(html.Div(dcc.Graph(id='room-temp-trend'),style={'margin-bottom': '20px', 'margin-top': '20px'},),width=8),
            dbc.Col(
             html.Div(
                 html.H4(id='room-temp')
             ),style={'margin-bottom': '20px', 'margin-top': '20px' }
            ),
             ]),

         dbc.Row([
             dbc.Col(html.Div(dcc.Graph(id='humidity-trend'), style={'margin-bottom': '20px', 'margin-top': '20px'}, ),
                     width=8),
             dbc.Col(
                 html.Div(
                     html.H4(id='humidity')
                 ), style={'margin-bottom': '20px', 'margin-top': '20px'}
             ),
         ]),

         dbc.Row([
             dbc.Col(html.Div(
                 html.Img(id="rgb")
             )),
         ]),
         dcc.Interval(
             id='rgb-update',
             interval=1 * 1000,  # in milliseconds
             n_intervals=0,
         ),
         dcc.Interval(
            id='graph-update',
            interval=1 * 1000,  # in milliseconds
            n_intervals=0,
         ),
         dcc.Interval(
             id='sentiment-pie-update',
             interval=1 * 1000,  # in milliseconds
             n_intervals=0,
         ),
         dcc.Interval(
             id='sleep-pos-update',
             interval=1 * 1000,  # in milliseconds
             n_intervals=0,
         ),
         dcc.Interval(
             id='heart-rate-update',
             interval=1 * 1000,  # in milliseconds
             n_intervals=0,
         ),
         dcc.Interval(
             id='room-temp-update',
             interval=1 * 1000,  # in milliseconds
             n_intervals=0,
         ),
         dcc.Interval(
             id='room-temp-trend-update',
             interval=1 * 1000,  # in milliseconds
             n_intervals=0,
         ),
         dcc.Interval(
             id='humidity-update',
             interval=1 * 1000,  # in milliseconds
             n_intervals=0,
         ),
         dcc.Interval(
             id='humidity-trend-update',
             interval=1 * 1000,  # in milliseconds
             n_intervals=0,
         ),
         dcc.Interval(
             id='REM-update',
             interval=1 * 1000,  # in milliseconds
             n_intervals=0,
         )
     ],
    id="mainContainer",
    style={'backgroundColor': app_colors['background'], 'margin-top': '50px', 'height': '2000px',
           'margin-bottom': '20px',
            'margin-left': '30px',
            'margin-right': '30px',
            'display':'flex',
            "flex-direction": "column",
               },
)

@app.callback(Output('heart_rate', "children"),
              [Input('heart-rate-update', 'n_intervals')])
def update_sleep_pos(n):

    conn = sqlite3.connect(r'D:\\4th_year\sleep_lab\sleep_lab\data_processor\sleep_lab.db')
    df = pd.read_sql("SELECT * FROM heart_info ORDER BY id DESC LIMIT 1", conn)
    HR = df['bpm'][0]
    return 'BPM: {0:.2f}'.format(HR)



@app.callback(Output('sleep-pos', "src"),
              [Input('sleep-pos-update', 'n_intervals')])
def update_sleep_pos(n):

    conn = sqlite3.connect(r'D:\\4th_year\sleep_lab\sleep_lab\data_processor\sleep_lab.db')
    df = pd.read_sql("SELECT * FROM position_info ORDER BY id DESC LIMIT 1", conn)
    pos = df['position'][0]
    if pos == 'facing up':
        src = "\\static\\figures\\face_up.jpg"
    if pos == 'facing down':
        src = "\\static\\figures\\face_down.jpg"
    if pos == 'facing left':
        src = "\\static\\figures\\face_left.jpg"
    if pos == 'facing right':
        src = "\\static\\figures\\face_right.jpg"
    if pos == 'transition':
        src = "\\static\\figures\\transition.jpg"


    app.get_asset_url(src)
    print('in source')
    return src

@app.callback(Output('live-graph', 'figure'),
              [Input('graph-update', 'n_intervals')])
def update_graph_scatter(n):
    try:
        conn = sqlite3.connect(r'D:\\4th_year\sleep_lab\sleep_lab\data_processor\sleep_lab.db')

        df = pd.read_sql("SELECT * FROM heart_info ORDER BY id DESC LIMIT 10", conn)

        Y = df['bpm']
        X = pd.to_datetime(df['time_stamp'])

        data = plotly.graph_objs.Scatter(
                x=X,
                y=Y,
                name='Scatter',
                mode= 'lines+markers'
                )
        app.logger.info('updating heart_info')

        layout_aggregate = copy.deepcopy(layout)
        layout_aggregate['xaxis']=dict(range=[min(X),max(X)])
        layout_aggregate['yaxis']=dict(range=[min(Y),150])
        layout_aggregate['title']='Heart Rate Trend'

        return dict(data=[data], layout=layout_aggregate)

    except Exception as e:
        with open('errors.txt','a') as f:
            f.write(str(e))
            traceback.print_exc()
            f.write('\n')

@app.callback(Output('sentiment-pie', 'figure'),
              [Input('sentiment-pie-update', 'n_intervals')])
def update_pie_chart(n):
    try:
        conn = sqlite3.connect(r'D:\\4th_year\sleep_lab\sleep_lab\data_processor\sleep_lab.db')

        down = pd.read_sql("SELECT count(*) FROM position_info WHERE position = 'facing down' ", conn)
        up = pd.read_sql("SELECT count(*) FROM position_info WHERE position = 'facing up'", conn)
        left = pd.read_sql("SELECT count(*) FROM position_info WHERE position = 'facing left'", conn)
        right = pd.read_sql("SELECT count(*) FROM position_info WHERE position = 'facing right'", conn)
        values = [down.at[0,'count(*)'], up.at[0,'count(*)'],left.at[0,'count(*)'],right.at[0,'count(*)']]

        labels = ['down', 'up' ,'left', 'right']
        print('updating position')

        data = dict(
            type='pie',
            labels=labels,
            values=values,
            name='Production Breakdown',
            hoverinfo="label+value+percent",
            textinfo="label+percent+name",
            hole=0.3,
            marker=dict(
                colors=['#FFA500','#66CDAA','#708090','#FFB6C1']
            ),
            domain={"x": [0, 0.5], 'y': [0.1, 0.8]},


        )

        layout_pie = copy.deepcopy(layout)
        layout_pie['font'] = dict(color='#777777')
        layout_pie['legend'] = dict(
            font=dict(color='#CCCCCC', size='10'),
            orientation='h',
            bgcolor='rgba(0,0,0,0)'
        )
        return {"data": [data], 'layout': layout_pie}

    except Exception as e:
        with open('errors.txt','a') as f:
            f.write(str(e))
            traceback.print_exc()
            f.write('\n')

@app.callback(Output('REM-pie', 'figure'),
              [Input('REM-update', 'n_intervals')])
def update_pie_chart(n):
    try:
        conn = sqlite3.connect(r'D:\\4th_year\sleep_lab\sleep_lab\data_processor\sleep_lab.db')

        moving = pd.read_sql("SELECT count(*) FROM rem_info WHERE eye_movement = 'moving' ", conn)
        steady = pd.read_sql("SELECT count(*) FROM rem_info WHERE eye_movement = 'steady'", conn)
        values = [moving.at[0,'count(*)'], steady.at[0,'count(*)']]

        labels = ['moving', 'steady']
        print('updating eye movement')

        data = dict(
            type='pie',
            labels=labels,
            values=values,
            name='Production Breakdown',
            hoverinfo="label+value+percent",
            textinfo="label+percent+name",
            hole=0.3,
            marker=dict(
                colors=['#FFA500','#66CDAA','#708090','#FFB6C1']
            ),
            domain={"x": [0, 0.5], 'y': [0.1, 0.8]},

        )

        layout_pie = copy.deepcopy(layout)
        layout_pie['title'] = 'Eye Movement summary'
        layout_pie['font'] = dict(color='#777777')
        layout_pie['legend'] = dict(
            font=dict(color='#CCCCCC', size='10'),
            orientation='h',
            bgcolor='rgba(0,0,0,0)'
        )
        return {"data": [data], 'layout': layout_pie}

    except Exception as e:
        with open('errors.txt','a') as f:
            f.write(str(e))
            traceback.print_exc()
            f.write('\n')

@app.callback(Output('REM-text', "children"),
              [Input('REM-update', 'n_intervals')])
def update_sleep_pos(n):

    conn = sqlite3.connect(r'D:\\4th_year\sleep_lab\sleep_lab\data_processor\sleep_lab.db')
    df = pd.read_sql("SELECT * FROM rem_info ORDER BY id DESC LIMIT 1", conn)
    move = df['eye_movement'][0]
    return 'eyes status: ' + move

@app.callback(Output('room-temp-trend', 'figure'),
              [Input('room-temp-trend-update', 'n_intervals')])
def update_graph_scatter(n):
    try:
        conn = sqlite3.connect(r'D:\\4th_year\sleep_lab\sleep_lab\data_processor\sleep_lab_serial.db')

        df = pd.read_sql("SELECT * FROM env_info ORDER BY id DESC LIMIT 10", conn)

        Y = df['Temperature']
        X = pd.to_datetime(df['time_stamp'])

        data = plotly.graph_objs.Scatter(
                x=X,
                y=Y,
                name='Scatter',
                mode= 'lines+markers'
                )
        app.logger.info('updating temp_info')

        layout_aggregate = copy.deepcopy(layout)
        layout_aggregate['xaxis']=dict(range=[min(X),max(X)])
        layout_aggregate['yaxis']=dict(range=[-10,50])
        layout_aggregate['title']='Room Temp Trend in Celsius'

        return dict(data=[data], layout=layout_aggregate)

    except Exception as e:
        with open('errors.txt','a') as f:
            f.write(str(e))
            traceback.print_exc()

@app.callback(Output('room-temp', "children"),
              [Input('room-temp-update', 'n_intervals')])
def update_sleep_pos(n):

    conn = sqlite3.connect(r'D:\\4th_year\sleep_lab\sleep_lab\data_processor\sleep_lab_serial.db')
    df = pd.read_sql("SELECT * FROM env_info ORDER BY id DESC LIMIT 1", conn)
    temp = df['Temperature'][0]
    return 'room temperature:  {0:.2f} celsius'.format(temp)


@app.callback(Output('humidity-trend', 'figure'),
              [Input('humidity-trend-update', 'n_intervals')])
def update_graph_scatter(n):
    try:
        conn = sqlite3.connect(r'D:\\4th_year\sleep_lab\sleep_lab\data_processor\sleep_lab_serial.db')

        df = pd.read_sql("SELECT * FROM env_info ORDER BY id DESC LIMIT 10", conn)

        Y = df['Humidity']
        X = pd.to_datetime(df['time_stamp'])

        data = plotly.graph_objs.Scatter(
                x=X,
                y=Y,
                name='Scatter',
                mode= 'lines+markers'
                )
        app.logger.info('updating temp_info')

        layout_aggregate = copy.deepcopy(layout)
        layout_aggregate['xaxis']=dict(range=[min(X),max(X)])
        layout_aggregate['yaxis']=dict(range=[-10,50])
        layout_aggregate['title']='Room Humidity Trend in Celsius'

        return dict(data=[data], layout=layout_aggregate)

    except Exception as e:
        with open('errors.txt','a') as f:
            f.write(str(e))
            traceback.print_exc()

@app.callback(Output('humidity', "children"),
              [Input('humidity-update', 'n_intervals')])
def update_sleep_pos(n):

    conn = sqlite3.connect(r'D:\\4th_year\sleep_lab\sleep_lab\data_processor\sleep_lab_serial.db')
    df = pd.read_sql("SELECT * FROM env_info ORDER BY id DESC LIMIT 1", conn)
    Humidity = df['Humidity'][0]
    return 'room Humidity:  {0:.2f} %'.format(Humidity)

def RGB(red,green,blue): return '#%02x%02x%02x' % (int(red),int(green),int(blue))

'''
@app.callback(Output('rgb', "children"),
              [Input('rgb-update', 'n_intervals')])
def update_rgb(n):

    conn = sqlite3.connect(r'D:\\4th_year\sleep_lab\sleep_lab\data_processor\sleep_lab_serial.db')
    df = pd.read_sql("SELECT * FROM env_info ORDER BY id DESC LIMIT 1", conn)
    r = df['r'][0]
    g = df['r'][0]
    b = df['r'][0]
    print(r,g,b)
    rgb = RGB(r, g,b)
    print(rgb)
    return 'light color', layout={'font':{'color':"{0}".format(rgb)

                                                  @ app.callback(Output('REM-pie', 'figure'),
                                                                 [Input('REM-update', 'n_intervals')])
'''
@app.callback(Output('rgb', "src"),
              [Input('rgb-update', 'n_intervals')])
def update_rgb(n):
    conn = sqlite3.connect(r'D:\\4th_year\sleep_lab\sleep_lab\data_processor\sleep_lab_serial.db')
    df = pd.read_sql("SELECT * FROM env_info ORDER BY id DESC LIMIT 1", conn)
    r = df['r'][0]
    g = df['r'][0]
    b = df['r'][0]

    rgb_mean = (r+g+b)/3
    print(rgb_mean)
    if rgb_mean < 10:
        src = "\\static\\figures\\dark.jpg"
    elif rgb_mean < 800:
        src = "\\static\\figures\\medium.jpg"
    else:
        src = "\\static\\figures\\bright.jpg"

    app.get_asset_url(src)
    print('in source')
    return src

if __name__ == '__main__':
    app.run_server(debug=True)
