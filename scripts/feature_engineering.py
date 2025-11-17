"""示例特征工程：从 SQLite 加载数据，构造日级与周内聚合特征并保存回 SQLite 或 CSV（模板）。"""
import pandas as pd
from scripts.utils import get_db_conn, now_eastern


def build_daily_features(ticker, db_path='data/cache.sqlite'):
    conn = get_db_conn(db_path)
    table = ticker.replace('.', '_')
    df = pd.read_sql_query(f'SELECT * FROM "{table}"', conn, parse_dates=['Datetime'])
    conn.close()
    if df.empty:
        return None
    df = df.sort_values('Datetime')
    df.set_index('Datetime', inplace=True)
    res = pd.DataFrame()
    res['close'] = df['Close']
    res['ret_1d'] = res['close'].pct_change(1)
    res['ret_5d'] = res['close'].pct_change(5)
    res['vol_20'] = res['ret_1d'].rolling(20).std()
    res['ema_5'] = res['close'].ewm(span=5).mean()
    res['rsi_14'] = compute_rsi(res['close'], 14)
    res = res.dropna()
    out_path = f'data/{ticker}_features.csv'
    res.to_csv(out_path)
    return out_path


def compute_rsi(series, period=14):
    delta = series.diff()
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)
    ma_up = up.ewm(alpha=1/period, adjust=False).mean()
    ma_down = down.ewm(alpha=1/period, adjust=False).mean()
    rs = ma_up / ma_down
    rsi = 100 - (100 / (1 + rs))
    return rsi

if __name__ == '__main__':
    print('示例：build_daily_features("SPY")')
