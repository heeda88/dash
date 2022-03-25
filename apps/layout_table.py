
from dash import dcc
from dash import html

from dash.dependencies import Input, Output
from app import app

import pandas as pd

from glob import glob

from dash import dash_table


UPLOAD_DIRECTORY="uploads/app_uploaded_files/*"

def generate_table2(path:str):
    df= pd.read_csv(f'./{path}')
    table=dash_table.DataTable(
    id='table2',
    columns=[{"name": i, "id": i} for i in df.columns],
    data=df.to_dict('records'),
    page_size=20,  # we have less data in this example, so setting to 20
    style_table={'height': 'auto', 'overflowY':'auto','width':'auto'}
    )
    return table


layout_table= html.Div(children=[
    dcc.Dropdown(id='app-table-dropdown',
                options=[{'label' : f'File : {index}', 'value': index } for index in glob(UPLOAD_DIRECTORY)]
    ),
    html.Div(children=[]),
    html.Div(id='app-table-display'),
    html.Div(children=[]),
])

@app.callback(  Output('app-table-display','children'),
                Input('app-table-dropdown','value')
)
def tableCallback(value):
    if value is None:
        return 'You are not selected'
    elif ( ('.csv' in value) or ('.xlsx' in value) ):
        return generate_table2(value)
    elif '.md' in value:
        return dcc.Markdown( open(f'./{value}','r').read() )
    else:
        return 'You have selected "{}"'.format(value)

# @app.callback(  Output('app-table-dropdown','options'),Input('app-table-dropdown','value')
# )
# def tableListCallback(valu):
#     return [{'label' : f'File : {index}', f'value': {index} } for index in glob(UPLOAD_DIRECTORY)]