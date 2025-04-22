import tkinter as tk
import time
from utils import load_config, setup_logger
from data_feed import DataFeed
from indicator_calculator import IndicatorCalculator
from strategy_engine import StrategyEngine
from risk_manager import RiskManager
from execution import Execution

# Load configuration and logger
cfg = load_config()
logger = setup_logger(__name__)

# Initialize modules
dfm = DataFeed()
strat = StrategyEngine(cfg["strategy"])
risk_mgr = RiskManager(cfg["risk"]["capital"])
execm = Execution()

# Settings and state
price_refresh_secs = 10
symbols = cfg["exchange"]["symbol"]
starting_capital = cfg["risk"]["capital"]
capital = starting_capital
positions = {symbol: 0.0 for symbol in symbols}
total_bought = {symbol: 0.0 for symbol in symbols}
total_sold = {symbol: 0.0 for symbol in symbols}

# GUI elements
price_label = None
capital_label = None
time_label = None
status_label = None

# Decision explanation helper
def explain_decision(signal, df):
    latest = df.iloc[-1]
    prev = df.iloc[-2]
    if signal == "buy":
        if latest['ema_fast'] > latest['ema_slow'] and prev['ema_fast'] <= prev['ema_slow']:
            return "Fast EMA crossed above slow EMA"
        if latest['rsi'] < 30:
            return "RSI below oversold threshold"
        return "Buy conditions met"
    elif signal == "sell":
        if latest['ema_fast'] < latest['ema_slow'] and prev['ema_fast'] >= prev['ema_slow']:
            return "Fast EMA crossed below slow EMA"
        if latest['rsi'] > 70:
            return "RSI above overbought threshold"
        return "Sell conditions met"
    return "No signal"

# Main bot logic update
def run_cycle():
    global capital
    prices = {}
    updates = []

    for symbol in symbols:
        df = dfm.fetch_historical(symbol, cfg["exchange"]["timeframe_h"])
        df = IndicatorCalculator.run_all(df)
        signal = strat.generate_signal(df)
        price = df["close"].iloc[-1]
        prices[symbol] = price
        explanation = explain_decision(signal, df)

        if signal in ("buy", "sell"):
            size = risk_mgr.position_size(price)
            sl, tp = risk_mgr.apply_sl_tp(price)
            execm.execute(signal, price, size, sl, tp)
            if signal == "buy":
                capital -= price * size
                total_bought[symbol] += size
                positions[symbol] += size
            else:
                capital += price * size
                total_sold[symbol] += size
                positions[symbol] -= size
            updates.append(
                f"{symbol}: {signal.upper()} @ {price:.2f} | size {size:.6f} | SL {sl:.2f} | TP {tp:.2f} — {explanation}"
            )
        else:
            updates.append(f"{symbol}: HOLD @ {price:.2f} — {explanation}")

        updates.append(f"  Bought: {total_bought[symbol]:.6f}, Sold: {total_sold[symbol]:.6f}, Pos: {positions[symbol]:.6f}")
        updates.append("")

    equity = capital + sum(prices[s] * positions[s] for s in symbols)
    pnl = equity - starting_capital

    # Update GUI
    if price_label:
        price_label.config(text=" | ".join(f"{s}: {prices[s]:.2f}" for s in symbols))
    if capital_label:
        capital_label.config(text=f"Cash: ${capital:.2f}  Equity: ${equity:.2f}  P/L: ${pnl:.2f}")
    if time_label:
        time_label.config(text=time.strftime("Last update: %Y-%m-%d %H:%M:%S"))
    if status_label:
        status_label.config(text="\n".join(updates))

# GUI launcher
def start_bot():
    global price_label, capital_label, time_label, status_label
    root = tk.Tk()
    root.title("Crypto Trading Bot Dashboard")

    price_label = tk.Label(root, text="Fetching...", font=("Arial", 12))
    price_label.pack(padx=10, pady=5)

    capital_label = tk.Label(root, text="", font=("Arial", 12))
    capital_label.pack(padx=10, pady=5)

    time_label = tk.Label(root, text="", font=("Arial", 10))
    time_label.pack(padx=10, pady=5)

    status_label = tk.Label(root, text="Initializing...", font=("Arial", 10), justify=tk.LEFT)
    status_label.pack(padx=10, pady=10)

    def periodic():
        run_cycle()
        root.after(price_refresh_secs * 1000, periodic)

    periodic()
    root.mainloop()

if __name__ == "__main__":
    start_bot()
