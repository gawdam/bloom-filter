import pandas as pd
import sys
import mmh3
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import os
from dash.exceptions import PreventUpdate

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.COSMO])
server = app.server
server.secret_key = os.environ.get('SECRET_KEY', 'my-secret-key')
m = 16
k = 2
# ---------------------------------------------------------------
bitarray = pd.DataFrame([0] * m).T

# ---------------------------------------------------------------

actual_dataframe = pd.DataFrame(columns=['Element', 'Hash values'])

# ---------------------------------------------------------------
app.layout = html.Div([
    html.Div([dbc.Row([
        html.Br(),
        dbc.Col(html.Div("Bloom Filter", id="title",
                         style={'text-align': 'center', 'font-size': '150%', "font-weight": 'bold'}), )]),
        html.Br(),
        dbc.Row([
            dbc.Col(
                dash_table.DataTable(
                    id='bitarray',
                    data=bitarray.to_dict('records'),
                    columns=[
                        {"name": str(i), "id": str(i), "type": 'numeric', 'deletable': False, "selectable": False} for i
                        in
                        bitarray.columns
                    ],
                    editable=False,
                    style_data_conditional=[],
                    row_deletable=False,
                    style_cell={'width': '5%', 'textAlign': 'center'}
                ), width={'size': 10, 'offset': 1})

        ], className='row-table'),
        html.Br(),
        dbc.Row([
            dbc.Col(
                dcc.Input(
                    id='input',
                    type='text',
                    placeholder="Insert number/word",
                    readOnly=False,
                    disabled=False,
                    debounce=False,
                    n_submit=0,
                    autoFocus=True,
                    value='',
                    style={'width': '100%%', 'text-align': 'left', 'border-radius': 4, 'font-family': 'Verdana'},

                ),
                width={'size': 3, 'offset': 1, 'text-align': 'center'}
            ),
            dbc.Col(
                html.Button(id='add-button', type='submit', n_clicks=0, n_clicks_timestamp=-1,
                            children="Add to bitarray",
                            style={'background-colour': 'white', "width": '100%',
                                   'border-radius': 4, 'font-family': 'Verdana'}),
                width={'size': 3}
            ),
        ]),
        html.Br(),

        dbc.Row([
            dbc.Col(
                dcc.Input(
                    id='input-check',
                    type='text',
                    placeholder="Insert number/word",
                    readOnly=False,
                    disabled=False,
                    debounce=False,
                    n_submit=0,
                    autoFocus=False,
                    value='',
                    style={'width': '100%%', 'text-align': 'left', 'horizontalAlign': 'left', 'border-radius': 4,
                           'font-family': 'Verdana'},

                ),
                width={'size': 3, 'offset': 1, 'text-align': 'center'}
            ),
            dbc.Col(
                html.Button(id='get-button', type='submit', n_clicks=0, children="Check",
                            style={"width": '100%',
                                   'horizontalAlign': 'left',
                                   'border-radius': 4, 'font-family': 'Verdana'}),
                width={'size': 3}
            ), ]),
        html.Br(),
        dbc.Row([
            dbc.Col(
                html.Div(id='Result',
                         style={'text-align': 'center', 'font-size': '150%', "font-weight": 'bold'}),
                width={'size':2,'offset':5}
            ),
        ]),
        html.Br(),
    ], style={"border": "2px brown solid", 'margin': '50px'}),

    # ------------------------------------------------------------------------------------------

    html.Div([
        html.Br(),
        dbc.Row([
            html.Br(),
            dbc.Col(html.Div("Elements Stored", id="title-2",
                             style={'text-align': 'center', 'font-size': '150%', "font-weight": 'bold'}),
                    ), ]),
        dbc.Row([
            dbc.Col(
                dash_table.DataTable(
                    id='elements-added',
                    data=actual_dataframe.to_dict('records'),
                    columns=[
                        {"name": str(i), "id": str(i), "type": 'text', 'deletable': False, "selectable": False} for i in
                        actual_dataframe.columns
                    ],
                    editable=False,
                    row_deletable=False,
                    style_cell={'width': '50%', 'textAlign': 'center'}
                ), width={'size': 4, 'offset': 4})

        ], className='row-table-2'),
        html.Br()
    ], style={"border": "2px brown solid", 'margin': '50px'}
    )
])


@app.callback(
    [Output(component_id='bitarray', component_property='data'),
     Output(component_id='elements-added', component_property='data'),
     Output(component_id='bitarray', component_property='style_data_conditional'),
     Output(component_id='input', component_property='n_submit'),
     Output(component_id='add-button', component_property='n_clicks'),
     Output(component_id='input', component_property='value')],
    [Input(component_id='bitarray', component_property='data'),
     Input(component_id='elements-added', component_property='data'),
     Input(component_id='add-button', component_property='n_clicks'),
     Input(component_id='input', component_property='n_submit')],
    [State(component_id='input', component_property='value')]
)
def update_output(bitarray, df_actual, num_submit, num_click, input_value):
    style_data_conditional = []
    hash_values = []
    if (num_submit and input_value) or num_click:
        # update records
        for i in range(k):
            index = mmh3.hash(input_value, i) % m
            hash_values.append(index)
            bitarray[0][str(index)] = 1
            style_data_conditional.append({
                'if': {
                    'row_index': 0,
                    'column_id': '{}'.format(index)
                },
                'color': 'tomato',
                'backgroundColor': '#DDDDDD',
                'fontWeight': 'bold'
            }, )

        df_actual = pd.DataFrame(df_actual, columns=['Element', 'Hash values'])
        if input_value in df_actual['Element'].values:
            pass
        else:
            df_actual = df_actual.append({'Element': input_value, 'Hash values': str(hash_values)}, ignore_index=True)
        print(df_actual)
        df_actual = df_actual.to_dict('records')

        return bitarray, df_actual, style_data_conditional, 0, 0, ''
    return bitarray, df_actual, style_data_conditional, num_submit, num_click, input_value


@app.callback(
    [Output(component_id='Result', component_property='children'),
     Output(component_id='input-check', component_property='n_submit'),
     Output(component_id='get-button', component_property='n_clicks')],
    [Input(component_id='bitarray', component_property='data'),
     Input(component_id='input-check', component_property='n_submit'),
     Input(component_id='get-button', component_property='n_clicks'),
     Input(component_id='input-check', component_property='value')],
    [State(component_id='input-check', component_property='value')]
)
def update_output(df, input_submit, button_submit, input_value_mock, input_value):
    if input_value_mock == '':
        return ["", button_submit, input_submit]
    if not (((input_submit and input_value) or button_submit) and input_value != ''):
        PreventUpdate
    else:
        button_submit = 0
        input_submit = 0
        for i in range(k):
            index = mmh3.hash(input_value, i) % m
            if df[0][str(index)] == 0:
                return ["Not Present!!", button_submit, input_submit]
        return ["Present!!", button_submit, input_submit]
    return ["", button_submit, input_submit]


# ------------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=True)
