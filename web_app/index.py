import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from web_app.apps import history_dash, summary_dash, home
from web_app.app import app

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return home.app_layout
    if pathname == '/apps/history_dash':
        return history_dash.app_layout
    elif pathname == '/apps/summary_dash':
        return summary_dash.app_layout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)