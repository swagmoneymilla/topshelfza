import numpy as np
from utils import load_config

cfg = load_config()["risk"]

class RiskManager:
    def __init__(self, balance: float):
        self.balance = balance  # paper trading cash
    
    def position_size(self, price: float) -> float:
        risk_amount = self.balance * cfg["risk_per_trade"]
        # e.g., use ATR to set stop‑loss distance
        # size = risk_amount / (atr * cfg["stop_atr_multiplier"])
        return risk_amount / price  # simple example

    def apply_sl_tp(self, entry: float) -> (float, float):
        # stub: compute SL/TP based on ATR or fixed percentages
        sl = entry * (1 - 0.01)
        tp = entry * (1 + 0.02)
        return sl, tp
