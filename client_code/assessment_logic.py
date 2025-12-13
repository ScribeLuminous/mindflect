# --- assessment_logic module ---

import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import math

# --- GLOBAL STORAGE (For all your answers) ---
user_data = {
  "sleep_hours": 0,          # Must be key: value pair
  "daily_exercise_mins": 0, 
  "screen_time_hours": 0,    
  "diet_quality_1_10": 1,
  "productivity_score_1_10": 1,
  "mood_level_1_10": 1
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


# --- FINAL CALCULATION ---
def calculate_total_stress():
  """
  Normalizes all inputs to a 0-100 Stress Scale and returns the average.
  0 = Zen/Relaxed, 100 = Maximum Stress
  """
  data = user_data 

  # 1. Sleep Logic (Inverse)
  val_sleep = float(data['sleep_hours'])
  score_sleep = max(0, min(100, (8 - val_sleep) * 25))

  # 2. Exercise Logic (Inverse)
  val_exercise = float(data['daily_exercise_mins'])
  score_exercise = max(0, min(100, (60 - val_exercise) * 1.6))

  # 3. Screen Time Logic (Direct)
  val_screen = float(data['screen_time_hours'])
  score_screen = max(0, min(100, (val_screen / 12) * 100))

  # 4. Subjective Scales (Inverse: 10 is 0 stress)
  score_diet = (10 - data['diet_quality_1_10']) * 11
  score_prod = (10 - data['productivity_score_1_10']) * 11
  score_mood = (10 - data['mood_level_1_10']) * 11

  # Average
  total_score = (score_sleep + score_exercise + score_screen + score_diet + score_prod + score_mood) / 6
  return round(total_score, 1)

def get_result_feedback(final_score):
  """Returns the text label and color based on the total score thresholds."""
  if final_score < 33:
    return {"level": "Low Stress", "color": "#4CAF50", "msg": "You are balanced."}
  elif final_score < 66:
    return {"level": "Moderate Stress", "color": "#FF9800", "msg": "You are under pressure."}
  else:
    return {"level": "High Stress", "color": "#F44336", "msg": "Critical levels detected."}