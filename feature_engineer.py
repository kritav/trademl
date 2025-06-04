import pandas as pd

def compute_features(prices):
    df = pd.DataFrame(index=prices.index)
    df['momentum_10'] = prices.pct_change(10)
    sma = prices.rolling(20).mean()
    std = prices.rolling(20).std()
    df['boll_pct'] = (prices - sma) / (2 * std)
    df['volatility'] = prices.rolling(20).std()
    df['target'] = prices.pct_change().shift(-1)
    return df.dropna()