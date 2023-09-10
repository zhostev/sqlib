import pandas as pd
import pybroker
from pybroker.data import DataSource
import qlib
from qlib.data import D

class qlibDataSource(DataSource):

    def __init__(self):
        super().__init__()
        qlib.init_qlib(provider_uri='~/.qlib/qlib_data/invest')

    def _fetch_data(self, symbols, start_date, end_date, _timeframe, _adjust):
        fields = ['$' + field for field in ['close', 'open', 'high', 'volume', 'low', 'amount', 'factor', 'change', 'vwap']]
        df = D.features(symbols, fields, start_time=start_date, end_time=end_date, freq='day').reset_index()

        df = df.rename(columns={'instrument':'symbol', 'datetime':'date', '$open':'open', '$high':'high', '$low':'low', '$close':'close'})
        df = df[['symbol', 'date', 'open', 'high', 'low', 'close']]

        return df
