from dash import dcc
from dash import html
from dash.dependencies import Input, Output

from app import app
from apps import app1, app2


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/dash/apps/app1':
         return app1.layout
    elif pathname == '/dash/apps/app2':
         return app2.layout
    else:
        return '404'
