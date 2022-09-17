from datetime import datetime as dt
from dateutil.relativedelta import relativedelta
from dash import html, dcc, Output, Input
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import yfinance as yf
from stock_market_list import stock_market_list
from functions import sarimax_pred


def prophet_prediction(df):
    pass

css_sheet = [dbc.themes.SPACELAB]
BS = "https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css"
dash.register_page(__name__)

layout = html.Div([
    dbc.Button('Contact Me: LinkedIn', href='https://www.linkedin.com/in/saad-khan-167704163/', target='_blank',
               style={'position':'center'}),
    html.Div(
        html.H1("Welcome to Live Crypto data", style={'textAlign':'center', 'backgroundColor':'Lightgreen'})
    ),

    html.Div([
        html.Label('Select Crypto-Pair'),
        dcc.Dropdown(id='crypto-pair', options=stock_market_list,
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
                                               {'label':'1 Day', 'value':'24h'}],
                     style={'width':'50%'}, value='1y'),
    ]),

    html.Div(
        dcc.Graph(id='my-graph-candlestick')
    ),

    html.Div(
        dcc.Graph(id='my-graph-line')
    ),

    html.Div([
        html.H2("SARIMAX Models Predictions"),
        html.Br(),

        html.Label('Select one of SARIMAX Model:   '),
        dcc.Dropdown(id='sarimax-model', options=[{'label':'MA', 'value':'MA'},
                                                  {'label':'AR', 'value':'AR'},
                                                  {'label':'ARMA','value':'ARMA'},
                                                  {'label':'ARIMA', 'value':'ARIMA'},
                                                  {'label':'SARIMAX', 'value':'SARIMAX'},
                                                  ],
                     style={'width':'50%', 'backgroundColor':'Lightscreen'},
                     value='SARIMAX'
                     ),


        html.Div([
            html.Label('Enter the order of P:   '),
            dcc.Input(id='p-order', type='number', placeholder='Enter the order of P', value=0, inputMode='numeric'),
        ], style={'display':'inline'}
        ),
        html.Div([
            html.Label('Enter the order of I:   '),
            dcc.Input(id='i-order', type='number', placeholder='Enter the order of I', value=0, inputMode='numeric'),
        ], style={'display':'inline'}
        ),
        html.Div([
            html.Label('Enter the order of Q:   '),
            dcc.Input(id='q-order', type='number', placeholder='Enter the order of Q', value=0, inputMode='numeric'),
        ], style={'display':'inline'}
        ),
        #dash_table.DataTable(id='sarimax-results',columns =  [{"name": i, "id": i,} for i in (df.columns)],),
        html.Div(id='sarimax-results'),

    ]),

    html.Br(),
    html.Br(),
    html.Br(),
    html.H1(f'Predictions Through SARIMAX Models'),
    dcc.Graph(id='fig-pred')





], style={'background-color': 'Lightgreen'})

@callback([Output('my-graph-candlestick', 'figure'),
               Output('my-graph-line', 'figure'),
               Output('sarimax-results', 'children'),
               Output('fig-pred', 'figure')],
              [Input('crypto-pair', 'value'),
               Input('time-frame', 'value'),
               Input('p-order', 'value'),
               Input('i-order', 'value'),
               Input('q-order', 'value'),
               Input('sarimax-model', 'value')])
def update_graph(crypto, time_frame, p, i, q, sarimax_model):
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
    elif time_frame in ['24h']:
        interval = '1m'
        start = (dt.now() - relativedelta(hours=23))
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

    # Here we will call our function for SARIMAX Model
    results, fig_pred = sarimax_pred(df, p, i, q, sarimax_model)

    fig_pred.update_layout(title='Predictions')

    return fig1, fig2, results, fig_pred
