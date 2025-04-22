import yaml
import logging

def load_config(path="config.yml"):
    with open(path) as f:
        return yaml.safe_load(f)

def setup_logger(name):
    logger = logging.getLogger(name)
    level = logging.INFO
    logger.setLevel(level)
    ch = logging.StreamHandler()
    ch.setLevel(level)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger
