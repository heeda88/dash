
from turtle import left
from dash import dcc
from dash import html

from dash.dependencies import Input, Output

import dash_bootstrap_components as dbc
from dash import dash_table

import pandas as pd
import numpy as np


from app import app






df_list=[]
for index in range(0,6000):
    row_list=[]
    row_list=[f'Pat_{str(index).zfill(6)}','datetime','Hospital','age','worker','datetime','대기']
    df_list.append(row_list)

df = pd.DataFrame(data=df_list,columns=['HRA_UID','등록일','등록기관','연령대','작업자','작업일','작업상태'])

# df.loc[0,:]=['HRA_UID','datetime','Hospital','age','worker','datetime','status']

layout_export= html.Div(
    children=[
        html.H3("Index Range"),
        dbc.Row(
            children=[
                dbc.Col([dcc.Input(value=1,id="label-list-input-index-1")], sm=4), 
                dbc.Col([""],sm=4),
                dbc.Col([dcc.Input(value=20,id="label-list-input-index-2")], sm=4)
            ]
        ),
        html.H6("data_List"),
        # html.Ul(id="label-data-list"),
    dbc.Row(children=[
        dbc.Container([
            dash_table.DataTable(
                df.to_dict('records'),
                [{"name": i, "id": i} for i in df.columns], 
                id='tbl',
                style_as_list_view=True,  
                page_size=20,  
                style_header={'backgroundColor': '#eeeeee','color':'black','fontWeight': 'bold','textAlign':'left', 'margin-left':'0px','border-bottom':'3px solid #dddddd'}, 
                style_cell={'backgroundColor': '#ccccc','color':'black',"textAlign":'left'}),
            dbc.Alert(id='tbl_out'),
        ],style={'textAlign':'left'})    
    ]),


    ],
    style={},
)


@app.callback(Output('tbl_out', 'children'), Input('tbl', 'active_cell'))
def update_graphs(active_cell):
    return str(active_cell) if active_cell else "Click the table"

if __name__ == "__main__":
    app.run_server(debug=True)


@app.callback(
    Output("label-data-list", "children"),
    [Input("label-list-input-index-1", "value"), Input("label-list-input-index-2", "value")],
)
def update_output(index_start, index_end):
    """Save uploaded files and regenerate the file list."""
    rt_layout=[html.Li(children=f"HAR_{index}",style={"border-top":'1px solid','padding':'1px'}) for index in range(index_start,index_end)]
    return rt_layout