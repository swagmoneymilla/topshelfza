import ccxt
import pandas as pd
from utils import load_config, setup_logger

logger = setup_logger(__name__)
config = load_config()

class DataFeed:
    def __init__(self):
        ex_cfg = config["exchange"]
        self.exchange = getattr(ccxt, ex_cfg["name"])()
        self.symbols = ex_cfg["symbol"]
    
    def fetch_historical(self, symbol: str, timeframe: str, since=None, limit=1000) -> pd.DataFrame:
        bars = self.exchange.fetch_ohlcv(symbol, timeframe, since=since, limit=limit)
        df = pd.DataFrame(bars, columns=["timestamp","open","high","low","close","volume"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        return df.set_index("timestamp")
    
    def fetch_latest(self, symbol: str, timeframe: str) -> pd.DataFrame:
        return self.fetch_historical(symbol, timeframe, limit=1)
