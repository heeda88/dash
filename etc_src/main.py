# from fastapi import FastAPI
# from fastapi import BackgroundTasks
# from fastapi.responses import HTMLResponse
# from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates

# from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
# from fastapi_mail.email_utils import DefaultChecker
# from fastapi.responses import FileResponse

# from starlette.requests import Request
# from starlette.responses import JSONResponse
# from starlette.middleware.wsgi import WSGIMiddleware

# from pydantic import EmailStr, BaseModel
# from typing import List, Dict, Any

# import dash
# from dash import dcc
# from dash import html
# from dash import dash_table
# import dash_bootstrap_components as dbc
# from dash.dependencies import Input, Output

# import pandas as pd
# import plotly.graph_objs as obj

# import base64
# import os
# from urllib.parse import quote as urlquote



# UPLOAD_DIRECTORY = "uploads/app_uploaded_files"
# if not os.path.exists(UPLOAD_DIRECTORY):
#     os.makedirs(UPLOAD_DIRECTORY)

# ##############
# ## 기본 구동##
# #############
# # 해당변수에 Fast API class instance 주소값 저장

# namu=FastAPI()
# namu.mount("/static", StaticFiles(directory="static"), name="static")
# templates = Jinja2Templates(directory="static/templates")


# # @something구문을 "decorator" ,  패스트 API 사용하는것을 path operation decorator 라고함 
# @namu.get("/")
# async def root():
#     return {"message" :  "Hello World"}

# ## http protocol mainly method list = ['GET','POST','PUT','DELETE'] 
# # GET  = 서버 메모리에 있는 데이터 읽어오기
# # POST = 서버 메모리에 데이터 추가하기
# # PUT  = 서버 메모리에 있는 기존 데이터 대체
# # DELETE = 서버 메모리에 있는 데이터 삭제
# # FAST API에서는 위의 메소드들을  'operation'이라고 말함

# ## 잘쓰이지 않는 메소드 리스트 = [OPTIONS, HEAD, PATCH,TRACE]


# ###################
# ## Path parmeter ##
# ###################

# # 자체 포맷터 기능이 존재함 {} 변수받는곳 즉 url에서 입력데이터를 받을 수 있음
# # 클래스인스턴스에서 종속되는 함수이므로 클래스 변수명과 함수 변수명이 같아야 url 입력값을 함수에 적용할수 있음

# # item_id-> item 
# # 경로매개변수를 함수인자와 달리 설정하는 경우 아래와 같은 처리불가 메세지가 뜨는데
# # {"detail":[{"loc":["query","item"],"msg":"field required","type":"value_error.missing"}]}
# # loc query, item이 나온걸로봐서 query문 안에 item이라는 인자가 존재하지 않아 발생한 문제로 확인 

# # heeda-namu/ok/miniconda3/LICENSE.txt

# # 데코레이터 인수에 int 타입으로 지정하는 경우
# # 정수가 들어오면 정수값을 받지만  이 들어오는경우 데코레이터 인수로 판별함

# @namu.get("/items/{item_id:int}")
# async def read_item(item_id):
#     return {"item_id":item_id}
# # 데코레이터 인수에  path 타입으로 지정을 하는경우 
# # 디렉토리 구문자 "/"를 지정구간 까지 string으로 인수를 받아들임 

# @namu.get("/path/{item_id:path}/miniconda3/{filename}")
# async def read_path(item_id:str, filename:str):
#     return {"item_id":item_id,"filename":filename}

# @namu.get("/template/items/{id}", response_class=HTMLResponse)
# async def read_template(request: Request, id: str):
#     return templates.TemplateResponse("item.html", {"request": request, "id": id})

# @namu.get("/index", response_class=HTMLResponse)
# async def read_template(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})


# @namu.get("/login", response_class=HTMLResponse)
# async def read_template(request: Request):
#     return templates.TemplateResponse("login.html", {"request": request})

# @namu.get("/cat", response_class=HTMLResponse)
# async def read_template(request: Request):
#     return templates.TemplateResponse("cat.html", {"request": request})

