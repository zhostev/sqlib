import pandas as pd
import pybroker
from pybroker.data import DataSource
import qlib
from qlib.data import D

class qlibDataSource(DataSource):

    def __init__(self):
        qlib.init_qlib(provider_uri='~/.qlib/qlib_data/invest')  # Adjust the path according to your setup

    def _fetch_data(self, symbols, start_date, end_date, _timeframe, _adjust):
        # symbols are already passed as arguments, no need to hardcode them
        fields = ['$close','$open','$high', '$volume', '$low', '$amount','$factor','$change','$vwap']
        df = D.features(symbols, fields, start_time=start_date, end_time=end_date, freq='day').reset_index()
        df = df.rename(columns={'instrument':'symbol','datetime':'date','$open':'open','$high':'high','$low':'low','$close':'close'})
        df = df[['symbol', 'date', 'open', 'high', 'low', 'close']]
        return df


data_source = qlibDataSource()
symbols = ['SH600809','SZ000001', 'SZ000002']
start_date = '2023-01-01'
end_date = '2023-12-31'
_timeframe = 'day'
_adjust = None

df = data_source._fetch_data(symbols, start_date, end_date, _timeframe, _adjust)
# print(df.head())