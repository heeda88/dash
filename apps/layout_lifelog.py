
from dash import dcc , State
from dash import html
import dash_bootstrap_components as dbc

from dash.dependencies import Input, Output
from app import app

import pandas as pd
import os


import base64
from urllib.parse import quote as urlquote

from glob import glob

from dash import dash_table



UPLOAD_DIRECTORY="uploads/app_uploaded_files/*"

def generate_table2(path:str):
    if '.csv' in path:
        df= pd.read_csv(f'./{path}')
    else :
        df=pd.read_excel(f'./{path}')
        
    view_df=df.copy()
    masking="===Masking==="
    masking_list=['외래일자','검사일자','검사코드']
    view_df.loc[:,masking_list]=masking
    view_df.loc[:,'검사코드']="Local_XXXX"
    table=dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in view_df.columns],
        data=view_df.to_dict('records'),
        page_size=10,  # we have less data in this example, so setting to 20
        style_table={'height': 'auto', 'overflowY':'auto','width':'auto','color':'gray'}
    )
    return table

def convert_table2(path:str):
    if '.csv' in path:
        out_df= pd.read_csv(f'./{path}')
    else :
        out_df=pd.read_excel(f'./{path}')
        
    out_df.rename(columns={'등록번호':'UID','검사코드':'OMOP-CDM'}, inplace=True)
    view_out_df=out_df.copy()
    masking="===Masking==="
    masking_list=['외래일자','검사일자','OMOP-CDM']
    view_out_df.loc[:,masking_list]=masking
    view_out_df.loc[:,'UID']="Pat_XXXXXX"
    view_out_df.loc[:,'OMOP-CDM']="CDM_XXXXX"
    table2=html.Div(children=[
        dcc.Dropdown(options=[],placeholder=f'File : CDM_{os.path.basename(path)}'),
        dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in view_out_df.columns],
        data=view_out_df.to_dict('records'),
        page_size=10,  # we have less data in this example, so setting to 20
        style_table={'height': 'auto', 'overflowY':'auto','width':'auto','color':'black'}
        )    
    ])
    return table2

def save_file(name, content):
    """Decode and store a file uploaded with Plotly Dash."""
    data = content.encode("utf8").split(b";base64,")[1]
    with open(os.path.join(UPLOAD_DIRECTORY, name), "wb") as fp:
        fp.write(base64.decodebytes(data))

def uploaded_files():
    """List the files in the upload directory."""
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return files

def file_download_link(filename):
    """Create a Plotly Dash 'A' element that downloads a file from the app."""
    location = "/download/{}".format(urlquote(filename))
    return html.A(filename, href=location)

def update_file_list(UPLOAD_DIRECTORY=UPLOAD_DIRECTORY):
    return glob(UPLOAD_DIRECTORY)

layout_table= html.Div(
    children=[
        dbc.Row(children=[
            dbc.Col([
                dbc.Button(children=["To CDM convert"],style={'textAlign':'center',"font-size":"20px","font-weight":"bold","color":"#ffffff","background":"#B4CFB0"})
            ],sm=5),
            dbc.Col([
                dbc.Button(id='app-lifelog-update',n_clicks=0,children=["update"],style={'textAlign':'center',"font-size":"20px","font-weight":"bold","color":"#ffffff","background":"#B4CFB0"})
            ],sm=1),
            dbc.Col([
                dbc.Button(children=["완료_"],style={'textAlign':'center',"font-size":"20px","font-weight":"bold","color":"#ffffff","background":"#789395"})
            ],sm=1),
            dbc.Col([
                dbc.Button(children=["재검토"],style={'textAlign':'center',"font-size":"20px","font-weight":"bold","color":"#ffffff","background":"#FFBFA3"})
            ],sm=1),
        ],style={"margin-bottom":"20px"}),
        dbc.Row(children= [
            dbc.Col([
                dcc.Dropdown(id='app-lifelog-dropdown',
                                options=[{'label' : f'File : {os.path.basename(index)}', 'value': index } for index in update_file_list()]
                ),
                html.Div(id='app-liflog-column',children=[]),
                html.Div(id='app-lifelog-input-display'),
                html.Div(children=[]),
                    
            ],sm=6), 
            dbc.Col([
                html.Div(id='app-lifelog-output-display')
            
            ],sm=6),
        ]),
        
    ])

# 무조건 call back을 시켜야함 


@app.callback(  Output('app-lifelog-input-display','children'),
                Output('app-lifelog-output-display','children'),
                Input('app-lifelog-dropdown','value')
)
def tableCallback(value):
    if value is None:
        return 'You are not selected',""
    elif ('.csv' or '.xls' or 'xlsx' in value):
        input_table=generate_table2(value)
        output_table=convert_table2(value)
        return input_table, output_table
    else:
        return 'You have selected "{}"'.format(value),""
html.Div([
    html.Button('Button 1', id='btn-nclicks-1', n_clicks=0),
    html.Button('Button 2', id='btn-nclicks-2', n_clicks=0),
    html.Button('Button 3', id='btn-nclicks-3', n_clicks=0),
    html.Div(id='container-button-timestamp')
])

@app.callback(
    Output('app-lifelog-dropdown', 'options'),
    Input('app-lifelog-update', 'n_clicks'),
    # State('input-on-submit', 'value')
)
def update_output(n_clicks):
    n_clicks
    return [{'label' : f'File : {os.path.basename(index)}', 'value': index } for index in update_file_list()]