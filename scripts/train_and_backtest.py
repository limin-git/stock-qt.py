"""示例训练与回测流程（模板）：读取特征 CSV，训练 LightGBM，生成简单回测统计并写报告。"""
import pandas as pd
import lightgbm as lgb
from pathlib import Path
from scripts.utils import setup_logging, now_eastern
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import roc_auc_score

logger = setup_logging()


def train_model(feature_csv, target_col='target', model_path='models/lgb_model.txt'):
    Path('models').mkdir(exist_ok=True)
    df = pd.read_csv(feature_csv, parse_dates=['Datetime'], index_col='Datetime')
    if target_col not in df.columns:
        logger.error('target column not in features')
        return None
    X = df.drop(columns=[target_col])
    y = df[target_col]
    tscv = TimeSeriesSplit(n_splits=5)
    models = []
    for train_idx, val_idx in tscv.split(X):
        X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
        y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]
        lgb_train = lgb.Dataset(X_train, y_train)
        lgb_val = lgb.Dataset(X_val, y_val, reference=lgb_train)
        params = {'objective':'binary','metric':'auc','verbosity':-1}
        gbm = lgb.train(params, lgb_train, num_boost_round=100, valid_sets=[lgb_val], early_stopping_rounds=10, verbose_eval=False)
        models.append(gbm)
        logger.info('fold auc: %.4f', gbm.best_score['valid_0']['auc'])
    models[0].save_model(model_path)
    return model_path


def simple_backtest(feature_csv, threshold=0.6):
    df = pd.read_csv(feature_csv, parse_dates=['Datetime'], index_col='Datetime')
    df = df.sort_index()
    if 'score' not in df.columns or 'close' not in df.columns:
        logger.error('required columns missing')
        return {}
    df['signal'] = (df['score'] > threshold).astype(int)
    df['strategy_ret'] = df['signal'].shift(1) * df['close'].pct_change().fillna(0)
    summary = {
        'start': str(df.index.min()),
        'end': str(df.index.max()),
        'total_return': (1+df['strategy_ret']).prod()-1,
        'trades': int(df['signal'].sum()),
        'avg_hold_days': 1
    }
    return summary


def write_report(summary):
    Path('reports').mkdir(exist_ok=True)
    with open('reports/latest.md','w',encoding='utf-8') as f:
        f.write('# 回测报告（示例）\n\n')
        f.write('## 摘要\n\n')
        f.write('| 项目 | 值 |\n')
        f.write('|---:|---:|\n')
        for k,v in summary.items():
            f.write(f'| {k} | {v} |\n')

if __name__ == '__main__':
    print('示例：train_model("data/SPY_features.csv")')
