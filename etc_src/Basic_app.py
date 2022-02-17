
# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.


import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from flask import Flask, render_template

sever=Flask()
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H6("Change the value in the text box to see callbacks in action!"),
    html.Div([
        "Input: ",
        dcc.Input(id='my-input', value='initial value', type='text')
    ]),
    html.Br(),
    html.Br(),html.Br(),html.Br(),html.Br(),
    html.Div(id='my-output'),
])

@sever.route('/home')
def index():
    return render_template('index.html')

## 콜백 데코테이터를 생성하면  아래의 함수를 이용하게됨.   컴포넌트 타겟을 id로 지정후 해당 타겟해서 새로운 밸류가 들어오면 call_back 함수가 일어남 
@app.callback( Output(component_id='my-output', component_property='children'), Input(component_id='my-input', component_property='value') )
def a(input_value):
    return 'Output: {}'.format(input_value+"intput")

if __name__ == '__main__':
    app.run_server(debug=True)

