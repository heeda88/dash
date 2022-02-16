

from dash import dcc
from dash import html

from dash.dependencies import Input, Output
from app import app

import pandas as pd

from glob import glob


UPLOAD_DIRECTORY="uploads/app_uploaded_files/*"

url_path='https://gist.githubusercontent.com/chriddyp/c78bf172206ce24f77d6363a2d754b59/raw/c353e8ef842413cae56ae3920b8fd78468aa4cb2/usa-agricultural-exports-2011.csv'
df = pd.read_csv('https://gist.githubusercontent.com/chriddyp/c78bf172206ce24f77d6363a2d754b59/raw/c353e8ef842413cae56ae3920b8fd78468aa4cb2/usa-agricultural-exports-2011.csv')


# table_3
def generate_table(path:str, max_rows=10):
    dataframe=pd.read_csv(path)
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

# lay_out_1
table_header = html.Div([
    html.H3('Data table Head'),
    dcc.Dropdown(
        id='app-tableSelct-dropdown',
        options=[
            {'label': 'App 1 - {}'.format(i), 'value': i} for i in glob(UPLOAD_DIRECTORY)
        ]
    ),
    html.Br(),
    html.Div(id='app-1-display-value'),
    html.Br(),
    html.Div(id="data-list"),
    html.Br(),
    html.Br(),
    html.Br(),

])
@app.callback(
    Output('app-1-display-value', 'children'),
    Output('data-list', 'children'),
    Input('app-tableSelct-dropdown', 'value'))
def display_value(value):
    if (value is not None) and ( ('.csv' in value) or ('.xlsx' in value) ):
        return ['You have selected "{}"'.format(value), generate_table(path=f'./{value}')]
    else:
        return ['You have selected "{}"'.format(value), '']
    



