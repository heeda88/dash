

from cProfile import label
from turtle import color
from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

import dash_bootstrap_components as dbc

import collections

import pandas as pd
import os

import base64
from urllib.parse import quote as urlquote

from glob import glob
from app import app


import plotly.express as px
import plotly.graph_objects as go


df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')

df_1 = px.data.stocks(indexed=True)-1
# 컬럼을 재정의하면 그후에  컬럼 name 또한 재임명해야함 
df_1.columns=['나트륨', '단백질', '지방', '칼륨', '탄수화물', '수분']
df_1.columns.name='영양성분'
fig_1 = px.area(df_1, facet_col="영양성분", facet_col_wrap=2, title='식이습관데이터')


df_2 = px.data.stocks()
df_2.columns=['date', 'LM_XXX1', 'AO_XXXX', 'UA_XXXX', 'HE_XXXX', 'DM_XXXX', 'ST_XXXX']
fig_2 = px.line(df_2, x="date", y=df_2.columns,
              hover_data={"date": "|%B %d, %Y"},
              title='생활습관데이터')
fig_2.update_xaxes(
    dtick="M1",
    tickformat="%b\n%Y",
    ticklabelmode="period")
component_list_1=[
    dbc.Row(
        children=[
            html.H6('당뇨 유형', style={'textAlign':'left'}),
            dcc.Slider(0, 140, 0.1, value=30, 
                marks={
                        10: {'label': '정상', 'style': {'color': '#99cc33'}},
                        30: {'label': '제 1형 당뇨', 'style': {'color': '#ffaa00'}},
                        70: {'label': '제 2형 당뇨(인슐린X)', 'style': {'color': '#DD9966'}},
                        105: {'label': '제 2형 당뇨(인슐린O)', 'style': {'color': '#cc3300'}}
                },
            )
        ],
        style={'margin-bottom':'25px'}
    ),
    dbc.Row(
        children=[
                html.H6('공복혈당', style={'textAlign':'left'}),
                dcc.Slider(0, 140, 0.1, value=70, 
                    marks={
                        25: {'label': '정상', 'style': {'color': '#99cc33'}},
                        50: {'label': '초기', 'style': {'color': '#ffaa00'}},
                        80: {'label': '중증', 'style': {'color': '#DD9966'}},
                        110: {'label': '고위험', 'style': {'color': '#cc3300'}}
                    },
                    tooltip={"placement": "bottom", "always_visible": True}
                )
        ],
        style={'margin-bottom':'25px'}
    ),
    dbc.Row(
        children=[
            html.H6('당화혈색소', style={'textAlign':'left'}),
            dcc.Slider(0, 140, 0.1, value=70, 
                marks={
                    25: {'label': '정상', 'style': {'color': '#99cc33'}},
                    50: {'label': '초기', 'style': {'color': '#ffaa00'}},
                    80: {'label': '중증', 'style': {'color': '#DD9966'}},
                    110: {'label': '고위험', 'style': {'color': '#cc3300'}}
                },
                tooltip={"placement": "bottom", "always_visible": True}
            )
        ],
        style={'margin-bottom':'25px'}
    ),
    dbc.Row(
        children=[
            html.H6('당뇨약 복용 여부', style={'textAlign':'left'}),
            dcc.Slider(0, 140, 0.1, value=100, 
                marks={
                    30: {'label': '당뇨약 미복용', 'style': {'color': '#99cc33'}},
                    100: {'label': '당뇨약 복용', 'style': {'color': '#cc3300'}},
                },
            )
        ],
        style={'margin-bottom':'25px'}
    ),
    dbc.Row(
        children=[
            html.H6('당뇨 기왕력 여부', style={'textAlign':'left'}),
            dcc.Slider(0, 140, 0.1, value=100, 
                marks={
                    30: {'label': '기왕력 X', 'style': {'color': '#99cc33'}},
                    100: {'label': '기왕력 O', 'style': {'color': '#cc3300'}},
                },
            )
        ],
        style={'margin-bottom':'25px'}
    ),
    # dcc.Graph(figure=fig_1),
    # dcc.Store(id='ckd-label-1-memory-output'),
    # dcc.Dropdown(options=df.country.unique(),
    #                 value=['Canada', 'United States'],
    #                 id='ckd-label-1-memory-countries',
    #                 multi=True),
    # dcc.Dropdown(options={'lifeExp': 'Life expectancy', 'gdpPercap': 'GDP per capita','pop':'Population'},
    #                 value='lifeExp',
    #                 id='ckd-label-1-memory-field'),
    # html.Div([
    #    # dcc.Graph(id='ckd-label-1-memory-graph'),
    #     dash_table.DataTable(
    #         id='ckd-label-1-memory-table',
    #         columns=[{'name': '혈중검사_XX', 'id': i} for i in df.columns],
    #         style_header={'color':'black', 'font-weight':'bold','background': '#c9dff0','textAlign': 'center'},
    #         style_cell={'textAlign': 'right','font-size':'0.5rem'},
    #     ),
    # ]) 
]

