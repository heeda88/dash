import dash
import dash_bootstrap_components as dbc


# call back을 모두 호출함 
app = dash.Dash(__name__, requests_pathname_prefix="/dash/", external_stylesheets=[dbc.themes.SLATE], suppress_callback_exceptions=True )
app.enable_dev_tools(debug=True)