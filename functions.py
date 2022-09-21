from statsmodels.tsa.statespace.sarimax import SARIMAX, SARIMAXResults
import pandas as pd
import dash_table
import plotly.express as px


def sarimax_pred(df, p, i, q, sarimax_model, days):
    if sarimax_model=='MA':
        order=(p, 0, 0)
    elif sarimax_model == 'AR':
        order=(0, 0, q)
    elif sarimax_model == 'ARMA':
        order=(p, 0, q)
    else:
        order=(p, i, q)

    if sarimax_model=='SARIMAX':
        model = SARIMAX(df['Close'], trend='c', order=order, seasonal_order=(p, i, q, 12))
    else:
        model = SARIMAX(df['Close'], trend='c', order=order)


    results = model.fit()
    preds = SARIMAXResults.predict(results, start=len(df), end=len(df) + days)
    actual = df['Close'].values
    results_summary = results.summary()

    results_as_html = results_summary.tables[1].as_html()
    results = pd.read_html(results_as_html, header=0, index_col=0)[0]
    data = results.to_dict('rows')
    columns = [{"name": i, "id": i, } for i in (results.columns)]


    pred_fig = px.line(y=preds)

    return dash_table.DataTable(data=data, columns=columns), pred_fig

