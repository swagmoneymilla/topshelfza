from finta import TA as talib
import pandas as pd
from utils import load_config

# load your strategy settings
config = load_config()["strategy"]

class IndicatorCalculator:
    @staticmethod
    def add_ema(df: pd.DataFrame):
        # FinTA expects the full DataFrame and the period
        df["ema_fast"] = talib.EMA(df, config["ema_fast"])
        df["ema_slow"] = talib.EMA(df, config["ema_slow"])

    @staticmethod
    def add_rsi(df: pd.DataFrame):
        df["rsi"] = talib.RSI(df, config["rsi_period"])

    @classmethod
    def run_all(cls, df: pd.DataFrame):
        cls.add_ema(df)
        cls.add_rsi(df)
        return df
