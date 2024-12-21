import pandas as pd

def load_data(file_path):
    """Load XAU/USD dataset."""
    data = pd.read_csv(file_path, parse_dates=['Date'], index_col='Date')
    data = data[['Open', 'High', 'Low', 'Close']]  # Keep only relevant columns
    return data

def resample_data(data, timeframe):
    """Resample data to specified timeframe."""
    resampled = data.resample(timeframe).agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',
        'Close': 'last'
    }).dropna()
    return resampled

def split_data(data):
    """Split data into training (2004-2020) and validation (2021-2024)."""
    train_data = data['2004':'2020']
    val_data = data['2021':'2024']
    return train_data, val_data
