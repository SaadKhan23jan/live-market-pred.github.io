from datetime import datetime as dt
from dateutil.relativedelta import relativedelta
from dash import Dash, html, dcc, Output, Input
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import yfinance as yf
from crypto_list import crypto_list

css_sheet = [dbc.themes.UNITED]
BS = "https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css"
app = Dash(__name__, external_stylesheets=css_sheet)

app.layout = html.Div([
    dbc.Button('Contact Me: LinkedIn', href='https://www.linkedin.com/in/saad-khan-167704163/', target='_blank',
               style={'margin':'Right'}),
    html.Div(
        html.H1("Welcome to Live Crypto data", style={'textAlign':'center', 'backgroundColor':'Lightgreen'})
    ),

    html.Div([
        html.Label('Select Crypto-Pair'),
        dcc.Dropdown(id='crypto-pair', options=crypto_list,
                     style={'width':'50%'}, value='BTC-USD'),
    ]),

    html.Div([
        html.Label('Select Time Frame'),
        dcc.Dropdown(id='time-frame', options=[{'label':'10 Year', 'value':'10y'},
                                               {'label':'1 Year', 'value':'1y'},
                                               {'label':'6 Months', 'value':'6mo'},
                                               {'label':'3 Months', 'value':'3mo'},
                                               {'label':'1 Months', 'value':'1mo'},
                                               {'label':'1 Week', 'value':'1wk'},
                                               {'label':'1 Day', 'value':'1d'}],
                     style={'width':'50%'}, value='1y')
    ]),

    html.Div(
        dcc.Graph(id='my-graph-candlestick')
    ),

    html.Div(
        dcc.Graph(id='my-graph-line')
    ),


], style={'background-color': 'Lightgreen'})

@app.callback([Output('my-graph-candlestick', 'figure'),
               Output('my-graph-line', 'figure')],
              [Input('crypto-pair', 'value'),
               Input('time-frame', 'value')])
def update_graph(crypto, time_frame):
    if time_frame in ['10y']:
        interval = '1mo'
        start = (dt.now()-relativedelta(years=10))
    elif time_frame in ['1y']:
        interval = '1wk'
        start = (dt.now() - relativedelta(years=1))
    elif time_frame in ['6mo']:
        interval = '5d'
        start = (dt.now() - relativedelta(months=6))
    elif time_frame in ['3mo']:
        interval = '1d'
        start = (dt.now() - relativedelta(months=3))
    elif time_frame in ['1mo']:
        interval = '90m'
        start = (dt.now() - relativedelta(months=1))
    elif time_frame in ['1wk']:
        interval = '30m'
        start = (dt.now() - relativedelta(weeks=1))
    elif time_frame in ['1d']:
        interval = '15m'
        start = (dt.now() - relativedelta(days=1))
    else:
        interval = '1m'
        start = dt.now() - relativedelta(days=1)

    end = dt.now()



    #df = yf.download(tickers=crypto, period=time_frame, interval=interval)
    df = yf.download(tickers=crypto, start=start, end=end)

    fig1 = go.Figure(data=[go.Candlestick(x=df.index,
                                          open=df.Open,
                                          high=df.High,
                                          low=df.Low,
                                          close=df.Close)])
    fig1.update_layout(title=f'Candle Chart of {crypto}', xaxis_title='Time', yaxis_title=f'{crypto}')

    fig2 = px.line(data_frame=df, x=df.index, y=df['Volume'], markers='o')
    fig2.update_layout(title=f'History of Volume {crypto}', xaxis_title='Time', yaxis_title=f'Volume of {crypto}')
    return fig1, fig2




if __name__ == '__main__':
    app.run_server(debug=True)