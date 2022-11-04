import dash
from dash.exceptions import PreventUpdate
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# create a layout with two multi-select dropdowns
def get_dropdown(n, value=None):
    value = [] if value is None else value
    return html.Div(
        [dcc.Dropdown(
            id='dropdown'+n,
            options=[
                {'label': 'New York City', 'value': 'NYC'},
                {'label': 'Montréal', 'value': 'MTL'},
                {'label': 'San Francisco', 'value': 'SF'}
            ],
            multi=True,
            value=value
        )],
        id='dropdown-container'+n,

    )
app.layout = html.Div([
    get_dropdown('1'),
    get_dropdown('2'),
    html.Div([], id='previously-selected', style={'display': 'none'})
])


# Callback one recreates the other dropdown using new values
#   and updates the previously-selected value
@app.callback(
    [Output('dropdown-container2', 'children'), Output('previously-selected', 'children')],
    [Input('dropdown1', 'value')],
    [State('previously-selected', 'children')]
)
def update_via_children(value, prev_selected):
    print('callback one')

    if sorted(value) == sorted(prev_selected):
        raise PreventUpdate

    return get_dropdown('2', value=value), value

# Callback two updates the value of dropdown1 directly and so could be used to alter something
#   complicated like a Graph, hopefully. Does not update previously-selected, so callback one
#   will be called again, recreating dropdown2, triggering callback one a second time, but
#   this time previously-selected == value
@app.callback(
    Output('dropdown1', 'value'),
    [Input('dropdown2', 'value')],
    [State('previously-selected', 'children')]
)
def update_directly(value, prev_selected):
    print('callback two')
    if sorted(value) == sorted(prev_selected):
        raise PreventUpdate
    return value


app.run_server(debug=True, use_reloader=False)