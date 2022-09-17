from statsmodels.tsa.statespace.sarimax import SARIMAX
import pandas as pd
import dash_table

def sarimax_pred(df):
    model = SARIMAX(df['Close'], trend='c', order=(1, 1, 1))
    results = model.fit()
    results_summary = results.summary()

    results_as_html = results_summary.tables[1].as_html()
    results = pd.read_html(results_as_html, header=0, index_col=0)[0]
    data = results.to_dict('rows')
    columns = [{"name": i, "id": i, } for i in (df.columns)]
    return dash_table.DataTable(data=data, columns=columns)

