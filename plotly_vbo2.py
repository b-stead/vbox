# Run this app with `python plotly_vbo2.py` and
# visit http://127.0.0.1:8051/ in your web browser.
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc
import pandas as pd
import json

df = pd.read_csv('DA500.csv')
external_stylesheets = [dbc.themes.DARKLY] # enables dark mode in plot using bootstrap
app = Dash(__name__)

#features we will need for callbacks
#effort_length = [50, 75, 150, 200, 250, 300, 400, 500]

colors = {
    'background': '#111111',
    'text': '#FFFFFF'
}
styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

"""
def generate_table(dff_t, max_rows=5):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dff_t.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dff_t.iloc[i][col]) for col in dff_t.columns
            ]) for i in range(min(len(dff_t), max_rows))
        ])
    
    ])
"""
layoutS = go.Layout(
    title="Meter",
    xaxis=dict(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(count=5, label="5y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    ),
    yaxis=dict(range=[0,2])
)

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
            id="graph", figure=dict(layout=layoutS)
            
        ), 
        dcc.Store(
            id='store-value',
        )
    ], style={'width': '100%', 'height':'100%', 'display': 'inline-block', 'padding': '0 20'}),
    html.Div([
            dcc.Markdown("""
                **Click Data**

                Click on points in the graph.
            """),
            html.Pre(id='click-data', style=styles['pre']),
        ], className='three columns'),
    #html.Div([
        #generate_table(dff_t),
    #],style={'display': 'inline-block', 'width': '100%',}),

    ], #style={'backgroundColor': 'rgb(17, 17, 17)'},
)

@app.callback(
    Output('click-data', 'children'),
    Output('store-value', 'data'),
    Input('graph', 'clickData'))
def display_click_data(clickData):
    return json.dumps(clickData, indent=2)

@app.callback(
    Output("graph", "figure"), 
    Input("radio", "value"))
def display_(radio_value):
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # add traces
    fig.add_trace(
        go.Scatter(x=df["Distance"], y=df["Speed"], name= "Speed (Kph)"),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=df["Distance"], y=df["StrokeRate"], mode='lines+markers',
        connectgaps= True, name= "Stroke Rate", line=dict(width=1.5,color='orange'),marker=dict(size=2, opacity=0.5)),
        secondary_y=radio_value == 'Secondary',
    )

    # Add figure title
    fig.update_layout(
        xaxis = dict(
            tickmode = 'linear',
            tick0 = 0,
            dtick = 50
        ),
    )

    # Set x-axis title
    fig.update_xaxes(
        rangemode="nonnegative",
        title_text="Distance",
        showgrid= True)

     # Set y-axes titles
    fig.update_yaxes(
        rangemode="nonnegative",
        title_text="<b>Speed</b>", 
        secondary_y=False,
        showgrid= True)
    fig.update_yaxes(
        rangemode="nonnegative", 
        title_text="<b>Stroke Rate</b>", 
        secondary_y=True,
        showgrid= False)
           
    fig.update_layout(
        height=500,
        margin={'l': 20, 'b': 30, 'r': 10, 't':10},
		hovermode='closest',
        #plot_bgcolor=colors['background'],
        #paper_bgcolor=colors['background'],
        #font_color=colors['text'],
        #template='plotly_dark',
    )
    # Add range slider
    fig.update_layout(  
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1m",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6m",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="YTD",
                        step="year",
                        stepmode="todate"),
                    dict(count=1,
                        label="1y",
                        step="year",
                        stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="linear"
        )
    )
    fig.update_layout(clickmode='event+select')


    return fig


if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
