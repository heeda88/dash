
from dash import dcc
from dash import html

from dash.dependencies import Input, Output
from app import app

# layout_list
layout_list = html.Div(children=[ html.H1('App 1'),
	dcc.Dropdown(
        id='app-1-dropdown',
        options=[
            {'label': 'App 1 - {}'.format(i), 'value': i} for i in [
                'BLUE', 'RED', 'GREEN'
            ]
        ]
    ),
	html.Div(id='app-1-display-value'),
	html.Br(),
	dcc.Link('Go to Dash Board', href='/dash/dashboard'),
	html.Br(),
	dcc.Link('Go to Upload', href='/dash/store'),
	html.Br(),
	dcc.Link('Go to CDM', href='/dash/apps/lifelog'),
	html.Br(),
	dcc.Link('Go to table_select', href='/dash/apps/table_header'),
	html.Br(),
	dcc.Link('Go to Labelling', href='/dash/apps/label'),
	html.Br(),
 	dcc.Link('Go to CKD-Labelling', href='/dash/apps/ckd_label'),
	html.Br(),
	dcc.Link('Go to Label List', href='/dash/apps/label_list'),
	html.Br(),
])

	# if pathname == '/dash/':
	# 		return layout_main.layout_main
	# elif pathname == '/dash/list':
	# 		return layout_list.layout_list
	# elif pathname == '/dash/dashboard':
	# 		return layout_list.layout_list
	# # elif pathname == '/dash/upload':
	# # 		return layout_upload
	# elif pathname == '/dash/apps/table_select':
	# 		return layout_table_select.table_select
	# elif pathname == '/dash/apps/table':
	# 		return layout_table.layout_table
	# elif pathname == '/dash/apps/image_annotation':
	# 		return layout_annotation.layout_annotation
	# elif pathname == '/dash/speech':
	# 		return speech_data_exploler.stats_layout
	# elif pathname == '/dash/speech/sample':
	# 		return speech_data_exploler.samples_layout	
	# elif pathname == '/dash/store':
	# 		return layout_store.layout_store