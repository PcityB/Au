import os
import pandas as pd
from utils.logger import logger  # Reuse the logging utility

def list_timeframe_files(directory, pattern="XAU_"):
    """
    List all CSV files in a directory that match a specific pattern.
    
    :param directory: Path to the directory containing CSV files.
    :param pattern: Pattern to match in filenames (default is "XAU_").
    :return: List of matching file paths.
    """
    try:
        logger.info(f"Listing CSV files in directory: {directory} with pattern: {pattern}")
        files = [os.path.join(directory, f) for f in os.listdir(directory) if f.startswith(pattern) and f.endswith(".csv")]
        logger.info(f"Found {len(files)} matching files.")
        return files
    except Exception as e:
        logger.error(f"Error listing files in directory {directory}: {e}", exc_info=True)
        raise

def load_csv_files(file_paths):
    """
    Load multiple CSV files into a dictionary of DataFrames.
    
    :param file_paths: List of file paths to load.
    :return: Dictionary where keys are filenames (without extension) and values are DataFrames.
    """
    data_frames = {}
    for file_path in file_paths:
        try:
            logger.info(f"Loading file: {file_path}")
            df = pd.read_csv(file_path)
            key = os.path.splitext(os.path.basename(file_path))[0]  # Use filename without extension as key
            data_frames[key] = df
            logger.info(f"Loaded {file_path} with shape {df.shape}")
        except Exception as e:
            logger.error(f"Error loading file {file_path}: {e}", exc_info=True)
            raise
    return data_frames

def load_timeframe_data(directory, timeframes):
    """
    Load data for specific timeframes from the directory.
    
    :param directory: Path to the directory containing CSV files.
    :param timeframes: List of timeframes to load (e.g., ["5m", "15m", "1hr"]).
    :return: Dictionary of DataFrames for each requested timeframe.
    """
    try:
        logger.info(f"Loading data for timeframes: {timeframes}")
        all_files = list_timeframe_files(directory)
        selected_files = [f for f in all_files if any(tf in f for tf in timeframes)]
        return load_csv_files(selected_files)
    except Exception as e:
        logger.error(f"Error loading timeframe data: {e}", exc_info=True)
        raise

def resample_data(data, timeframe):
    """
    Resample data to specified timeframe (if needed).
    
    :param data: Pandas DataFrame with raw price data.
    :param timeframe: Desired timeframe for resampling (e.g., '5T', '15T').
    :return: Resampled DataFrame.
    """
    try:
        logger.info(f"Resampling data to timeframe: {timeframe}")
        resampled = data.resample(timeframe).agg({
            'Open': 'first',
            'High': 'max',
            'Low': 'min',
            'Close': 'last'
        }).dropna()
        logger.info(f"Resampled data shape: {resampled.shape}")
        return resampled
    except Exception as e:
        logger.error(f"Error resampling data to timeframe {timeframe}: {e}", exc_info=True)
        raise

def split_data(data):
    """
    Split data into training (2004-2020) and validation (2021-2024) sets.
    
    :param data: Pandas DataFrame with historical price data.
    :return: Tuple of training and validation DataFrames.
    """
    try:
        # Ensure the index is converted to datetime if not already
        if not isinstance(data.index, pd.DatetimeIndex):
            logger.info("Converting index to DatetimeIndex...")
            data.index = pd.to_datetime(data.index)

        # Perform slicing using datetime strings
        train_data = data['2004':'2020']
        val_data = data['2021':'2024']
        
        logger.info(f"Split data into training ({train_data.shape}) and validation ({val_data.shape}) sets.")
        return train_data, val_data
    except Exception as e:
        logger.error("Error splitting data into training and validation sets.", exc_info=True)
        raise