# @namu.get("/download/{path:path}")
# def download(path:str):
# 	"""Serve a file from the upload directory."""
# 	return FileResponse(path=UPLOAD_DIRECTORY+'/'+path, filename=path, media_type='text/mp4')


# ###########
# ## E-Mail##
# ###########

# class EmailSchema(BaseModel):
# 	email: List[EmailStr]
# 	body: Dict[str, Any]

# conf = ConnectionConfig(
# 	MAIL_USERNAME='hdshin@namuintelligence.com',
# 	MAIL_PASSWORD="namu02110hd!!",
# 	MAIL_FROM = "hdshin@namuintelligence.com",
# 	MAIL_PORT=587,
# 	MAIL_SERVER="smtp.gmail.com",
# 	MAIL_TLS=True,
# 	MAIL_SSL=False,
# 	USE_CREDENTIALS = True,
# 	VALIDATE_CERTS = True,
# 	TEMPLATE_FOLDER ='static/templates'
# )

# # html = """
# # <p>Hi this test mail, thanks for using Fastapi-mail</p> 
# # """
# async def send_email_async(subject: str, email_to: str, body: dict):
# 	message = MessageSchema(
# 			subject=subject,
# 			recipients=[email_to],
# 			template_body=body,
# 			subtype='html',
# 	)
# 	fm = FastMail(conf)
# 	await fm.send_message(message, template_name='email.html')

# def send_email_background(background_tasks: BackgroundTasks, subject: str, email_to: str, body: dict):
# 	print(email_to,'=====================')
# 	message = MessageSchema(
# 			subject=subject,
# 			recipients=[email_to],
# 			template_body=body,
# 			subtype='html',
# 	)
# 	fm = FastMail(conf)
# 	background_tasks.add_task(
# 		fm.send_message, message, template_name='email.html')

# # POST- > 웹에서  단순 접근으로 확인하려고하면 405 에러가 뜨게됨 post 전용 페이지이기 때문
# @namu.get('/send-email/asynchronous')
# async def send_email_asynchronous():
#     await send_email_async('Hello World','chesyuyu@gmail.com', body={'title': 'Hello World', 'name': 'Shin heeda'})
#     return JSONResponse(status_code=200, content={"message": "email has been sent"})

# @namu.get('/send-email/backgroundtasks')
# def send_email_backgroundtasks(background_tasks: BackgroundTasks):
#     send_email_background(background_tasks, 'Hello World',   
#     'chesyuyu@gmail.com', body={'title': 'Hello World', 'name':  'Shin heeda'})
#     return JSONResponse(status_code=200, content={"message": "email has been sent"})


# @namu.get('/e-mail/namu/{email_to}')
# def send_email_backgroundtasks(background_tasks: BackgroundTasks, email_to:str):
#     send_email_background(background_tasks, 'Hello World', email_to=email_to, body={'title': 'Hello World', 'name':  'Shin heeda'})
#     return JSONResponse(status_code=200, content={"message": "email has been sent"})


# ##########
# ## dash ##
# ##########
# app = dash.Dash(__name__, requests_pathname_prefix="/dash/", external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
# app.enable_dev_tools(debug=True)
# namu.mount("/dash", WSGIMiddleware(app.server),name="dash")


# ## color palette

# #C0D8C0 Teal
# #F5EEDC Beige
# #DD4A48 Red
# #ECB390 Orange
# nav_div="""
# <div class='area'></div>
# <nav class="main-menu">
# 		<ul>
# 			<li>
# 				<a href="/index">
# 					<i class="fa fa-home fa-2x"></i>
# 					<span class="nav-text">
# 						Home
# 					</span>
# 				</a>
# 			</li>
# 			<li class="has-subnav">
# 				<a href="/dash/dashboard">
# 					<i class="fa fa-bars fa-2x"></i>
# 					<span class="nav-text">
# 						Dashboard
# 					</span>
# 				</a>
# 			</li>
# 			<li clas
# 			<li class="has-subnav">
# 				<a href="#">
# 					<i class="fa fa-laptop fa-2x"></i>
# 					<span class="nav-text">
# 						UI Components
# 					</span>
# 				</a>
				
