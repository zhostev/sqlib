from qlib.data.dataset.handler import DataHandlerLP
from qlib.data.dataset.processor import Processor
from qlib.utils import get_callable_kwargs
from qlib.data.dataset import processor as processor_module
from inspect import getfullargspec
from database_utils.db_utils import save_to_db, DuckDBManager
from alpha158 import Alpha158, _DEFAULT_LEARN_PROCESSORS, _DEFAULT_INFER_PROCESSORS,check_transform_proc


import numpy as np
import pandas as pd
from numpy import abs
from numpy import log
from numpy import sign
from scipy.stats import rankdata


# region Auxiliary functions
def ts_sum(df, window=10):
    """
    Wrapper function to estimate rolling sum.
    :param df: a pandas DataFrame.
    :param window: the rolling window.
    :return: a pandas DataFrame with the time-series min over the past 'window' days.
    """
    
    return df.rolling(window).sum()

def sma(df, window=10):
    """
    Wrapper function to estimate SMA.
    :param df: a pandas DataFrame.
    :param window: the rolling window.
    :return: a pandas DataFrame with the time-series min over the past 'window' days.
    """
    return df.rolling(window).mean()

def stddev(df, window=10):
    """
    Wrapper function to estimate rolling standard deviation.
    :param df: a pandas DataFrame.
    :param window: the rolling window.
    :return: a pandas DataFrame with the time-series min over the past 'window' days.
    """
    return df.rolling(window).std()

def correlation(x, y, window=10):
    """
    Wrapper function to estimate rolling corelations.
    :param df: a pandas DataFrame.
    :param window: the rolling window.
    :return: a pandas DataFrame with the time-series min over the past 'window' days.
    """
    return x.rolling(window).corr(y)

def covariance(x, y, window=10):
    """
    Wrapper function to estimate rolling covariance.
    :param df: a pandas DataFrame.
    :param window: the rolling window.
    :return: a pandas DataFrame with the time-series min over the past 'window' days.
    """
    return x.rolling(window).cov(y)

def rolling_rank(na):
    """
    Auxiliary function to be used in pd.rolling_apply
    :param na: numpy array.
    :return: The rank of the last value in the array.
    """
    return rankdata(na)[-1]

def ts_rank(df, window=10):
    """
    Wrapper function to estimate rolling rank.
    :param df: a pandas DataFrame.
    :param window: the rolling window.
    :return: a pandas DataFrame with the time-series rank over the past window days.
    """
    return df.rolling(window).apply(rolling_rank)

def rolling_prod(na):
    """
    Auxiliary function to be used in pd.rolling_apply
    :param na: numpy array.
    :return: The product of the values in the array.
    """
    return np.prod(na)

def product(df, window=10):
    """
    Wrapper function to estimate rolling product.
    :param df: a pandas DataFrame.
    :param window: the rolling window.
    :return: a pandas DataFrame with the time-series product over the past 'window' days.
    """
    return df.rolling(window).apply(rolling_prod)

def ts_min(df, window=10):
    """
    Wrapper function to estimate rolling min.
    :param df: a pandas DataFrame.
    :param window: the rolling window.
    :return: a pandas DataFrame with the time-series min over the past 'window' days.
    """
    return df.rolling(window).min()

def ts_max(df, window=10):
    """
    Wrapper function to estimate rolling min.
    :param df: a pandas DataFrame.
    :param window: the rolling window.
    :return: a pandas DataFrame with the time-series max over the past 'window' days.
    """
    return df.rolling(window).max()

def delta(df, period=1):
    """
    Wrapper function to estimate difference.
    :param df: a pandas DataFrame.
    :param period: the difference grade.
    :return: a pandas DataFrame with today’s value minus the value 'period' days ago.
    """
    return df.diff(period)

def delay(df, period=1):
    """
    Wrapper function to estimate lag.
    :param df: a pandas DataFrame.
    :param period: the lag grade.
    :return: a pandas DataFrame with lagged time series
    """
    return df.shift(period)

def rank(df):
    """
    Cross sectional rank
    :param df: a pandas DataFrame.
    :return: a pandas DataFrame with rank along columns.
    """
    #return df.rank(axis=1, pct=True)
    return df.rank(pct=True)

def scale(df, k=1):
    """
    Scaling time serie.
    :param df: a pandas DataFrame.
    :param k: scaling factor.
    :return: a pandas DataFrame rescaled df such that sum(abs(df)) = k
    """
    return df.mul(k).div(np.abs(df).sum())

