import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
import quandl
from dash.dependencies import Input, Output

quandl.ApiConfig.api_key = 'QrkyFyJnoyC-SMpNC_ca'
app = dash.Dash()

app.layout = html.Div(children=[
    html.H1(children='Dashboard'),
    html.Div(children='''
    Financial Dashboard using Dash.
    '''),
    dcc.Input(id='input', value='', type='text'),
    html.Div(id='output-graph')
])

@app.callback(
    Output(component_id='output-graph', component_property='children'),
    [Input(component_id='input', component_property='value')]
)
def update_graph(input_data):
    start = datetime.datetime(2015, 1, 1)
    end = datetime.datetime.now()
    ticker = input_data.upper()
    stock = 'WIKI/' + ticker
    mydata = quandl.get(stock, start_date=start, end_date=end)

    return dcc.Graph(
        id='stock-graph',
        figure={
            'data':[
                {'x': mydata.index, 'y': mydata.Close, 'type': 'line', 'name': ticker},
            ],
            'layout': {
                'title': stock
            }
        }
    )

if __name__ == '__main__':
    app.run_server(debug=True)

#QrkyFyJnoyC-SMpNC_ca
