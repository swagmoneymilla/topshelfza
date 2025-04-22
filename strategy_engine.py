from typing import Dict
import pandas as pd

class StrategyEngine:
    def __init__(self, config: Dict):
        self.cfg = config
    
    def generate_signal(self, df: pd.DataFrame) -> str:
        latest = df.iloc[-1]
        prev   = df.iloc[-2]
        # Example: EMA crossover + RSI filter
        if prev["ema_fast"] < prev["ema_slow"] and latest["ema_fast"] > latest["ema_slow"]            and latest["rsi"] < self.cfg["rsi_overbought"]:
            return "buy"
        if prev["ema_fast"] > prev["ema_slow"] and latest["ema_fast"] < latest["ema_slow"]            and latest["rsi"] > self.cfg["rsi_oversold"]:
            return "sell"
        return "hold"
