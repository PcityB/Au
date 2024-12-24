import numpy as np

def calculate_similarity(grid1, grid2):
    """
    Calculate similarity between two grids using absolute differences.
    :param grid1: First grid (numpy array).
    :param grid2: Second grid (numpy array).
    :return: Similarity score (lower is better).
    """
    try:
        # Ensure both grids have the same shape
        if grid1.shape != grid2.shape:
            raise ValueError("Grid shapes do not match for similarity calculation.")

        # Calculate absolute differences and sum them
        similarity_score = np.sum(np.abs(grid1 - grid2))
        return similarity_score
    except Exception as e:
        raise ValueError(f"Error calculating similarity: {e}")