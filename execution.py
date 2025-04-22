import pandas as pd

class Execution:
    def __init__(self):
        self.trades = pd.DataFrame(columns=[
            "timestamp","symbol","side","price","size","sl","tp","pnl"
        ])

    def execute(self, signal: str, price: float, size: float, sl: float, tp: float):
        trade = {
            "timestamp": pd.Timestamp.utcnow(),
            "symbol": None,
            "side": signal,
            "price": price,
            "size": size,
            "sl": sl,
            "tp": tp,
            "pnl": 0.0
        }
        # insert as a new row by index
        self.trades.loc[len(self.trades)] = trade
