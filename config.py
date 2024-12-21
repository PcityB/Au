# Configuration constants

# File paths
DATA_FILE = "data/xauusd_data.csv"

# Timeframes to process
TIMEFRAMES = {"5T": "5-Minute", "30T": "30-Minute", "1H": "1-Hour"}

# Grid dimensions for prototype patterns
GRID_SIZES = [(10, 10), (15, 10), (20, 15), (25, 15)]

# Genetic Algorithm parameters
POP_SIZE = 100  # Population size
GENS = 50       # Number of generations
MUTATION_RATE = 0.2
CROSSOVER_RATE = 0.5

# Validation thresholds
SIMILARITY_THRESHOLD = 60  # Minimum similarity for pattern match
PREDICTION_ACCURACY_THRESHOLD = 60  # Minimum prediction accuracy (%)
