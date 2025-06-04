# Momentum Trading Strategy

A momentum-based trading strategy using machine learning, Bollinger Bands, and performance comparison against the SPY index.

## Features

- Monte Carlo Simulation for forecasting future prices
- Changepoint Detection for trend shifts

- Data collection with Yahoo Finance
- Feature engineering (momentum, Bollinger %, volatility)
- Machine Learning using Random Forest
- Simple backtesting engine
- Monte Carlo & changepoint analysis (planned)

## To Run

```bash
pip install -r requirements.txt
python main.py
```

## Monte Carlo Simulation

```python
from src.simulator import monte_carlo_simulation, plot_simulations
results = monte_carlo_simulation(start_price=100, mu=0.05, sigma=0.2)
plot_simulations(results)
```

## Changepoint Detection

```python
from src.simulator import detect_changepoints, plot_changepoints
changepoints = detect_changepoints(prices)
plot_changepoints(prices, changepoints)
```

---

## GitHub-Ready Checklist

- [x] Clear folder structure
- [x] Modular code with `src/`
- [x] Jupyter-friendly with `notebook/`
- [x] Readable `README.md`
- [x] Extensible for more models