def ts_argmax(df, window=10):
    """
    Wrapper function to estimate which day ts_max(df, window) occurred on
    :param df: a pandas DataFrame.
    :param window: the rolling window.
    :return: well.. that :)
    """
    return df.rolling(window).apply(np.argmax) + 1 

def ts_argmin(df, window=10):
    """
    Wrapper function to estimate which day ts_min(df, window) occurred on
    :param df: a pandas DataFrame.
    :param window: the rolling window.
    :return: well.. that :)
    """
    return df.rolling(window).apply(np.argmin) + 1

def decay_linear(df, period=10):
    """
    Linear weighted moving average implementation.
    :param df: a pandas DataFrame.
    :param period: the LWMA period
    :return: a pandas DataFrame with the LWMA.
    """
    # Clean data
    if df.isnull().values.any():
        df.fillna(method='ffill', inplace=True)
        df.fillna(method='bfill', inplace=True)
        df.fillna(value=0, inplace=True)
    na_lwma = np.zeros_like(df)
    na_lwma[:period, :] = df.iloc[:period, :] 
    na_series = df.as_matrix()

    divisor = period * (period + 1) / 2
    y = (np.arange(period) + 1) * 1.0 / divisor
    # Estimate the actual lwma with the actual close.
    # The backtest engine should assure to be snooping bias free.
    for row in range(period - 1, df.shape[0]):
        x = na_series[row - period + 1: row + 1, :]
        na_lwma[row, :] = (np.dot(x.T, y))
    return pd.DataFrame(na_lwma, index=df.index, columns=['CLOSE'])  
# endregion


