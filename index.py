from fastapi import FastAPI
from fastapi import BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from fastapi.responses import FileResponse

from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.middleware.wsgi import WSGIMiddleware

from pydantic import EmailStr, BaseModel
from typing import List, Dict, Any

from dash import dcc
from dash import html
from dash.dependencies import Input, Output

import os

from app import app
from apps import layout_main, layout_list , layout_store , layout_index_string, layout_table, layout_table_header , layout_annotation, layout_lifelog



################
## static_dir ##
################

UPLOAD_DIRECTORY = "uploads/app_uploaded_files"
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)



############
## server ##
############


namu=FastAPI()

namu.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="static/templates")

# app.server  from app.py    Dash
namu.mount("/dash", WSGIMiddleware(app.server),name="dash")



###########
## router##
###########

@namu.get("/")
async def root():
    return {"message" :  "Hello World"}

@namu.get("/items/{item_id:int}")
async def read_item(item_id):
    return {"item_id":item_id}

@namu.get("/path/{item_id:path}/miniconda3/{filename}")
async def read_path(item_id:str, filename:str):
    return {"item_id":item_id,"filename":filename}

@namu.get("/template/items/{id}", response_class=HTMLResponse)
async def read_template(request: Request, id: str):
    return templates.TemplateResponse("item.html", {"request": request, "id": id})

@namu.get("/index", response_class=HTMLResponse)
async def read_template(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@namu.get("/login", response_class=HTMLResponse)
async def read_template(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@namu.get("/cat", response_class=HTMLResponse)
async def read_template(request: Request):
    return templates.TemplateResponse("cat.html", {"request": request})

@namu.get("/download/{path:path}")
def download(path:str):
	"""Serve a file from the upload directory."""
	return FileResponse(path=UPLOAD_DIRECTORY+'/'+path, filename=path, media_type='text/mp4')


###########
## E-Mail##
###########

class EmailSchema(BaseModel):
	email: List[EmailStr]
	body: Dict[str, Any]

conf = ConnectionConfig(
	MAIL_USERNAME='hdshin@namuintelligence.com',
	MAIL_PASSWORD="namu02110hd!!",
	MAIL_FROM = "hdshin@namuintelligence.com",
	MAIL_PORT=587,
	MAIL_SERVER="smtp.gmail.com",
	MAIL_TLS=True,
	MAIL_SSL=False,
	USE_CREDENTIALS = True,
	VALIDATE_CERTS = True,
	TEMPLATE_FOLDER ='static/templates'
)

# html = """
# <p>Hi this test mail, thanks for using Fastapi-mail</p> 
# """
async def send_email_async(subject: str, email_to: str, body: dict):
	message = MessageSchema(
			subject=subject,
			recipients=[email_to],
			template_body=body,
			subtype='html',
	)
	fm = FastMail(conf)
	await fm.send_message(message, template_name='email.html')

def send_email_background(background_tasks: BackgroundTasks, subject: str, email_to: str, body: dict):
	print(email_to,'=====================')
	message = MessageSchema(
			subject=subject,
			recipients=[email_to],
			template_body=body,
			subtype='html',
	)
	fm = FastMail(conf)
	background_tasks.add_task(
		fm.send_message, message, template_name='email.html')

# POST- > 웹에서  단순 접근으로 확인하려고하면 405 에러가 뜨게됨 post 전용 페이지이기 때문
@namu.get('/send-email/asynchronous')
async def send_email_asynchronous():
    await send_email_async('Hello World','chesyuyu@gmail.com', body={'title': 'Hello World', 'name': 'Shin heeda'})
    return JSONResponse(status_code=200, content={"message": "email has been sent"})

@namu.get('/send-email/backgroundtasks')
def send_email_backgroundtasks(background_tasks: BackgroundTasks):
    send_email_background(background_tasks, 'Hello World',   
    'chesyuyu@gmail.com', body={'title': 'Hello World', 'name':  'Shin heeda'})
    return JSONResponse(status_code=200, content={"message": "email has been sent"})


@namu.get('/e-mail/namu/{email_to}')
def send_email_backgroundtasks(background_tasks: BackgroundTasks, email_to:str):
    send_email_background(background_tasks, 'Hello World', email_to=email_to, body={'title': 'Hello World', 'name':  'Shin heeda'})
    return JSONResponse(status_code=200, content={"message": "email has been sent"})


##########
## dash ##
##########

app.index_string = layout_index_string.index_string

## main-page

app.layout = html.Div(children=[
    dcc.Location(id='url', refresh=False),
	html.Div(children=[
    	html.Div(id='page-content')
	],
	style={'padding':'25px'})
])

@app.callback(Output('page-content', 'children'), Input('url', 'pathname'))
def display_page(pathname):
	if pathname == '/dash/':
			return layout_main.layout_main
	elif pathname == '/dash/list':
			return layout_list.layout_list
	elif pathname == '/dash/dashboard':
			return layout_list.layout_list
	elif pathname == '/dash/apps/table_header':
			return layout_table_header.table_header
	elif pathname == '/dash/apps/table':
			return layout_table.layout_table
	elif pathname == '/dash/apps/image_annotation':
			return layout_annotation.layout_annotation
	elif pathname == '/dash/store':
			return layout_store.layout_store
	elif pathname == '/dash/apps/lifelog':
			return layout_lifelog.layout_table
	# elif pathname == '/dash/apps/test' or pathname == '/dash/test' :
	# 		return test	
	else:
		return '404'

