from strategies.sma_crossover import SMACrossover

def get_strategy(strategy_name):
    strategies = {
        "sma_crossover": SMACrossover,
    }
    return strategies.get(strategy_name, None)
