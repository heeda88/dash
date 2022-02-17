

from dash import dcc
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
        dcc.Dropdown(options=[],placeholder=f'File : CDM_원천데이터.xls'),
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


# layout_store = html.Div(
#     [
#         html.H6("Upload"),
#         dcc.Upload(
#             id="upload-data",
#             children=html.Div(
#                 ["Drag and drop or click to select a file to upload."]
#             ),
#             style={
#                 "width": "100%",
#                 "height": "60px",
#                 "lineHeight": "60px",
#                 "borderWidth": "1px",
#                 "borderStyle": "dashed",
#                 "borderRadius": "5px",
#                 "textAlign": "center",
#                 "margin": "10px",
#             },
#             multiple=True,
#         ),
#         html.H6("File List"),
#         html.Ul(id="file-list"),
#     ],
#     style={"max-width": "500px"},
# )

layout_table= html.Div(children=[
#   dbc.Row(children=[layout_store]),
    dbc.Row(children= [
        dbc.Col([

            dcc.Dropdown(id='app-lifelog-dropdown',
                            options=[{'label' : f'File : {os.path.basename(index)}', 'value': index } for index in glob(UPLOAD_DIRECTORY)]
            ),
            html.Div(id='app-liflog-column',children=[]),
            html.Div(id='app-lifelog-input-display'),
            html.Div(children=[]),
                
        ],sm=6), dbc.Col([
            html.Div(id='app-lifelog-output-display')
        
        ],sm=6),
    ])
])


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
    
