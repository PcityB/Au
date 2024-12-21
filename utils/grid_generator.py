import numpy as np

def create_template_grid(data, grid_rows, grid_cols):
    """Convert closing prices into a normalized template grid."""
    close_prices = data['Close'].values
    min_val, max_val = np.min(close_prices), np.max(close_prices)
    normalized = (close_prices - min_val) / (max_val - min_val)
    
    step = len(normalized) // (grid_rows * grid_cols)
    grid = [normalized[i:i+step].mean() for i in range(0, len(normalized), step)]
    return np.reshape(grid[:grid_rows * grid_cols], (grid_rows, grid_cols))
