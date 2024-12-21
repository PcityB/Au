import numpy as np

def backtest_strategy(data, patterns, initial_balance=10000, stop_loss_pips=10):
    """
    Backtest trading strategy using historical data and discovered patterns.
    :param data: Historical price data (validation set).
    :param patterns: Validated prototype patterns with forecasting power.
    :param initial_balance: Starting balance for the simulation.
    :param stop_loss_pips: Trailing stop-loss in pips.
    :return: Final balance after backtesting.
    """
    balance = initial_balance
    position = None  # Current position: "LONG", "SHORT", or None
    entry_price = None
    stop_loss = None

    for i in range(len(data) - len(patterns[0]["grid"])):
        # Extract current segment of data
        segment = data.iloc[i:i + len(patterns[0]["grid"])]
        signal = generate_trading_signal(segment, patterns)

        # Handle signals
        if signal == "ENTER LONG" and position != "LONG":
            position = "LONG"
            entry_price = segment["Close"].iloc[-1]
            stop_loss = entry_price - stop_loss_pips

        elif signal == "ENTER SHORT" and position != "SHORT":
            position = "SHORT"
            entry_price = segment["Close"].iloc[-1]
            stop_loss = entry_price + stop_loss_pips

        # Check trailing stop-loss
        current_price = segment["Close"].iloc[-1]
        if position == "LONG" and current_price < stop_loss:
            balance += (current_price - entry_price)
            position = None  # Close position
        elif position == "SHORT" and current_price > stop_loss:
            balance += (entry_price - current_price)
            position = None  # Close position

    return balance
