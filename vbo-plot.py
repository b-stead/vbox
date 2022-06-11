# Run this app with `python3 vbo-plot.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, dcc, html, Input, Output, State, dash_table
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc
import pandas as pd
import json

df = pd.read_csv('DA500.csv')
external_stylesheets = [dbc.themes.DARKLY] # enables dark mode in plot using bootstrap
app = Dash(__name__)
fig = go.Figure()

fig.add_trace(go.Scatter(x=df['distance'], y=df['speed'],
                mode='lines+markers',
                name='speed'))
colors = {
    'background': '#171717',
    'text': '#FFFFFF'
}
styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll', 'display':'inline-block', 'width': '49%'
    }
}
bins = [0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500]
aggfuncs = ['mean', 'max']
col_names = ['var', '0', '50', '100', '150', '200', '250', '300', '350', '400', '450', '500']
df = df[['distance', 'speed', 'strokerate', 'split_d']]
df.loc[:, 'splits']=pd.cut(df['distance'], bins) #create new column 'splits' indexing all rows for Distance grtouped into the bins
dff=df.groupby('splits')[['speed', 'strokerate']].agg(aggfuncs)
dff=dff.round(1)
dff_t=dff.T
dff_t =dff_t.reset_index()
dff_t.columns = col_names

def generate_table(dff_t, max_rows=5):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dff_t.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dff_t.iloc[i][col]) for col in dff_t.columns
            ]) for i in range(min(len(dff_t),max_rows))
        ])
    
    ])

app.layout = html.Div([
    html.Div([

        html.Div([
            html.Div([
                html.Label('Distance Selection'),]),

            dcc.Dropdown(
                id='distance-selection',
                options=[
                    {'label': '250m', 'value': 250},
                    {'label': '500m', 'value': 500},
                ],
                value=500,
                clearable=False

            )], style={'width': '15%', 'display': 'inline-block'}

        ),

        html.Div([
            html.Div([
                html.Label("Select SR Y-axis:"),], style={'float': 'right','font-size': '18px', 'width': '40%'}),

            html.Div([
                dcc.RadioItems(
                    id='radio',
                    options=['Primary', 'Secondary'],
                    value='Secondary',
                    labelStyle={'float': 'right', 'margin-right': 10}
            ),
        ], style={'width': '49%', 'float': 'right'}),
        ], 
    )]),

    html.Div([
        dcc.Graph(
            id="graph", figure = fig           
        ), 
        dcc.Store(
            id='store-value',
        )
    ], style={'width': '100%', 'height':'100%', 'display': 'inline-block', 'padding': '0 20'}),
    html.Div([
        html.Div([
            html.H4(children='vbo-plot Session Data'),
            html.Div(children=[dash_table.DataTable(id='split-table')
            ]),
            generate_table(dff_t,max_rows=5),
            html.Pre(id='selection-data', style=styles['pre']),            
            dcc.Markdown("""
                **Click Data**
                Selection Data
                Click on start point on the speed curve.
            """),
        ],)
    ]),

], style={'backgroundColor': 'white'},
)
#get stored data for checking
@app.callback(
    Output('selection-data', 'children'),
    #Output('store-value', 'data'),
    Input('graph', 'selectedData'))
def display_click_data(selectedData):
    return json.dumps(selectedData, indent=2)

#update fig on selection data   
@app.callback(
    Output('graph', 'figure'),
    Input('graph', 'relayoutData'),
    State('graph', 'figure'),
    prevent_initial_call=True)
def update_graph(relOut, fig):
    if "xaxis.range[0]" not in relOut:
        return fig
    xmin = relOut["xaxis.range[0]"]
    xmax = relOut["xaxis.range[1]"]
    dff = df[df['distance'].between(xmin, xmax)]
    dff['distance']=dff.split_d.cumsum()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dff['distance'], y=dff['speed'],
                mode='lines+markers',
                name='speed'))
    #create secondary axis for stroke rate

    newLayout = go.Layout(
        title="updated-now",
        xaxis_range=[dff['distance'].min(), dff['distance'].max()],
        yaxis_range=[dff['speed'].min(), dff['speed'].max()],
    )
    fig['layout'] = newLayout
    return fig

#table callback with new split data
"""
@app.callback(
     Output('split-table', 'data'),
     Input('graph', 'relayoutData'),
)   
def update_table(relOut, dff):
    if "xaxis.range[0]" not in relOut:
        return generate_table()
    xmin = relOut["xaxis.range[0]"]
    xmax = relOut["xaxis.range[1]"]
    dff = df[df['distance'].between(xmin, xmax)]
    dff.loc[:, 'splits']=pd.cut(dff['distance'], bins)
    dff=df.groupby('splits')[['speed', 'strokerate']].agg(aggfuncs)
    dff=dff.round(1)
    dff['distance']=dff.split_d.cumsum() 
    dff_t=dff.T
    dff_t =dff_t.reset_index()
    dff_t.columns = col_names
    return generate_table(dff_t, max_rows=5)
"""

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
