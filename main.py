from utils.data_loader import load_data, resample_data, split_data
from utils.grid_generator import create_template_grid
from utils.pattern_discovery import setup_ga, evolve_population
from utils.validation import validate_pattern
from utils.backtest import backtest_strategy
from utils.sql_analyzer import create_database, insert_pattern, query_patterns, resolve_conflicts
from utils.dataset_downloader import download_dataset
from utils.logger import logger

import config
import os

def main():
    try:
        logger.info("Starting XAU/USD Pattern System...")
        
        # Check if dataset exists; if not, download it
        dataset_path = os.path.join("data", "XAUUSD_Historical_Data.csv")
        if not os.path.exists(dataset_path):
            logger.info("Dataset not found locally. Downloading...")
            download_dataset("novandraanugrah/xauusd-gold-price-historical-data-2004-2024", "data")
        
        # Load dataset
        raw_data = load_data(dataset_path)
        logger.info("Data loaded successfully.")

        # Create SQLite database for storing patterns
        conn = create_database()
        logger.info("Database initialized.")

        # Process each timeframe
        for tf_code, tf_name in config.TIMEFRAMES.items():
            logger.info(f"Processing {tf_name} timeframe...")
            
            # Resample data to the current timeframe
            resampled_data = resample_data(raw_data, tf_code)
            
            # Split into training and validation sets
            train_data, val_data = split_data(resampled_data)

            # Discover prototype patterns for each grid size
            toolbox = setup_ga()
            for rows, cols in config.GRID_SIZES:
                logger.info(f"Discovering patterns for grid size {rows}x{cols}...")
                
                target_grid = create_template_grid(train_data, rows, cols)
                best_pattern = evolve_population(target_grid, toolbox)
                
                # Validate discovered pattern
                accuracy = validate_pattern(best_pattern, train_data)
                
                if accuracy >= config.PREDICTION_ACCURACY_THRESHOLD:
                    logger.info(f"Pattern validated with accuracy {accuracy}%")
                    
                    # Insert pattern into database with trend behavior (mocked as Bullish here)
                    pic_code = str(best_pattern.flatten().tolist())  # Convert grid to PIC string format
                    insert_pattern(conn, f"{rows}x{cols}", tf_name, pic_code,
                                   accuracy, True, "Bullish")  # Assuming forecasting power is True
                    
                    logger.info("Pattern stored in database.")

            # Query patterns from database for backtesting
            logger.info(f"Querying validated patterns for {tf_name} timeframe...")
            patterns = query_patterns(conn, f"{rows}x{cols}", tf_name)

            if not patterns:
                logger.warning(f"No validated patterns found for {tf_name}. Skipping backtesting.")
                continue

            resolved_decision = resolve_conflicts(patterns)
            logger.info(f"Resolved decision: {resolved_decision}")

            if resolved_decision != "CONFLICT":
                final_balance = backtest_strategy(val_data.reset_index(drop=True), patterns)
                logger.info(f"Final Balance after backtesting ({tf_name}): ${final_balance:.2f}")
            else:
                logger.warning(f"Conflict detected in {tf_name}. No trades executed.")

        logger.info("XAU/USD Pattern System completed successfully.")

    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)

if __name__ == "__main__":
    main()
