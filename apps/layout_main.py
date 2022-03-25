
from dash import dcc
from dash import html

from dash.dependencies import Input, Output
from markdown import markdown
from app import app


markdown="""
## 수행과제 : 감각기계-난청환자 어음 검사 데이터              
"""
layout_main = \
html.Div(
  children=[ 
            dcc.Markdown(children=markdown)
          ]

)
