"""通用工具：时区、SQLite 操作与日志初始化（示例实现）。"""
import sqlite3
import logging
from pathlib import Path
import pytz
from datetime import datetime

EASTERN = pytz.timezone('US/Eastern')


def now_eastern():
    return datetime.now(EASTERN)


def ensure_dirs():
    Path('data').mkdir(exist_ok=True)
    Path('reports').mkdir(exist_ok=True)
    Path('logs').mkdir(exist_ok=True)


def get_db_conn(path='data/cache.sqlite'):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES)
    return conn


def setup_logging(level_console=logging.INFO, level_file=logging.DEBUG, logfile='logs/latest.log'):
    ensure_dirs()
    logger = logging.getLogger()
    logger.setLevel(min(level_console, level_file))
    for h in list(logger.handlers):
        logger.removeHandler(h)
    ch = logging.StreamHandler()
    ch.setLevel(level_console)
    fmt = logging.Formatter('%(asctime)s %(name)s %(levelname)s: %(message)s')
    ch.setFormatter(fmt)
    logger.addHandler(ch)
    fh = logging.FileHandler(logfile, mode='w', encoding='utf-8')
    fh.setLevel(level_file)
    fh.setFormatter(fmt)
    logger.addHandler(fh)
    return logger
