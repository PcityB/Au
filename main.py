from utils.data_loader import load_timeframe_data, split_data
from utils.grid_generator import create_template_grid
from utils.pattern_discovery import setup_ga, evolve_population
from utils.validation import validate_pattern
from utils.backtest import backtest_strategy
from utils.sql_analyzer import create_database, insert_pattern, query_patterns, resolve_conflicts
from utils.logger import logger
import config


def main():
    try:
        logger.info("Starting XAU/USD Pattern System...")

        # Load dataset for specific timeframes
        timeframes = ["5m", "15m", "1hr"]  # Specify desired timeframes
        data_dir = "data"  # Directory containing CSV files

        # Dynamically load timeframe-specific datasets
        loaded_data = load_timeframe_data(data_dir, timeframes)
        
        # Create SQLite database for storing patterns
        conn = create_database()
        logger.info("Database initialized.")

        # Process each timeframe's dataset
        for key, df in loaded_data.items():
            logger.info(f"Processing timeframe: {key}")

            # Split data into training and validation sets
            train_data, val_data = split_data(df)
            train_data.head()
            # Discover prototype patterns for each grid size
            toolbox = setup_ga()
            for rows, cols in config.GRID_SIZES:
                logger.info(f"Discovering patterns for grid size {rows}x{cols}...")

                # Create template grid from training data
                target_grid = create_template_grid(train_data, rows, cols)

                # Run genetic algorithm to discover the best pattern
                best_pattern = evolve_population(target_grid, toolbox)

                # Validate discovered pattern using training data
                accuracy = validate_pattern(best_pattern, train_data)

                if accuracy >= config.PREDICTION_ACCURACY_THRESHOLD:
                    logger.info(f"Pattern validated with accuracy {accuracy}%")

                    # Insert validated pattern into database with mock trend behavior (e.g., Bullish)
                    pic_code = str(best_pattern.flatten().tolist())  # Convert grid to PIC string format
                    insert_pattern(conn, f"{rows}x{cols}", key, pic_code,
                                   accuracy, True, "Bullish")  # Assuming forecasting power is True

                    logger.info("Pattern stored in database.")

            # Query patterns from database for backtesting
            logger.info(f"Querying validated patterns for {key} timeframe...")
            patterns = query_patterns(conn, f"{rows}x{cols}", key)

            if not patterns:
                logger.warning(f"No validated patterns found for {key}. Skipping backtesting.")
                continue

            # Resolve conflicts between multiple patterns firing simultaneously
            resolved_decision = resolve_conflicts(patterns)
            logger.info(f"Resolved decision: {resolved_decision}")

            if resolved_decision != "CONFLICT":
                # Backtest strategy using validation data and discovered patterns
                final_balance = backtest_strategy(val_data.reset_index(drop=True), patterns)
                logger.info(f"Final Balance after backtesting ({key}): ${final_balance:.2f}")
            else:
                logger.warning(f"Conflict detected in {key}. No trades executed.")

        logger.info("XAU/USD Pattern System completed successfully.")

    except Exception as e:
        logger.error(f"An error occurred during execution: {e}", exc_info=True)


if __name__ == "__main__":
    main()
