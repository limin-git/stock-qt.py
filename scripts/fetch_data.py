"""示例：从 Yahoo 获取历史日线数据并写入 SQLite（示例，仅作模板）。"""
import sqlite3
import pandas as pd
import yfinance as yf
from datetime import datetime

def fetch_and_store(ticker, db_path='data/cache.sqlite'):
    df = yf.download(ticker, period='5y', interval='1d')
    if df.empty:
        return 0
    df.reset_index(inplace=True)
    df['Datetime'] = df['Date'].dt.tz_localize('UTC').dt.tz_convert('US/Eastern')
    df = df.rename(columns={'Date':'date'})
    conn = sqlite3.connect(db_path)
    df.to_sql(ticker.replace('.','_'), conn, if_exists='append', index=False)
    conn.close()
    return len(df)

if __name__ == '__main__':
    print('示例：fetch_and_store("SPY")')