# 			</li>
# 			<li class="has-subnav">
# 				<a href="/dash/list">
# 					<i class="fa fa-list fa-2x"></i>
# 					<span class="nav-text">
# 						Lists
# 					</span>
# 				</a>
				
# 			</li>
# 			<li class="has-subnav">
# 				<a href="#">
# 					<i class="fa fa-folder-open fa-2x"></i>
# 					<span class="nav-text">
# 						Pages
# 					</span>
# 				</a>
				
# 			</li>
# 			<li>
# 				<a href="#">
# 					<i class="fa fa-bar-chart-o fa-2x"></i>
# 					<span class="nav-text">
# 						Graphs and Statistics
# 					</span>
# 				</a>
# 			</li>
# 			<li>
# 				<a href="#">
# 					<i class="fa fa-font fa-2x"></i>
# 					<span class="nav-text">
# 						Typography and Icons
# 					</span>
# 				</a>
# 			</li>
# 			<li>
# 				<a href="#">
# 					<i class="fa fa-table fa-2x"></i>
# 					<span class="nav-text">
# 						Tables
# 					</span>
# 				</a>
# 			</li>
# 			<li>
# 				<a href="#">
# 					<i class="fa fa-map-marker fa-2x"></i>
# 					<span class="nav-text">
# 						Maps
# 					</span>
# 				</a>
# 			</li>
# 			<li>
# 				<a href="#">
# 					<i class="fa fa-info fa-2x"></i>
# 					<span class="nav-text">
# 						Documentation
# 					</span>
# 				</a>
# 			</li>
# 		</ul>

# 		<ul class="logout">
# 			<li>
# 				<a href="#">
# 						<i class="fa fa-power-off fa-2x"></i>
# 					<span class="nav-text">
# 						Logout
# 					</span>
# 				</a>
# 			</li>  
# 		</ul>
# 	</nav>
# """

# #
# app.index_string = """
# <!DOCTYPE html>
# <html>
#     <head>
#         {%metas%}
#         <title>{%title%}</title>
#         {%favicon%}
#         {%css%}
#     </head>
#     <body>
# """+nav_div+"""
# 			<div class="dash_content">
# 				<div>My Custom header</div>
# 				{%app_entry%}
# 				<footer>
# 					{%config%}
# 					{%scripts%}
# 					{%renderer%}
# 				</footer>
# 				<div>My Custom footer</div>
# 			</div>
# 		</div>
#     </body>
# </html>
# """

# ## main-page
# app.layout = html.Div([
#     dcc.Location(id='url', refresh=False),
#     html.Div(id='page-content')
# ])

# @app.callback(Output('page-content', 'children'), Input('url', 'pathname'))
# def display_page(pathname):
# 	if pathname == '/dash/':
# 			return layout_main
# 	elif pathname == '/dash/list':
# 			return layout_list
# 	elif pathname == '/dash/dashboard':
# 			return layout_list
# 	elif pathname == '/dash/upload':
# 			return layout_upload
# 	elif pathname == '/dash/apps/app1':
# 			return layout1
# 	elif pathname == '/dash/apps/app2':
# 			return layout2
# 	elif pathname == '/dash/apps/app3':
# 			return layout3
# 	elif pathname == '/dash/apps/app4':
# 			return layout4
# 	elif pathname == '/dash/apps/app5':
# 			return layout5	
# 	elif pathname == '/dash/store':
# 			return layout_store
# 	elif pathname == '/dash/apps/lifelog' or pathname == '/dash/lifelog' :
# 			return layout_lifelog	
# 	else:
# 		return '404'


# ## data tale

# #source
# df2 = pd.read_csv('https://gist.githubusercontent.com/chriddyp/c78bf172206ce24f77d6363a2d754b59/raw/c353e8ef842413cae56ae3920b8fd78468aa4cb2/usa-agricultural-exports-2011.csv')

# #table_1
# df3 = df2.iloc[:,1:].copy()
# table1=dash_table.DataTable(
#     id='table',
#     columns=[{"name": i, "id": i} for i in df3.columns],
#     data=df3.to_dict('records'),
# 	page_size=20,  # we have less data in this example, so setting to 20
# 	style_table={'height': 'auto', 'overflowY':'auto','width':'auto'}
#     )

