### Option Prices
- **Call Price**: Price of a call option
- **Put Price**: Price of a put option  

### Greeks (Risk)
- **Delta**: Rate of change in option price with respect to stock price
- **Gamma**: Rate of change in delta with respect to stock price
- **Theta**: Rate of change in option price with respect to time (time decay)
- **Vega**: Rate of change in option price with respect to volatility
- **Rho**: Rate of change in option price with respect to interest rate

### Risk Metrics
- **Moneyness**: In-the-Money, At-the-Money, or Out-of-the-Money
- **Intrinsic Value**: The immediate value if exercised
- **Time Value**: The premium for time remaining
- **Daily Theta**: Daily time decay (theta/365)

## Math Stuff

Black-Scholes model assumes:
- European-style options (no early exercise)
- No dividend payments
- Constant volatility
- Risk-free interest rate
- Lognormal distribution of stock prices
- No transaction costs or taxes

### Important Formulas
- **Call Price**: C = S×N(d₁) - K×e^(-rT)×N(d₂)
- **Put Price**: P = K×e^(-rT)×N(-d₂) - S×N(-d₁)
- **d₁**: (ln(S/K) + (r + σ²/2)T) / (σ√T)
- **d₂**: d₁ - σ√T