class Alpha101(DataHandlerLP):
    def __init__(
        self,
        instruments="csi500",
        start_time=None,
        end_time=None,
        freq="day",
        infer_processors=[],
        learn_processors=_DEFAULT_LEARN_PROCESSORS,
        fit_start_time=None,
        fit_end_time=None,
        process_type=DataHandlerLP.PTYPE_A,
        filter_pipe=None,
        data_loader=None,
        inst_processors=None,
        **kwargs
    ):
        infer_processors = check_transform_proc(infer_processors, fit_start_time, fit_end_time)
        learn_processors = check_transform_proc(learn_processors, fit_start_time, fit_end_time)

        data_loader = {
            "class": "QlibDataLoader",
            "kwargs": {
                "config": {
                    "feature": self.get_feature_config(),
                    "label": kwargs.pop("label", self.get_label_config()),
                },
                "filter_pipe": filter_pipe,
                "freq": freq,
                "inst_processors": inst_processors,
            },
        }
        super().__init__(
            instruments=instruments,
            start_time=start_time,
            end_time=end_time,
            data_loader=data_loader,
            infer_processors=infer_processors,
            learn_processors=learn_processors,
            process_type=process_type,
            **kwargs
        )
        # Print loaded data
        print("Loaded data:")
        df = self.data_loader.load(instruments=self.instruments, start_time=self.start_time, end_time=self.end_time)
        print(start_time,end_time,'debug')
        print(df.tail(20))

    def alpha001(self, df):
        # Define your alpha factor calculation here
        pass

    def alpha002(self, df):
        # Define your alpha factor calculation here
        pass

    # define more alpha factors as needed...

    def get_feature_config(self):
        conf = {
            "kbar": {},
            "price": {
                "windows": [0],
                "feature": ["OPEN", "HIGH", "LOW", "VWAP"],
            },
            "rolling": {},
        }
        return self.parse_config_to_fields(conf)

    def get_label_config(self):
        return ["Ref($close, -2)/Ref($close, -1) - 1"], ["LABEL0"]

    @staticmethod
    def parse_config_to_fields(config):
        """create factors from config

        config = {
            'kbar': {}, # whether to use some hard-code kbar features
            'price': { # whether to use raw price features
                'windows': [0, 1, 2, 3, 4], # use price at n days ago
                'feature': ['OPEN', 'HIGH', 'LOW'] # which price field to use
            },
            'volume': { # whether to use raw volume features
                'windows': [0, 1, 2, 3, 4], # use volume at n days ago
            },
            'rolling': { # whether to use rolling operator based features
                'windows': [5, 10, 20, 30, 60], # rolling windows size
                'include': ['ROC', 'MA', 'STD'], # rolling operator to use
                #if include is None we will use default operators
                'exclude': ['RANK'], # rolling operator not to use
            }
        }
        """
        fields = []
        names = []
        if "kbar" in config:
            fields += [
                "($close-$open)/$open",
                "($high-$low)/$open",
                "($close-$open)/($high-$low+1e-12)",
                "($high-Greater($open, $close))/$open",
                "($high-Greater($open, $close))/($high-$low+1e-12)",
                "(Less($open, $close)-$low)/$open",
                "(Less($open, $close)-$low)/($high-$low+1e-12)",
                "(2*$close-$high-$low)/$open",
                "(2*$close-$high-$low)/($high-$low+1e-12)",
            ]
            names += [
                "KMID",
                "KLEN",
                "KMID2",
                "KUP",
                "KUP2",
                "KLOW",
                "KLOW2",
                "KSFT",
                "KSFT2",
            ]
        if "price" in config:
            windows = config["price"].get("windows", range(5))
            feature = config["price"].get("feature", ["OPEN", "HIGH", "LOW", "CLOSE", "VWAP"])
            for field in feature:
                field = field.lower()
                fields += ["Ref($%s, %d)/$close" % (field, d) if d != 0 else "$%s/$close" % field for d in windows]
                names += [field.upper() + str(d) for d in windows]
        if "volume" in config:
            windows = config["volume"].get("windows", range(5))
            fields += ["Ref($volume, %d)/($volume+1e-12)" % d if d != 0 else "$volume/($volume+1e-12)" for d in windows]
            names += ["VOLUME" + str(d) for d in windows]
        if "rolling" in config:
            windows = config["rolling"].get("windows", [5, 10, 20, 30, 60])
            include = config["rolling"].get("include", None)
            exclude = config["rolling"].get("exclude", [])
            # `exclude` in dataset config unnecessary filed
            # `include` in dataset config necessary field
            
            
            
            # Alpha#1
            def alpha001(self):
                return (rank(ts_argmax(signed_power(((self.returns < 0) ? stddev(self.returns, 20) : self.close), 2), 5)) - 0.5)

            # Alpha#2
            def alpha002(self):
                df = -1 * correlation(rank(delta(log(self.volume), 2)), rank(((self.close - self.open) / self.open)), 6)
                return df.replace([-np.inf, np.inf], 0).fillna(value=0)

            # Alpha#3
            def alpha003(self):
                df = -1 * correlation(rank(self.open), rank(self.volume), 10)
                return df.replace([-np.inf, np.inf], 0).fillna(value=0)

            # Alpha#4
            def alpha004(self):
                return -1 * ts_rank(rank(self.low), 9)

            # Alpha#5
            def alpha005(self):
                return (rank((self.open - (sum(self.vwap, 10) / 10))) * (-1 * abs(rank((self.close - self.vwap)))))

            # Alpha#6
            def alpha006(self):
                df = -1 * correlation(self.open, self.volume, 10)
                return df.replace([-np.inf, np.inf], 0).fillna(value=0)

            # Alpha#7
            def alpha007(self):
                adv20 = sma(self.volume, 20)
                alpha = -1 * ts_rank(abs(delta(self.close, 7)), 60) * sign(delta(self.close, 7))
                alpha[adv20 >= self.volume] = -1
                return alpha

            # Alpha#8
            def alpha008(self):
                return -1 * (rank(((ts_sum(self.open, 5) * ts_sum(self.returns, 5)) - delay((ts_sum(self.open, 5) * ts_sum(self.returns, 5)), 10))))

            # Alpha#9
            def alpha009(self):
                delta_close = delta(self.close, 1)
                cond_1 = ts_min(delta_close, 5) > 0
                cond_2 = ts_max(delta_close, 5) < 0
                alpha = -1 * delta_close
                alpha[cond_1 | cond_2] = delta_close
                return alpha

            # Alpha#10
            def alpha010(self):
                delta_close = delta(self.close, 1)
                cond_1 = ts_min(delta_close, 4) > 0
                cond_2 = ts_max(delta_close, 4) < 0
                alpha = -1 * delta_close
                alpha[cond_1 | cond_2] = delta_close
                return alpha

            # Alpha#11
            def alpha011(self):
                return ((rank(ts_max((self.vwap - self.close), 3)) + rank(ts_min((self.vwap - self.close), 3))) * rank(delta(self.volume, 3)))

            # Alpha#12
            def alpha012(self):
                return sign(delta(self.volume, 1)) * (-1 * delta(self.close, 1))

            # Alpha#13
            def alpha013(self):
                return -1 * rank(covariance(rank(self.close), rank(self.volume), 5))

            # Alpha#14
            def alpha014(self):
                df = correlation(self.open, self.volume, 10)
                df = df.replace([-np.inf, np.inf], 0).fillna(value=0)
                return -1 * rank(delta(self.returns, 3)) * df

            # Alpha#15
            def alpha015(self):
                df = correlation(rank(self.high), rank(self.volume), 3)
                df = df.replace([-np.inf, np.inf], 0).fillna(value=0)
                return -1 * ts_sum(rank(df), 3)

            # Alpha#16
            def alpha016(self):
                return -1 * rank(covariance(rank(self.high), rank(self.volume), 5))
            
            
            # Alpha#17
            def alpha017(self):
                adv20 = sma(self.volume, 20)
                return -1 * (rank(ts_rank(self.close, 10)) * rank(delta(delta(self.close, 1), 1)) * rank(ts_rank((self.volume / adv20), 5)))

            # Alpha#18
            def alpha018(self):
                df = correlation(self.close, self.open, 10)
                df = df.replace([-np.inf, np.inf], 0).fillna(value=0)
                return -1 * (rank((stddev(abs((self.close - self.open)), 5) + (self.close - self.open)) + df))

            # Alpha#19
            def alpha019(self):
                return ((-1 * sign((self.close - delay(self.close, 7)) + delta(self.close, 7))) * (1 + rank(1 + ts_sum(self.returns, 250))))

            # Alpha#20
            def alpha020(self):
                return (((-1 * rank((self.open - delay(self.high, 1)))) * rank((self.open - delay(self.close, 1)))) * rank((self.open - delay(self.low, 1))))

            # Alpha#21
            def alpha021(self):
                cond_1 = (sma(self.close, 8) / 8 + stddev(self.close, 8)) < (sma(self.close, 2) / 2)
                cond_2 = (sma(self.volume, 20) / self.volume) < 1
                alpha = pd.DataFrame(np.ones_like(self.close), index=self.close.index, columns=self.close.columns)
                alpha[cond_1 | cond_2] = -1
                return alpha

            # Alpha#22
            def alpha022(self):
                df = correlation(self.high, self.volume, 5)
                df = df.replace([-np.inf, np.inf], 0).fillna(value=0)
                return -1 * delta(df, 5) * rank(stddev(self.close, 20))

            # Alpha#23
            def alpha023(self):
                cond = sma(self.high, 20) < self.high
                alpha = pd.DataFrame(np.zeros_like(self.close), index=self.close.index, columns=self.close.columns)
                alpha.at[cond, 'close'] = -1 * delta(self.high, 2).fillna(value=0)
                return alpha

            # Alpha#24
            def alpha024(self):
                cond = delta(sma(self.close, 100), 100) / delay(self.close, 100) <= 0.05
                alpha = -1 * delta(self.close, 3)
                alpha[cond] = -1 * (self.close - ts_min(self.close, 100))
                return alpha

            # Alpha#25
            def alpha025(self):
                adv20 = sma(self.volume, 20)
                return rank(((((-1 * self.returns) * adv20) * self.vwap) * (self.high - self.close)))

            # Alpha#26
            def alpha026(self):
                df = correlation(ts_rank(self.volume, 5), ts_rank(self.high, 5), 5)
                df = df.replace([-np.inf, np.inf], 0).fillna(value=0)
                return -1 * ts_max(df, 3)

            # Alpha#27
            def alpha027(self):
                alpha = rank((sma(correlation(rank(self.volume), rank(self.vwap), 6), 2) / 2.0))
                alpha[alpha > 0.5] = -1
                alpha[alpha <= 0.5] = 1
                return alpha

            # Alpha#28
            def alpha028(self):
                adv20 = sma(self.volume, 20)
                df = correlation(adv20, self.low, 5)
                df = df.replace([-np.inf, np.inf], 0).fillna(value=0)
                return scale(((df + ((self.high + self.low) / 2)) - self.close))

            # Alpha#29
            def alpha029(self):
                return (ts_min(rank(rank(scale(log(ts_sum(rank(rank(-1 * rank(delta((self.close - 1), 5)))), 2))))), 5) + ts_rank(delay((-1 * self.returns), 6), 5))

            # Alpha#30
            def alpha030(self):
                return (((1 - rank(rank(decay_linear(delta(self.volume, 1), 10)))) * ts_sum(self.volume, 5)) / ts_sum(self.volume, 20))

            # Alpha#31
            def alpha031(self):
                adv20 = sma(self.volume, 20)
                return ((rank(rank(rank(decay_linear((-1 * rank(rank(delta((self.close - 1), 5))))).to_frame(), 10)))) + rank((-1 * delta(self.close, 3)))) + sign(scale(correlation(adv20, self.low, 12))))

            # Alpha#32
            def alpha032(self):
                return scale(((sma(self.close, 7) / 7) - self.close)) + (20 * scale(correlation(self.vwap, delay(self.close, 5), 230)))

            # Alpha#33
            def alpha033(self):
                return rank((-1 * ((1 - (self.open / self.close)) ** 1)))

            # Alpha#34
            def alpha034(self):
                inner = stddev(self.returns, 2) / stddev(self.returns, 5)
                inner = inner.replace([-np.inf, np.inf], 1).fillna(value=1)
                return rank(1 - rank(inner) - rank(delta(self.close, 1)))

            # Alpha#35
            def alpha035(self):
                adv20 = sma(self.volume, 20)
                return (ts_rank(self.volume / adv20, 20) * ts_rank((-1 * delta(self.close, 7)), 8))

            # Alpha#36
            def alpha036(self):
                adv20 = sma(self.volume, 20)
                return (((((2.21 * rank(correlation((self.close - self.open), delay(self.volume, 1), 15))) + (0.7 * rank((self.open- self.close)))) + (0.73 * rank(ts_rank(delay((-1 * self.returns), 6), 5)))) + rank(abs(correlation(self.vwap, adv20, 6)))) + (0.6 * rank((((sma(self.close, 200) / 200) - self.open) * (self.close - self.open)))))

            # Alpha#37
            def alpha037(self):
                return rank(correlation(delay(self.open - self.close, 1), self.close, 200)) + rank(self.open - self.close)

            # Alpha#38
            def alpha038(self):
                inner = self.close / self.open
                inner = inner.replace([-np.inf, np.inf], 1).fillna(value=1)
                return -1 * rank(ts_rank(self.open, 10)) * rank(inner)

            # Alpha#39
            def alpha039(self):
                adv20 = sma(self.volume, 20)
                return ((-1 * rank(delta(self.close, 7) * (1 - rank(decay_linear((self.volume / adv20).to_frame(), 9).CLOSE)))) * (1 + rank(sma(self.returns, 250))))

            # Alpha#40
            def alpha040(self):
                return -1 * rank(stddev(self.high, 10)) * correlation(self.high, self.volume, 10)

            # Alpha#41
            def alpha041(self):
                return pow((self.high * self.low), 0.5) - self.vwap

            # Alpha#42
            def alpha042(self):
                return rank((self.vwap - self.close)) / rank((self.vwap + self.close))

            # Alpha#43
            def alpha043(self):
                adv20 = sma(self.volume, 20)
                return ts_rank(self.volume / adv20, 20) * ts_rank((-1 * delta(self.close, 7)), 8)

            # Alpha#44
            def alpha044(self):
                df = correlation(self.high, rank(self.volume), 5)
                df = df.replace([-np.inf, np.inf], 0).fillna(value=0)
                return -1 * df

            # Alpha#45
            def alpha045(self):
                df = correlation(self.close, self.volume, 2)
                df = df.replace([-np.inf, np.inf], 0).fillna(value=0)
                return -1 * (rank(sma(delay(self.close, 5), 20)) * df * rank(correlation(ts_sum(self.close, 5), ts_sum(self.close, 20), 2)))

            # Alpha#46
            def alpha046(self):
                inner = ((delay(self.close, 20) - delay(self.close, 10)) / 10) - ((delay(self.close, 10) - self.close) / 10)
                alpha = (-1 * delta(self.close))
                alpha[inner < 0] = 1
                alpha[inner > 0.25] = -1
                return alpha

            # Alpha#47
            def alpha047(self):
                adv20 = sma(self.volume, 20)
                return ((((rank((1 / self.close)) * self.volume) / adv20) * ((self.high * rank((self.high - self.close))) / (sma(self.high, 5) / 5))) - rank((self.vwap - delay(self.vwap, 5))))

            # Alpha#48
            # Placeholder for Alpha#48

            # Alpha#49
            def alpha049(self):
                inner = (((delay(self.close, 20) - delay(self.close, 10)) / 10) - ((delay(self.close, 10) - self.close) / 10))
                alpha = (-1 * delta(self.close))
                alpha[inner < -0.1] = 1
                return alpha

            # Alpha#50
            def alpha050(self):
                return (-1 * ts_max(rank(correlation(rank(self.volume), rank(self.vwap), 5)), 5))


            # Alpha#51
            def alpha051(self):
                inner = (((delay(self.close, 20) - delay(self.close, 10)) / 10) - ((delay(self.close, 10) - self.close) / 10))
                alpha = (-1 * delta(self.close))
                alpha[inner < -0.05] = 1
                return alpha

            # Alpha#52
            def alpha052(self):
                return (((-1 * delta(ts_min(self.low, 5), 5)) *
                        rank(((ts_sum(self.returns, 240) - ts_sum(self.returns, 20)) / 220))) * ts_rank(self.volume, 5))

            # Alpha#53
            def alpha053(self):
                inner = (self.close - self.low).replace(0, 0.0001)
                return -1 * delta((((self.close - self.low) - (self.high - self.close)) / inner), 9)

            # Alpha#54
            def alpha054(self):
                inner = (self.low - self.high).replace(0, -0.0001)
                return -1 * (self.low - self.close) * (self.open ** 5) / (inner * (self.close ** 5))

            # Alpha#55
            def alpha055(self):
                divisor = (ts_max(self.high, 12) - ts_min(self.low, 12)).replace(0, 0.0001)
                inner = (self.close - ts_min(self.low, 12)) / (divisor)
                df = correlation(rank(inner), rank(self.volume), 6)
                return -1 * df.replace([-np.inf, np.inf], 0).fillna(value=0)

            # Alpha#56
            # Placeholder for Alpha#56

            # Alpha#57
            def alpha057(self):
                return (0 - (1 * ((self.close - self.vwap) / decay_linear(rank(ts_argmax(self.close, 30)).to_frame(), 2).CLOSE)))

            # Alpha#58
            # Placeholder for Alpha#58

            # Alpha#59
            # Placeholder for Alpha#59

            # Alpha#60
            def alpha060(self):
                divisor = (self.high - self.low).replace(0, 0.0001)
                inner = ((self.close - self.low) - (self.high - self.close)) * self.volume / divisor
                return - ((2 * scale(rank(inner))) - scale(rank(ts_argmax(self.close, 10))))

            # Alpha#61
            def alpha061(self):
                adv180 = sma(self.volume, 180)
                return (rank((self.vwap - ts_min(self.vwap, 16))) < rank(correlation(self.vwap, adv180, 18)))

            # Alpha#62
            def alpha062(self):
                adv20 = sma(self.volume, 20)
                return ((rank(correlation(self.vwap, sma(adv20, 22), 10)) < rank(((rank(self.open) + rank(self.open)) < (rank(((self.high + self.low) / 2)) + rank(self.high))))) * -1)

            # Alpha#63
            # Placeholder for Alpha#63

            # Alpha#64
            def alpha064(self):
                adv120 = sma(self.volume, 120)
                return ((rank(correlation(sma(((self.open * 0.178404) + (self.low * (1 - 0.178404))), 13), sma(adv120, 13), 17)) < rank(delta(((((self.high + self.low) / 2) * 0.178404) + (self.vwap * (1 - 0.178404))), 3.69741))) * -1)

            # Alpha#65
            def alpha065(self):
                adv60 = sma(self.volume, 60)
                return ((rank(correlation(((self.open * 0.00817205) + (self.vwap * (1 - 0.00817205))), sma(adv60, 9), 6)) < rank((self.open - ts_min(self.open, 14)))) * -1)

            # Alpha#66
            def alpha066(self):
                return ((rank(decay_linear(delta(self.vwap, 4).to_frame(), 7).CLOSE) + ts_rank(decay_linear(((((self.low * 0.96633) + (self.low * (1 - 0.96633))) - self.vwap) / (self.open - ((self.high + self.low) / 2))).to_frame(), 11).CLOSE, 7)) * -1)

            # Alpha#67
            # Placeholder for Alpha#67

            # Alpha#68
            def alpha068(self):
                adv15 = sma(self.volume, 15)
                return ((ts_rank(correlation(rank(self.high), rank(adv15), 9), 14) < rank(delta(((self.close * 0.518371) + (self.low * (1 - 0.518371))), 1.06157))) * -1)


            # Alpha#69
            def alpha069(self):
                adv_industry = IndNeutralize(self.vwap, IndClass.industry)
                p1 = rank(ts_max(delta(adv_industry, 2.72412), 4.79344))
                p2 = ts_rank(correlation(((self.close * 0.490655) + (self.vwap * (1 - 0.490655))), self.volume, 4.92416), 9.0615)
                return -1 * (p1.pow(p2))

            # Alpha#70
            def alpha070(self):
                return (rank(delta(self.vwap, 1.29456)).pow(ts_rank(correlation(IndNeutralize(self.close, IndClass.industry), self.volume, 17.8256), 17.9171))) * -1

            # Alpha#71
            def alpha071(self):
                adv180 = sma(self.volume, 180)
                p1 = ts_rank(decay_linear(correlation(ts_rank(self.close, 3.43976), ts_rank(adv180, 12.0647), 18.0175).to_frame(), 4.20501).CLOSE, 15.6948)
                p2 = ts_rank(decay_linear((rank(((self.low + self.open) - (self.vwap + self.vwap))).pow(2)).to_frame(), 16.4662).CLOSE, 4.4388)
                return pd.concat([p1, p2], axis=1).max(axis=1)

            # Alpha#72
            def alpha072(self):
                adv40 = sma(self.volume, 40)
                return (rank(decay_linear(correlation(((self.high + self.low) / 2), adv40, 8.93345), 10.1519)) / rank(decay_linear(correlation(ts_rank(self.vwap, 3.72469), ts_rank(self.volume, 18.5188), 6.86671), 2.95011)))

            # Alpha#73
            def alpha073(self):
                p1 = rank(decay_linear(delta(self.vwap, 4.72775), 2.91864))
                p2 = ts_rank(decay_linear(((delta(((self.open * 0.147155) + (self.low * (1 - 0.147155))), 2) / ((self.open * 0.147155) + (self.low * (1 - 0.147155)))) * -1).to_frame(), 3.33829).CLOSE, 16.7411)
                return -1 * pd.concat([p1, p2], axis=1).max(axis=1)

            # Alpha#74
            def alpha074(self):
                adv30 = sma(self.volume, 30)
                return ((rank(correlation(self.close, sma(adv30, 37), 15)) < rank(correlation(rank(((self.high * 0.0261661) + (self.vwap * (1 - 0.0261661)))), rank(self.volume), 11))) * -1)

            # Alpha#75
            def alpha075(self):
                adv50 = sma(self.volume, 50)
                return (rank(correlation(self.vwap, self.volume, 4)) < rank(correlation(rank(self.low), rank(adv50), 12)))

            # Alpha#76
            # Placeholder for Alpha#76

            # Alpha#77
            def alpha077(self):
                adv40 = sma(self.volume, 40)
                p1 = rank(decay_linear(((((self.high + self.low) / 2) + self.high) - (self.vwap + self.high)).to_frame(), 20.0451).CLOSE)
                p2 = rank(decay_linear(correlation(((self.high + self.low) / 2), adv40, 3.1614), 5.64125).CLOSE)
                return pd.concat([p1, p2], axis=1).min(axis=1)

            # Alpha#78
            def alpha078(self):
                adv40 = sma(self.volume, 40)
                return (rank(correlation(ts_sum(((self.low * 0.352233) + (self.vwap * (1 - 0.352233))), 19), ts_sum(adv40, 19), 6.83313)).pow(rank(correlation(rank(self.vwap), rank(self.volume), 5.77492))))

            # Alpha#79
            # Placeholder for Alpha#79

            # Alpha#80
            # Placeholder for Alpha#80

            # Alpha#81
            def alpha081(self):
                adv10 = sma(self.volume, 10)
                return ((rank(log(product(rank((rank(correlation(self.vwap, ts_sum(adv10, 49.6054), 8.47743))).pow(4))), 14.9655))) < rank(correlation(rank(self.vwap), rank(self.volume), 5.07914))) * -1

            # Alpha#82
            # Placeholder for Alpha#82

            # Alpha#83
            def alpha083(self):
                return ((rank(delay(((self.high - self.low) / (ts_sum(self.close, 5) / 5)), 2)) * rank(rank(self.volume))) / (((self.high - self.low) / (ts_sum(self.close, 5) / 5)) / (self.vwap - self.close)))

            # Alpha#84
            def alpha084(self):
                return pow(ts_rank((self.vwap - ts_max(self.vwap, 15.3217)), 20.7127), delta(self.close, 4.96796))

            # Alpha#85
            def alpha085(self):
                adv30 = sma(self.volume, 30)
                return (rank(correlation(((self.high * 0.876703) + (self.close * (1 - 0.876703))), adv30, 9.61331)).pow(rank(correlation(ts_rank(((self.high + self.low) / 2), 3.70596), ts_rank(self.volume, 10.1595), 7.11408))))

            # Alpha#86
            def alpha086(self):
                adv60 = sma(self.volume, 60)
                return ((ts_rank(decay_linear(correlation(self.close, sma(adv60, 15), 6.00049), 5.51607), 3.79744) - ts_rank(decay_linear(delta(IndNeutralize(self.vwap, IndClass.industry), 3.48158), 10.1466), 15.3012)) * -1)

            # Alpha#87
            # Placeholder for Alpha#87

            # Alpha#88
            def alpha088(self):
                adv60 = sma(self.volume, 60)
                p1 = rank(decay_linear(((rank(self.open) + rank(self.low)) - (rank(self.high) + rank(self.close))).to_frame(), 8.06882).CLOSE)
                p2 = rank(decay_linear(correlation(((self.high + self.low) / 2), adv60, 3.1614), 5.64125).CLOSE)
                return pd.concat([p1, p2], axis=1).min(axis=1)

            # Alpha#89
            # Placeholder for Alpha#89

            # Alpha#90
            # Placeholder for Alpha#90

            # Alpha#91
            # Placeholder for Alpha#91

            # Alpha#92
            def alpha092(self):
                adv30 = sma(self.volume, 30)
                p1 = ts_rank(decay_linear(((((self.high + self.low) / 2) + self.close) < (self.low + self.open)).to_frame(), 14.7221), 18.8683)
                p2 = ts_rank(decay_linear(correlation(rank(self.low), rank(adv30), 7.58555), 6.94024), 6.80584)
                return pd.concat([p1, p2], axis=1).min(axis=1)

            # Alpha#93
            # Placeholder for Alpha#93

            # Alpha#94
            def alpha094(self):
                adv60 = sma(self.volume, 60)
                return ((rank((self.vwap - ts_min(self.vwap, 11.5783))).pow(ts_rank(correlation(ts_rank(self.vwap, 19.6462), ts_rank(adv60, 4.02992), 18.0926), 2.70756))) * -1)

            # Alpha#95
            def alpha095(self):
                adv50 = sma(self.volume, 50)
                return (rank((self.open - ts_min(self.open, 12.4105))) < ts_rank((rank(correlation(sma(((self.high + self.low) / 2), 19.1351), sma(adv40, 19.1351), 12.8742)).pow(5)), 11.7584))

            # Alpha#96
            def alpha096(self):
                adv60 = sma(self.volume, 60)
                p1 = ts_rank(decay_linear(correlation(rank(self.vwap), rank(self.volume), 3.83878), 4.16783), 8.38151)
                p2 = ts_rank(decay_linear(ts_argmax(correlation(ts_rank(self.close, 7.45404), ts_rank(adv60, 4.13242), 3.65459), 12.6556), 14.0365), 13.4143)
                return pd.concat([p1, p2], axis=1).max(axis=1) * -1

            # Alpha#97
            # Placeholder for Alpha#97

            # Alpha#98
            def alpha098(self):
                adv15 = sma(self.volume, 15)
                return (rank(decay_linear(correlation(self.vwap, ts_sum(adv5, 26.4719), 4.58418), 7.18088)) - rank(decay_linear(ts_rank(ts_argmin(correlation(rank(self.open), rank(adv15), 20.8187), 8.62571), 6.95668), 8.07206)))

            # Alpha#99
            def alpha099(self):
                adv60 = sma(self.volume, 60)
                return ((rank(correlation(ts_sum(((self.high + self.low) / 2), 19.8975), ts_sum(adv60, 19.8975), 8.8136)) < rank(correlation(self.low, self.volume, 6.28259))) * -1)

            # Alpha#100
            # Placeholder for Alpha#100

            # Alpha#101
            def alpha101(self):
                return (self.close - self.open) / ((self.high - self.low) + 0.001)
