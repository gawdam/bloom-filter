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
                         style={"text-align": "center", "font-size": "150%",
                                "color": "black","font-weight":'bold'})
                , width={'size': 12, 'offset': 0}
                )),
    html.Br(),
    html.Br(),

    dbc.Row([
        dbc.Col(
            html.Label('Choose plot:',
                       style={"width": "100%", "text-align": "left", "font-size": "95%", "color": "black",'padding-left':'7%','font-family': 'Verdana'}),
            width={'size': 4, 'offset': 0}
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
            width={'size': 3, 'offset': 0}
        ),
    ], align='center'),
    html.Br(),
    dbc.Row([
        dbc.Col(
            html.Pre(id="slider-1-name",
                     children="Number of Hash Functions 'k':",
                     style={"width": "100%", "text-align": "left", "font-size": "95%", "color": "black",
                            "font-family": "Verdana",'padding-left':'7%'})
            ,
            width={'size': 4, 'offset': 0},
        ),

        dbc.Col([
            dcc.Slider(
                id='slider-1',
            ),
            html.Div(id='slider-output-container-1')],
            style={'text-align': 'left', 'width': '100%', 'padding-left': '0%', 'padding-right': '5%'},
            width={'size': 8, 'offset': 0}
        )]),
    dbc.Row([
        dbc.Col(
            html.Pre(id="slider-2-name",
                     children="Size of Bitarray 'm':",
                     style={"width": "100%", "text-align": "left", "font-size": "95%", "color": "black",
                            "font-family": "Verdana",'padding-left':'7%'})
            ,
            width={'size': 4, 'offset': 0}
        ),

        dbc.Col([
            dcc.Slider(
                id='slider-2',
                updatemode='drag',
            ),
            html.Div(id='slider-output-container-2')],
            style={'width': '100%', 'padding-left': '0%', 'padding-right': '5%'},
            width={'size': 8, 'offset': 0}
        ),
    ]),
    html.Div([
        dcc.Graph(id='the_graph')
    ])

], className='select_box')


# ---------------------------------------------------------------
@app.callback(
    [
        Output('slider-1', 'min'),
        Output('slider-1', 'max'),
        Output('slider-1', 'marks'),
        Output('slider-1', 'step'),
        Output('slider-1', 'value'),
        Output('slider-1-name', 'children'),
    ],
    Input('plot-dropdown', 'value')
)
def update_graph(choice):
    minimum = 1
    maximum = 20
    marks = {2*i: '{}'.format(2*i) for i in range(10)}
    step = 1
    value = 10
    title = "Number of Hash Functions 'k':"
    # update slider to hold k
    if choice == 2:
        minimum = 1
        maximum = 20
        marks = {2*i: '{}'.format(20 * i) for i in range(10)}
        step = 10
        value = 10
        title = "Number of Input Elements 'n':"
        pass
        # update slider to hold n
    return minimum, maximum, marks, step, value, title


# ---------------------------------------------------------------
@app.callback(
    [
        Output('slider-2', 'min'),
        Output('slider-2', 'max'),
        Output('slider-2', 'marks'),
        Output('slider-2', 'step'),
        Output('slider-2', 'value'),
        Output('slider-2-name', 'children'),
    ],
    Input('plot-dropdown', 'value')
)
def update_graph(choice):
    minimum = 1
    maximum = 20
    marks = {2*i: '{}'.format(100 * i) for i in range(10)}
    step = 1
    value = 15
    title = "Size of Bitarray 'm':"
    # update slider to hold m
    if choice == 3:
        minimum = 1
        maximum = 20
        marks = {2*i: '{}'.format(20 * i) for i in range(10)}
        step = 1
        value = 10
        title = "Number of Input Elements 'n':"
        pass
    return minimum, maximum, marks, step, value, title


# ---------------------------------------------------------------
@app.callback(
    Output('the_graph', 'figure'),
    [Input('plot-dropdown', 'value'), Input('slider-1', 'value'), Input('slider-2', 'value')]
)
def update_graph(choice, v1, v2):
    k = v1
    m = v2 * 50
    n = np.arange(1, 200, 1)
    x = n
    y = [(1 - math.exp(-k * 1.0 / (m * 1.0 / x * 1.0))) ** k for x in n]
    title = 'Input array size'
    if choice == 2:
        k = np.arange(1, 50, 1)
        m = v2 * 50
        n = v1 * 10
        x = k
        y = [(1 - math.exp(-x * 1.0 / (m * 1.0 / n * 1.0))) ** x for x in k]
        title = 'Number of hash functions'

    elif choice == 3:
        k = v1
        m = np.arange(1, 1000, 5)
        n = v2 * 10
        x = m
        title = "Bitarray Size"
        y = [(1 - math.exp(-k * 1.0 / (x * 1.0 / n * 1.0))) ** k for x in m]

    data = {title: x,
            'Probability': y}
    df = pd.DataFrame(data)
    scatterplot = px.line(df, x=title,
                          y="Probability",
                          hover_data=['Probability'], range_y=[0, 1],
                          height=550
                          )

    scatterplot.update_traces(textposition='top center')
    pio.write_html(scatterplot, file='index.html', auto_open=False)
    return scatterplot


if __name__ == '__main__':
    app.run_server(debug=True)
