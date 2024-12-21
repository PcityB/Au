import kagglehub
import os
import logging

def download_dataset(dataset_name, output_dir="data"):
    """
    Download a Kaggle dataset using kagglehub and extract it to the specified directory.
    
    :param dataset_name: The Kaggle dataset identifier (e.g., "novandraanugrah/xauusd-gold-price-historical-data-2004-2024").
    :param output_dir: The directory where the dataset will be extracted.
    """
    try:
        # Ensure output directory exists
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Use kagglehub to download the dataset
        logging.info(f"Downloading dataset: {dataset_name}")
        path = kagglehub.dataset_download(dataset_name, path=output_dir)
        
        logging.info(f"Dataset downloaded successfully to: {path}")
        return path
    except Exception as e:
        logging.error(f"Failed to download dataset: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    # Example usage
    DATASET_NAME = "novandraanugrah/xauusd-gold-price-historical-data-2004-2024"
    OUTPUT_DIR = "data"
    
    logging.basicConfig(level=logging.INFO)
    
    try:
        download_path = download_dataset(DATASET_NAME, OUTPUT_DIR)
        print(f"Dataset downloaded and extracted to: {download_path}")
    except Exception as e:
        print(f"Error: {e}")
