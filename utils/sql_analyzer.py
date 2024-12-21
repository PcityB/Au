import sqlite3

def create_database(db_name="patterns.db"):
    """Create SQLite database for storing prototype patterns."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS PrototypePatterns (
            Pattern_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Grid_Size TEXT,
            Time_Frame TEXT,
            PIC TEXT,
            Prediction_Accuracy REAL,
            Forecasting_Power BOOLEAN,
            Trend_Behavior TEXT  -- Bullish, Bearish, or NoTrend
        )
    """)
    conn.commit()
    return conn

def insert_pattern(conn, grid_size, time_frame, pic, accuracy, forecasting_power, trend_behavior):
    """Insert a discovered pattern into the database."""
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO PrototypePatterns (Grid_Size, Time_Frame, PIC, Prediction_Accuracy, Forecasting_Power, Trend_Behavior)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (grid_size, time_frame, pic, accuracy, forecasting_power, trend_behavior))
    conn.commit()

def query_patterns(conn, grid_size, time_frame):
    """Query database for matching prototype patterns."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM PrototypePatterns WHERE Grid_Size = ? AND Time_Frame = ?
    """, (grid_size, time_frame))
    return cursor.fetchall()

def resolve_conflicts(patterns):
    """
    Resolve conflicts when multiple patterns fire simultaneously.
    Rules:
      - If all patterns agree on "ENTER LONG" or "ENTER SHORT," use that decision.
      - If there's a conflict (some say "ENTER LONG," others "ENTER SHORT"), return "CONFLICT."
      - If all patterns say "NOT TRADE," return "NOT TRADE."
    """
    decisions = [pattern[-1] for pattern in patterns]  # Extract Trend_Behavior column
    
    if all(decision == "Bullish" for decision in decisions):
        return "ENTER LONG"
    elif all(decision == "Bearish" for decision in decisions):
        return "ENTER SHORT"
    elif all(decision == "NoTrend" for decision in decisions):
        return "NOT TRADE"
    
    return "CONFLICT"
