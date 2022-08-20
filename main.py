import dash
import dash_html_components as html
from dash.dependencies import Input, Output
from dash_canvas import DashCanvas
import dash_core_components as dcc
from dash import Dash, html, Input, Output, ctx

import json

FEATURES = {"a" : [[95.99, 136.63999771118165, 262.99, 223.65999771118163, 95.99, 87.64999771118164, 422, 223.65999771118163],
[268, 215.63999771118165, 157.99, 439.65999771118163, 157.99, 215.63999771118165, 268, 439.65999771118163]]}

def extract_features(canvas_svg):
    objects = canvas_svg['objects']

    paths = [o for o in objects if o['type'] == 'path']

    features_all_strokes = []
    for stroke in paths:
        x = [point[1] for point in stroke['path']]
        y = [point[2] for point in stroke['path']]

        features_this_stroke = [x[0], y[0], x[-1], y[-1], min(x), min(y), max(x), max(y)]
        features_all_strokes.append(features_this_stroke)

    return features_all_strokes

import numpy as np
def compare_features(f1, f2):
    if len(f1) != len(f2):
        return -1 # incorrect number of strokes
    return np.linalg.norm(np.asarray(f1)-np.asarray(f2))


app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Store(id="state"),
    html.H5('Write the katakana for A', id="blah"),
html.Div(
    [html.Img(id="img", src=None),
     html.Br(),
     html.Button(["Done"],id="btn_seen")],
    id="div_gif"
),

    html.Div(
    DashCanvas(id='canvas_101',
               hide_buttons=["zoom", "pan",  # "line", "pencil",
                             "rectangle", "select", "save"],
               width=500,
               height=500,
            #  filename="assets/character_background_faint.drawio.png",
               # from  https://upload.wikimedia.org/wikipedia/commons/9/91/Japanese_Katakana_A.svg
            filename="assets/output.svg",
# filename="assets/a.gif",
               # json_data="""{"objects":[{"type":"image","originX":"left","originY":"top","left":0,"top":0,"width":236,"height":236,"fill":"rgb(0,0,0)","stroke":null,"strokeWidth":0,"strokeDashArray":null,"strokeLineCap":"butt","strokeLineJoin":"miter","strokeMiterLimit":10,"scaleX":2.12,"scaleY":2.12,"angle":0,"flipX":false,"flipY":false,"opacity":1,"shadow":null,"visible":true,"clipTo":null,"backgroundColor":"","fillRule":"nonzero","globalCompositeOperation":"source-over","transformMatrix":null,"skewX":0,"skewY":0,"crossOrigin":"","alignX":"none","alignY":"none","meetOrSlice":"meet","src":"http://localhost:8050/assets/character_background_faint.drawio.png","filters":[],"resizeFilters":[]},{"type":"line","originX":"center","originY":"center","left":262,"top":147.65,"width":228,"height":4,"fill":"red","stroke":"red","strokeWidth":10,"strokeDashArray":null,"strokeLineCap":"butt","strokeLineJoin":"miter","strokeMiterLimit":10,"scaleX":1,"scaleY":1,"angle":0,"flipX":false,"flipY":false,"opacity":1,"shadow":null,"visible":true,"clipTo":null,"backgroundColor":"","fillRule":"nonzero","globalCompositeOperation":"source-over","transformMatrix":null,"skewX":0,"skewY":0,"x1":-114,"x2":114,"y1":2,"y2":-2}]}"""
               ),
        # style={"display":"none"},
        id="div_canvas"
    ),

    html.H5('debug', id="debug"),
])



@app.callback([Output("div_canvas", "style"),
               Output("div_gif", "style"),
               Output("img", "src"),
               Output("canvas_101", "filename")
               ],
              [Input("state", "data")])
def update_state(state):
    print ("state", state)
    if state == 0:
        return [{"display": "inline"}, {"display": "none"}, None, "assets/output.svg",]
    else:
        return [{"display":"none"}, {"display":"inline"}, "assets/a.gif", None]




@app.callback([Output('state', 'data')],
              [Input('canvas_101', 'json_data'),
               Input("btn_seen", "n_clicks")])
def user_drew_line(string, n_clicks):
    print ("TI", ctx.triggered_id)
    if ctx.triggered_id == "canvas_101":

        parsed = json.loads(string)

        features = extract_features(parsed)

        score = compare_features(FEATURES["a"], features)
        if score >= 0 and score < 200:
            verdict = "CORRECT"
        else:
            verdict = "WRONG"

        # verdict = ""
        # if len(paths) != 2:
        #     verdict = "WRONG NUMBER OF STROKES"
        # else:
        #     stroke1 = paths[0]
        #     start = stroke1['path'][0]
        #     end = stroke1['path'][-1]
        #
        #     print ("start", start)
        #     print("end", end)
        #
        #     if start[1] < 250 and start[2] < 250 and end[1] > 250 and end[2] < 250:
        #         verdict = "YES"

            # TODO: extract features (start, end, bounding box)
            # TODO: find SVGs and convert them to features

        print (string)

        print (verdict)
        print (score)

        return [1]

        # return [verdict + " " + str(score)]

    else:
        return [0]



if __name__ == '__main__':
    app.run_server(debug=True)