component_list_2=[
    dbc.Row(
        children=[
            html.H6('고혈압 유형', style={'textAlign':'left'}),
            dcc.Slider(0, 140, 0.1, value=10, 
                marks={
                        10: {'label': '정상', 'style': {'color': '#99cc33'}},
                        30: {'label': '전고혈압', 'style': {'color': '#ffaa00'}},
                        70: {'label': '고혈압1기', 'style': {'color': '#DD9966'}},
                        105: {'label': '고혈압2기', 'style': {'color': '#cc3300'}}
                },
            )
        ],
        style={'margin-bottom':'25px'}
    ),
    dbc.Row(
        children=[
                html.H6('수축기 혈압', style={'textAlign':'left'}),
                dcc.Slider(60, 200, 0.1, value=100, 
                    marks={
                        90: {'label': '정상', 'style': {'color': '#99cc33'}},
                        125: {'label': '초기', 'style': {'color': '#ffaa00'}},
                        144: {'label': '중증', 'style': {'color': '#DD9966'}},
                        160: {'label': '고위험', 'style': {'color': '#cc3300'}}
                    },
                    tooltip={"placement": "bottom", "always_visible": True}
                )
        ],
        style={'margin-bottom':'25px'}
    ),
    dbc.Row(
        children=[
            html.H6('이완기 혈압', style={'textAlign':'left'}),
            dcc.Slider(60, 180, 0.1, value=80, 
                marks={
                    70: {'label': '정상', 'style': {'color': '#99cc33'}},
                    105: {'label': '초기', 'style': {'color': '#ffaa00'}},
                    120: {'label': '중증', 'style': {'color': '#DD9966'}},
                    140: {'label': '고위험', 'style': {'color': '#cc3300'}}
                },
                tooltip={"placement": "bottom", "always_visible": True}
            )
        ],
        style={'margin-bottom':'25px'}
    ),
    dbc.Row(
        children=[
            html.H6('고혈압약 복용 여부', style={'textAlign':'left'}),
            dcc.Slider(0, 140, 0.1, value=30, 
                marks={
                    30: {'label': '고혈압약 미복용', 'style': {'color': '#99cc33'}},
                    100: {'label': '고혈압약 복용', 'style': {'color': '#cc3300'}},
                },
            )
        ],
        style={'margin-bottom':'25px'}
    ),
    dbc.Row(
        children=[
            html.H6('고혈압 기왕력 여부', style={'textAlign':'left'}),
            dcc.Slider(0, 140, 0.1, value=30, 
                marks={
                    30: {'label': '기왕력 X', 'style': {'color': '#99cc33'}},
                    100: {'label': '기왕력 O', 'style': {'color': '#cc3300'}},
                },
            )
        ],
        style={'margin-bottom':'25px'}
    ),
    # dcc.Graph(figure=fig_2),
    # dcc.Store(id='ckd-label-2-memory-output'),
    # dcc.Dropdown(options=df.continent.unique(),
    #                 value=['Americas'],
    #                 id='ckd-label-2-memory-continent',
    #                 multi=True),
    # dcc.Dropdown({'lifeExp': 'Life expectancy', 'gdpPercap': 'GDP per capita','pop':'Population'},
    #                 'lifeExp',
    #                 id='ckd-label-2-memory-field'),
    # html.Div([
    #     dcc.Graph(id='ckd-label-2-memory-graph'),
    #     dash_table.DataTable(
    #         id='ckd-label-2-memory-table',
    #         columns=[{'name': '임상검사_XX', 'id': i} for i in df.columns],
    #         style_header={'color':'black', 'font-weight':'bold','background': '#99aa37','textAlign': 'center'},
    #         style_cell={'textAlign': 'right','font-size':'0.5rem','textOverflow':'inherit','overflow': 'hidden'}
    #     ),
    # ]) 
]

