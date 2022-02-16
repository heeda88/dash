
import dash
import plotly.express as px

from dash import dcc
from dash import html

from dash.dependencies import Input, Output
from app import app

from skimage import data
import json

img = data.chelsea()
fig = px.imshow(img)
fig.update_layout(dragmode="drawrect")

config = {
    "modeBarButtonsToAdd": [
        "drawline",
        "drawopenpath",
        "drawclosedpath",
        "drawcircle",
        "drawrect",
        "eraseshape",
    ]
}

layout_annotation = html.Div(
    [
        html.H3("Drag and draw rectangle annotations"),
        dcc.Graph(id="graph-picture", figure=fig, config=config),
        dcc.Markdown("Characteristics of shapes"),
        html.Pre(id="annotations-data"),
    ]
)

@app.callback(
    Output("annotations-data", "children"),
    Input("graph-picture", "relayoutData"),
    prevent_initial_call=True,
)
def on_new_annotation(relayout_data):
    if "shapes" in relayout_data:
        return json.dumps(relayout_data["shapes"], indent=2)
    else:
        return dash.no_update

if __name__ == "__main__":
    app.run_server(debug=True)