# # table_2
# years = list(range(1940, 2021, 1))
# temp_high = [x / 20 for x in years]
# temp_low = [x - 20 for x in temp_high]
# df = pd.DataFrame({"Year": years, "TempHigh": temp_high, "TempLow": temp_low})

# slider = dcc.RangeSlider(
#     id="slider",
#     value=[df["Year"].min(), df["Year"].max()],
#     min=df["Year"].min(),
#     max=df["Year"].max(),
#     step=5,
#     marks={
#         1940: "1940",
#         1945: "1945",
#         1950: "1950",
#         1955: "1955",
#         1960: "1960",
#         1965: "1965",
#         1970: "1970",
#         1975: "1975",
#         1980: "1980",
#         1985: "1985",
#         1990: "1990",
#         1995: "1995",
#         2000: "2000",
#         2005: "2005",
#         2010: "2010",
#         2015: "2015",
#         2020: "2020",
#     },
# )

# # table_3
# def generate_table(dataframe, max_rows=10):
#     return html.Table([
#         html.Thead(
#             html.Tr([html.Th(col) for col in dataframe.columns])
#         ),
#         html.Tbody([
#             html.Tr([
#                 html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
#             ]) for i in range(min(len(dataframe), max_rows))
#         ])
#     ])



# ## components
# # component_1
# # accordion
# accordion = html.Div(
#     dbc.Accordion(
#         [
#             dbc.AccordionItem(
#                 [
#                     html.P("This is the content of the first section"),
#                     dbc.Button("Click here"),
#                 ],
#                 title="Item 1",
#             ),
#             dbc.AccordionItem(
#                 [
#                     html.P("This is the content of the second section"),
#                     dbc.Button("Don't click me!", color="danger"),
#                 ],
#                 title="Item 2",
#             ),
#             dbc.AccordionItem(
#                 "This is the content of the third section",
#                 title="Item 3",
#             ),
#         ],
#     )
# )


# ## lay_outs

# # layout_main
# layout_main = html.Div(children=[ html.H1('App 1')])


# # layout_list
# layout_list = html.Div(children=[ html.H1('App 1'),
# 	dcc.Dropdown(
#         id='app-1-dropdown',
#         options=[
#             {'label': 'App 1 - {}'.format(i), 'value': i} for i in [
#                 'BLUE', 'RED', 'GREEN'
#             ]
#         ]
#     ),
# 	html.Div(id='app-1-display-value'),
# 	html.Br(),
# 	dcc.Link('Go to App 1', href='/dash/apps/app1'),
# 	html.Br(),
# 	dcc.Link('Go to App 2', href='/dash/apps/app2'),
# 	html.Br(),
# 	dcc.Link('Go to App 3', href='/dash/apps/app3'),
# 	html.Br(),
# 	dcc.Link('Go to App 4', href='/dash/apps/app4'),
# 	html.Br(),
# 	dcc.Link('Go to App 5', href='/dash/apps/app5'),
# 	html.Br(),
# ])

# # layout_upload
# layout_upload = html.Div([
#     dcc.Upload(
#         id='upload-data',
#         children=html.Div([
#             'Drag and Drop or ',
#             html.A('Select Files')
#         ]),
#         style={
#             'width': '100%',
#             'height': '60px',
#             'lineHeight': '60px',
#             'borderWidth': '1px',
#             'borderStyle': 'dashed',
#             'borderRadius': '5px',
#             'textAlign': 'center',
#             'margin': '10px'
#         },
#         # Allow multiple files to be uploaded
#         multiple=True
#     ),
#     html.Div(id='output-data-upload'),
# ])


