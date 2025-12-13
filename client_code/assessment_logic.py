# --- assessment_logic module ---

import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import math

# --- GLOBAL STORAGE (For all your answers) ---
user_data = {
  "sleep_hours": 7,          
  "daily_exercise_mins": 30, 
  "screen_time_hours": 4,    
  "diet_quality_1_10": 5,
  "productivity_score_1_10": 5,
  "mood_level_1_10": 5
}

# --- VALIDATION UTILITY ---
def validate_input(value_str, min_val, max_val):
  """
    Checks if a string input is a valid number within the min/max range.
    Returns (True, numeric_value) on success, or (False, error_message) on failure.
    """
  if not value_str:
    return (False, "Please enter a value.")

  try:
    # Try to convert to float/int
    val = float(value_str)
    if val == int(val):
      val = int(val) # Keep as int if it's a whole number

  except ValueError:
    return (False, "Input must be a number.")

  if min_val <= val <= max_val:
    return (True, val)
  else:
    return (False, f"Value must be between {min_val} and {max_val}.")


# --- FEEDBACK UTILITY (For individual forms if needed) ---
def get_feedback(val, min_val, max_val):
  """Provides generic immediate feedback based on where the score falls."""
  range_size = max_val - min_val
  low_threshold = min_val + (range_size * 0.3)
  high_threshold = max_val - (range_size * 0.3)

  if val <= low_threshold:
    return {"color": "#F44336", "msg": "High Risk"}
  elif val >= high_threshold:
    return {"color": "#4CAF50", "msg": "Healthy/Positive"}
  else:
    return {"color": "#FF9800", "msg": "Moderate/Average"}


# --- FINAL CALCULATION (Keep for later) ---
def calculate_total_stress():
  # ... (Your complex calculation logic remains here, unchanged) ...
  pass 

def get_result_feedback(final_score):
  # ... (Your final result classification remains here, unchanged) ...
  pass