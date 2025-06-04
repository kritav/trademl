from src.data_collector import download_data
from src.feature_engineer import compute_features
from src.strategy import MomentumModel
from src.simulator import run_backtest, compare_to_benchmark
from src.utils import train_test_split

import matplotlib.pyplot as plt

def main():
    stock = 'AAPL'
    benchmark = 'SPY'
    data = download_data([stock, benchmark])

    prices = data[stock]
    features = compute_features(prices)

    X = features.drop('target', axis=1)
    y = features['target']
    X_train, X_test, y_train, y_test = train_test_split(X, y)

    model = MomentumModel()
    model.train(X_train, y_train)

    preds = model.predict(X_test)

    strategy_returns = run_backtest(preds, y_test)
    spy_returns = data[benchmark].pct_change().shift(-1).loc[y_test.index]

    compare_to_benchmark(strategy_returns, spy_returns)
    plt.show()

if __name__ == "__main__":
    main()