# # lay_out_1
# layout1 = html.Div([
#     html.H3('App 1'),
#     dcc.Dropdown(
#         id='app-1-dropdown',
#         options=[
#             {'label': 'App 1 - {}'.format(i), 'value': i} for i in [
#                 'BLUE', 'RED', 'GREEN'
#             ]
#         ]
#     ),
#     html.Div(id='app-1-display-value'),
#     dcc.Link('Go to App 1', href='/dash/apps/app1'),
# 	dcc.Link('Go to App 2', href='/dash/apps/app2'),
# 	dcc.Link('Go to App 3', href='/dash/apps/app3'),
# 	dcc.Link('Go to App 4', href='/dash/apps/app4'),
# 	dcc.Link('Go to App 5', href='/dash/apps/app5'),
# ])
# @app.callback(
#     Output('app-1-display-value', 'children'),
#     Input('app-1-dropdown', 'value'))
# def display_value(value):
#     return 'You have selected "{}"'.format(value)


# # lay_out_2
# layout2 = html.Div(
#     children=[
#         html.H1(children="Data Visualization with Dash"),
#         html.Div(children="High/Low Temperatures Over Time"),
#         dcc.Graph(id="temp-plot"),
#         slider,
#     ]
# )

# @app.callback(Output("temp-plot", "figure"), [Input("slider", "value")])
# def add_graph(slider):
#     print(type(slider))
#     trace_high = obj.Scatter(x=df["Year"], y=df["TempHigh"], mode="markers", name="High Temperatures")
#     trace_low = obj.Scatter(x=df["Year"], y=df["TempLow"], mode="markers", name="Low Temperatures")
#     layout = obj.Layout(xaxis=dict(range=[slider[0], slider[1]]), yaxis={"title": "Temperature"})
#     figure = obj.Figure(data=[trace_high, trace_low], layout=layout)
#     return figure

# # lay_out_3
# layout3 = html.Div([
#     html.H4(children='US Agriculture Exports (2011)'),
#     generate_table(df2)
# ])

# # lay_out_4
# markdown_text = f"""
# ### Intro
# Dash apps can be written in Markdown.
# Dash uses the [CommonMark](http://commonmark.org/)
# specification of Markdown.
# Check out their [60 Second Markdown Tutorial](http://commonmark.org/help/)
# if this is your first introduction to Markdown!
# """

# layout4 = html.Div(children=[
# 	html.Div(children=[
#     dcc.Markdown(children=markdown_text),
# 	accordion
# ],style={'margin':'10px','padding':'200px', 'border': '10px solid','border-radius':'10px', 'background': '#F5EEDC'})

# ],style={'padding':'10px'})

# # lay_out_5
# layout5 = html.Div(children=[table1], style={'margin':'10px','padding':'20px', 'border': '5px solid','border-radius':'10px', 'background': '#F5EEDC'}
# )





# ########### upload and download

# def save_file(name, content):
#     """Decode and store a file uploaded with Plotly Dash."""
#     data = content.encode("utf8").split(b";base64,")[1]
#     with open(os.path.join(UPLOAD_DIRECTORY, name), "wb") as fp:
#         fp.write(base64.decodebytes(data))

# def uploaded_files():
#     """List the files in the upload directory."""
#     files = []
#     for filename in os.listdir(UPLOAD_DIRECTORY):
#         path = os.path.join(UPLOAD_DIRECTORY, filename)
#         if os.path.isfile(path):
#             files.append(filename)
#     return files

# def file_download_link(filename):
#     """Create a Plotly Dash 'A' element that downloads a file from the app."""
#     location = "/download/{}".format(urlquote(filename))
#     return html.A(filename, href=location)

# layout_store = html.Div(
#     [
#         html.H1("File Browser"),
#         html.H2("Upload"),
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
#         html.H2("File List"),
#         html.Ul(id="file-list"),
#     ],
#     style={"max-width": "500px"},
# )
# @app.callback(
#     Output("file-list", "children"),
#     [Input("upload-data", "filename"), Input("upload-data", "contents")],
# )
# def update_output(uploaded_filenames, uploaded_file_contents):
#     """Save uploaded files and regenerate the file list."""

#     if uploaded_filenames is not None and uploaded_file_contents is not None:
#         for name, data in zip(uploaded_filenames, uploaded_file_contents):
#             save_file(name, data)

#     files = uploaded_files()
#     if len(files) == 0:
#         return [html.Li("No files yet!")]
#     else:
#         return [html.Li(file_download_link(filename)) for filename in files]