def validate_pattern(pattern_grid, data):
    """Validate a prototype pattern using multi-predicate instances."""
    predicates = [
        {"periods": 5, "pips": 10},
        {"periods": 10, "pips": 20},
        {"periods": 20, "pips": 30},
    ]
    
    valid_count = 0
    total_count = len(data) - len(pattern_grid[0])

    for i in range(total_count):
        segment = data[i:i + len(pattern_grid[0])]
        similarity = calculate_similarity(create_template_grid(segment), pattern_grid)

        if similarity > SIMILARITY_THRESHOLD:
            valid_count += sum(
                future_segment["High"].max() - future_segment["Low"].min() >= pred["pips"]
                for pred in predicates)

            accuracy = (valid_count / total_count) * 100 if total_count > else None.
