"""最小示例回测：读取 SQLite 数据，生成简单报告（模板）。"""
import sqlite3
import pandas as pd
from pathlib import Path

def load_df(ticker, db_path='data/cache.sqlite'):
    conn = sqlite3.connect(db_path)
    table = ticker.replace('.','_')
    df = pd.read_sql_query(f'SELECT * FROM "{table}"', conn, parse_dates=['Datetime'])
    conn.close()
    return df


def generate_report(summary, report_path='reports/latest.md'):
    Path('reports').mkdir(exist_ok=True)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('# 回测报告（示例）\n\n')
        f.write('## 摘要\n\n')
        f.write('| 项目 | 值 |\n')
        f.write('|---:|---:|\n')
        for k,v in summary.items():
            f.write(f'| {k} | {v} |\n')

if __name__ == '__main__':
    print('示例回测脚本：请替换为实际回测逻辑')
