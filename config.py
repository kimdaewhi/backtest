STRATEGY_CONFIGS = {
    "sma_crossover": {
        "ticker": "ORCL",
        "start_date": "2018-01-01",
        "end_date": "2018-12-31",
        "initial_cash": 1500,
        "params": {"short_period": 10, "long_period": 50}
    },
    "rsi_strategy": {
        "ticker": "TSLA",
        "start_date": "2020-01-01",
        "end_date": "2024-01-01",
        "initial_cash": 5000,
        "params": {"rsi_period": 14, "rsi_overbought": 70, "rsi_oversold": 30}
    },
}
