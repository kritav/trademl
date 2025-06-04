import pandas as pd

def run_backtest(predictions, returns, threshold=0.001):
    signals = predictions > threshold
    strategy_returns = returns[signals]
    return strategy_returns

def compare_to_benchmark(strategy_returns, benchmark_returns):
    df = pd.DataFrame({
        'Strategy': strategy_returns.cumsum(),
        'SPY': benchmark_returns.cumsum()
    })
    df.plot(title="Strategy vs SPY Cumulative Returns", figsize=(10, 5))
import numpy as np
import matplotlib.pyplot as plt

def monte_carlo_simulation(start_price, mu, sigma, days=252, simulations=1000):
    dt = 1 / days
    results = np.zeros((days, simulations))
    for i in range(simulations):
        price = start_price
        for d in range(days):
            shock = np.random.normal(loc=mu * dt, scale=sigma * np.sqrt(dt))
            price *= (1 + shock)
            results[d, i] = price
    return results

def plot_simulations(results):
    plt.figure(figsize=(10, 6))
    plt.plot(results)
    plt.title("Monte Carlo Simulated Price Paths")
    plt.xlabel("Days")
    plt.ylabel("Price")
    plt.show()
import numpy as np
import matplotlib.pyplot as plt
from ruptures import detect

def detect_changepoints(prices, model="l2", penalty=3):
    import ruptures as rpt
    algo = rpt.Pelt(model=model).fit(prices.values)
    result = algo.predict(pen=penalty)
    return result

def plot_changepoints(prices, changepoints):
    import ruptures as rpt
    rpt.display(prices.values, changepoints)
    plt.title("Changepoint Detection")
    plt.show()