import pandas as pd     #(version 0.24.2)
import math
import dash             #(version 1.0.0)
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import numpy as np
import plotly.io as pio
import chart_studio
import chart_studio.plotly as py

username = "Gowdamn"
api_key = "GUrcvT3BxNuabS7JdcZz"
chart_studio.tools.set_credentials_file(username=username, api_key=api_key)
array_size_max = 200

app = dash.Dash(__name__)
server = app.server

#---------------------------------------------------------------
app.layout = html.Div([
        html.Div([
            html.Pre(children= "Bloom Filter",
            style={"text-align": "center", "font-size":"300%", "color":"black"})
        ]),
        html.Div([
            html.Pre(children= "Probability of False Positives",
            style={"text-align": "center", "font-size":"200%", "color":"black"})
        ]),

        html.Div([
            dcc.Graph(id='the_graph')
        ]),
        html.Div([
            html.Pre(children= "Number of Hash Functions 'k':",
            style={"text-align": "left", "font-size":"200%", "color":"black"})
        ]),
        html.Div([
            dcc.Slider(
                id='k-slider',
                min=1,
                max=20,
                marks={i: '{}'.format(i) for i in range(20)},
                step=1,
                value=10,
            ),
            html.Div(id='slider-output-container-k')]
        ),
        html.Div([
            html.Pre(children="Size of Bitarray 'm':",
                     style={"text-align": "left", "font-size": "200%", "color": "black"})
        ]),
        html.Div([
        dcc.Slider(
                id='m-slider',
                min=1,
                max=20,
                marks={i: '{}'.format(50*i) for i in range(20)},
                step=50,
                value=15,
                updatemode='drag',
            ),
            html.Div(id='slider-output-container-m')]
        ),


])
#---------------------------------------------------------------
@app.callback(
    Output('the_graph','figure'),
    [Input('k-slider','value'), Input('m-slider','value')]
)

def update_graph(k,m):
     # print(k)
    # print(m)
    # print (dff[:3])
    m = m*50

    t = np.arange(1, array_size_max, 1)
    x=t
    y = [(1 - math.exp(-k*1.0 / (m*1.0 / x*1.0)))**k for x in t]
    data = {'Input array size':x,
            'Probability': y}
    print(len(x),len(y))

    df = pd.DataFrame(data)
    scatterplot = px.line(df, x="Input array size",
        y="Probability",
        hover_data=['Probability'],range_y=[0,1],
        height=550
    )

    scatterplot.update_traces(textposition='top center')
    pio.write_html(scatterplot, file='index.html', auto_open = False)
    return (scatterplot)

if __name__ == '__main__':
    app.run_server(debug=True)
