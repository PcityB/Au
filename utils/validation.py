from utils.similarity import calculate_similarity # Import the similarity function
from utils.grid_generator import create_template_grid # Ensure this is available
import config

def validate_pattern(pattern_grid, data):
    """
    Validate a prototype pattern using multi-predicate instances.
    :param pattern_grid: The prototype pattern grid to validate.
    :param data: Historical data to validate against.
    :return: Validation accuracy as a percentage.
    """
    predicates = [
        {"periods": 5, "pips": 10},
        {"periods": 10, "pips": 20},
        {"periods": 20, "pips": 30},
    ]
    
    valid_count = 0
    total_count = len(data) - len(pattern_grid[0]) # Total possible matches

    for i in range(total_count):
        # Extract a segment of the data matching the grid size
        segment = data.iloc[i:i + len(pattern_grid[0])]
        
        # Create a template grid for the segment
        segment_grid = create_template_grid(segment, pattern_grid.shape[0], pattern_grid.shape[1])
        
        # Calculate similarity with the prototype pattern
        similarity = calculate_similarity(segment_grid, pattern_grid)

        # Check if similarity meets the threshold
        if similarity <= config.SIMILARITY_THRESHOLD:
            for pred in predicates:
                future_segment = data.iloc[i + len(pattern_grid[0]):i + len(pattern_grid[0]) + pred["periods"]]
                if not future_segment.empty: # Ensure there is enough future data
                    if future_segment["High"].max() - future_segment["Low"].min() >= pred["pips"]:
                        valid_count += 1
                        break # Stop checking predicates once one is satisfied

    # Calculate accuracy as a percentage
    accuracy = (valid_count / total_count) * 100 if total_count > 0 else 0
    return accuracy