import time
from utils import load_config, setup_logger
from data_feed import DataFeed
from indicator_calculator import IndicatorCalculator
from strategy_engine import StrategyEngine
from risk_manager import RiskManager
from execution import Execution
# from ml_module import LSTMModel  # optional: load & infer

logger = setup_logger(__name__)
cfg = load_config()

def main():
    dfm  = DataFeed()
    strat= StrategyEngine(cfg["strategy"])
    emgr = None  # instantiate risk manager once you have starting capital
    execm= Execution()

    while True:
        for symbol in cfg["exchange"]["symbol"]:
            df = dfm.fetch_historical(symbol, cfg["exchange"]["timeframe_h"])
            df = IndicatorCalculator.run_all(df)
            sig = strat.generate_signal(df)
            price = df["close"].iloc[-1]
            # risk & execution
            if sig in ("buy","sell"):
                if emgr is None:
                    emgr = RiskManager(cfg["risk"]["capital"])
                size = emgr.position_size(price)
                sl, tp = emgr.apply_sl_tp(price)
                execm.execute(sig, price, size, sl, tp)
                logger.info(f"{sig.upper()} {symbol} at {price}")
        time.sleep(60 * 60)  # run hourly

if __name__ == "__main__":
    main()
