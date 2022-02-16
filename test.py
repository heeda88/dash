from turtle import title
from fastapi import FastAPI
from fastapi import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from starlette.requests import Request
from starlette.responses import JSONResponse
from pydantic import EmailStr, BaseModel
from typing import List, Dict, Any
from fastapi_mail.email_utils import DefaultChecker

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
##############
## 기본 구동##
#############
# 해당변수에 Fast API class instance 주소값 저장
namu=FastAPI()

namu.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="static/templates")

class NamuSchema():
    email='chesyuyu@gamil.com'
    title='lolen'
    name='heeda'

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

@namu.get("/email")
async def send_with_template() -> JSONResponse:
    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=['chesyuyu@gmail.com'],  # List of recipients, as many as you can pass 
        template_body={'title': 'Hello World', 'name':  'John Doe'},
        subtype="html"
        )
    fm = FastMail(conf)
    await fm.send_message(message, template_name="email.html") 
    return JSONResponse(status_code=200, content={"message": "email has been sent"})