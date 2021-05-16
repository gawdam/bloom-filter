import pandas as pd  # (version 0.24.2)
import math
import dash  # (version 1.0.0)
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
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

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.COSMO])
server = app.server

# ---------------------------------------------------------------
app.layout = html.Div([
    html.Br(),
    dbc.Row(

        dbc.Col(html.Div("Bloom Filter - Probability of False Positives",
                         style={"text-align": "center", "font-size": "40px",
                                "color": "black"})
                , width={'size': 12, 'offset': 0}
                )),
    html.Br(),
    html.Br(),
    dbc.Row([
        dbc.Col(
            html.Label('Choose plot:',
                       style={"width": "100%", "text-align": "right", "font-size": "15px", "color": "black"}),
            width={'size': 1, 'offset': 0}
        ),
        dbc.Col(
            dcc.Dropdown(id='plot-dropdown',
                         options=[
                             {'label': 'p-n', 'value': 1},
                             {'label': 'p-k', 'value': 2},
                             {'label': 'p-m', 'value': 3}
                         ],
                         optionHeight=35,  # height/space between dropdown options
                         value=1,  # dropdown value selected automatically when page loads
                         disabled=False,  # disable dropdown value selection
                         multi=False,  # allow multiple dropdown values to be selected
                         searchable=True,  # allow user-searching of dropdown values
                         search_value='',  # remembers the value searched in dropdown
                         placeholder='p-n',  # gray, default text shown when no option is selected
                         clearable=False,  # allow user to removes the selected value
                         style={'width': "100%", 'font-family': 'Verdana', "text-align": "left"},
                         ),
            width={'size': 1, 'offset': 0}
        ),

        dbc.Col(
            html.Pre(children="Number of Hash Functions 'k':",
                     style={"width": "100%", "text-align": "left", "font-size": "20px", "color": "black",
                            "font-family": "Verdana"}),
            width={'size': 4, 'offset': 1},
        ),
        dbc.Col(
            html.Pre(children="Size of Bitarray 'm':",
                     style={"width": "100%", "text-align": "left", "font-size": "20px", "color": "black",
                            "font-family": "Verdana"}),
            width={'size': 5, 'offset': 0}
        )
    ], align='center'),

    dbc.Row([
        dbc.Col([
            dcc.Slider(
                id='k-slider',
                min=1,
                max=20,
                marks={i: '{}'.format(i) for i in range(20)},
                step=1,
                value=10,
            ),
            html.Div(id='slider-output-container-k')],
            style={'text-align': 'left', 'width': '100%', 'padding-left': '0%', 'padding-right': '0%'},
            width={'size': 4, 'offset': 3}
        ),
        dbc.Col([
            dcc.Slider(
                id='m-slider',
                min=1,
                max=20,
                marks={i: '{}'.format(50 * i) for i in range(20)},
                step=50,
                value=15,
                updatemode='drag',
            ),
            html.Div(id='slider-output-container-m')],
            style={'width': '100%', 'padding-left': '0%', 'padding-right': '0%'},
            width={'size': 5, 'offset': 0}
        ),
    ]),
    html.Div([
        dcc.Graph(id='the_graph')
    ])

], className='select_box')


# ---------------------------------------------------------------
@app.callback(
    Output('the_graph', 'figure'),
    [Input('plot-dropdown', 'value'), Input('k-slider', 'value'), Input('m-slider', 'value')]
)
def update_graph(choice, k, m):
    m = m * 50

    t = np.arange(1, array_size_max, 1)
    x = t
    y = [(1 - math.exp(-k * 1.0 / (m * 1.0 / x * 1.0))) ** k for x in t]
    data = {'Input array size': x,
            'Probability': y}
    print(len(x), len(y))

    df = pd.DataFrame(data)
    scatterplot = px.line(df, x="Input array size",
                          y="Probability",
                          hover_data=['Probability'], range_y=[0, 1],
                          height=550
                          )

    scatterplot.update_traces(textposition='top center')
    pio.write_html(scatterplot, file='index.html', auto_open=False)
    return scatterplot


if __name__ == '__main__':
    app.run_server(debug=True)