label_list=[
    html.H3('Labelling List', style={'textAlign':'center','margin-bottom':'25px','color':'white'}),
    dbc.Row(children=[
        dbc.Col(children=[
            html.H6('입원 유형', style={'textAlign':'left'}),
            dcc.Dropdown(options=['미입원', '기저질환악화','감염성질환','기타원인','재검토', '미입력'],value='미입력')
        ],
        sm=4),
        dbc.Col(children=[
            html.H6('심혈관계 사건 ', style={'textAlign':'left'}),
            dcc.Dropdown(options=['정상', 'revascularization','stroke','death','arrhythmia','기타원인','재검토', '미입력'], value='미입력')
        ],
         sm=4),
        dbc.Col(children=[
            html.H6('신장기능 악화', style={'textAlign':'left'}),
            dcc.Dropdown(options=['정상', '신장기능악화','재검토', '미입력'], value='미입력')
        ],
        sm=4),
    ],
        style={'font-size':'0.8rem','margin-bottom':'25px'}
    ),
]


layout_label = html.Div(children=[

    dbc.Row(children=[
        dbc.Col(
            children=component_list_1,
            sm=4
        ),
        dbc.Col(
            children=component_list_2,
            sm=4
        ),
        dbc.Col(
            children=label_list,
            sm=4,
            style={'border':'dashed 5px black','border-radius':'20px', 'padding-top':'1%'}
        )    
    ])
])

# 드롭 다운에서 국가를 선택하면 해당 국가 데이터가 넘어옴 
@app.callback(Output('ckd-label-1-memory-output', 'data'),
              Input('ckd-label-1-memory-countries', 'value'))
def filter_countries(countries_selected):
    if not countries_selected:
        # Return all the rows on initial load/no country selected.
        return df.to_dict('records')

    filtered = df.query('country in @countries_selected')

    return filtered.to_dict('records')


@app.callback(Output('ckd-label-1-memory-table', 'data'),
              Input('ckd-label-1-memory-output', 'data'))
def on_data_set_table(data):
    if data is None:
        raise PreventUpdate
    return data


@app.callback(Output('ckd-label-1-memory-graph', 'figure'),
              Input('ckd-label-1-memory-output', 'data'),
              Input('ckd-label-1-memory-field', 'value'))
def on_data_set_graph(data, field):
    if data is None:
        raise PreventUpdate

    aggregation = collections.defaultdict(
        lambda: collections.defaultdict(list)
    )

    for row in data:

        a = aggregation[row['country']]

        a['name'] = row['country']
        a['mode'] = 'lines+markers'

        a['y'].append(row[field])
        a['x'].append(row['year'])

    return {
        'data': [x for x in aggregation.values()]
    }


# 드롭 다운에서 국가를 선택하면 해당 국가 데이터가 넘어옴 
@app.callback(Output('ckd-label-2-memory-output', 'data'),
              Input('ckd-label-2-memory-continent', 'value'))
def filter_countries(continent_selected):
    if not continent_selected:
        # Return all the rows on initial load/no country selected.
        return df.to_dict('records')

    filtered = df.query('continent in @continent_selected')

    return filtered.to_dict('records')


@app.callback(Output('ckd-label-2-memory-table', 'data'),
              Input('ckd-label-2-memory-output', 'data'))
def on_data_set_table(data):
    if data is None:
        raise PreventUpdate
    return data


@app.callback(Output('ckd-label-2-memory-graph', 'figure'),
              Input('ckd-label-2-memory-output', 'data'),
              Input('ckd-label-2-memory-field', 'value'))

def on_data_set_graph(data, field):
    if data is None:
        raise PreventUpdate

    aggregation = collections.defaultdict(
        lambda: collections.defaultdict(list)
    )

    for row in data:
        b = aggregation[row['continent']]
        b['name'] = row['continent']
        b['mode'] = 'markers'
        b['y'].append(row[field])
        b['x'].append(row['pop'])
        
    df = px.data.iris()
    name_list=['약제데이터1','약제데이터2','약제데이터3']
    for index in df.loc[:,'species'].unique().tolist():
        cond_list=(df.loc[:,'species']==index)
        df.loc[cond_list,'species']=name_list[df.loc[:,'species'].unique().tolist().index(index)]
        
    df.loc[:,'type']=df.loc[:,'species'].copy()
    df.loc[:,'x']=df.loc[:,'sepal_width'].copy()
    df.loc[:,'y']=df.loc[:,'sepal_length'].copy()
    fig = px.scatter(df, x="x", y="y", color="type")

    fig.update_traces(marker=dict(size=12,
                                line=dict(width=2,
                                            color='DarkSlateGrey')),
                    selector=dict(mode='markers'))
    return fig    
    # return {
    #     'data': [x for x in aggregation.values()],
    # }
