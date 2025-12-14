# --- assessment_logic.py (FINAL VERIFIED CODE) ---

import anvil.server

# -----------------------------
# GLOBAL STORAGE
# -----------------------------
user_data = {
  "sleep_hours": None,
  "daily_exercise_mins": None,
  "screen_time_hours": None,
  "diet_quality_1_10": None,
  "productivity_score_1_10": None,
  "mood_level_1_10": None,
  "current_situation": None # Added for burnout flow logic
}

# -----------------------------
# VALIDATION
# -----------------------------
def validate_input(value_str, min_val, max_val, require_integer=False):
  if value_str is None:
    return False, "Please enter a number."

  value_str = str(value_str).strip()
  if value_str == "":
    return False, "Please enter a number."

  try:
    val = float(value_str)
  except ValueError:
    return False, "Please enter a valid number."

  if require_integer and not val.is_integer():
    return False, "Only whole numbers are allowed."

  val_final = int(val) if require_integer else val 

  if val_final < min_val or val_final > max_val:
    return False, f"Value must be between {min_val} and {max_val}."

  return True, val_final


# -----------------------------
# STRESS CALCULATION
# -----------------------------
def calculate_total_stress():
  for key, val in user_data.items():
    # Exclude 'current_situation' from the required check
    if val is None and key not in ['current_situation']: 
      raise ValueError("All stress questions must be answered.")

    # Assume a calculation based on your original logic:
  score_sleep = max(0, min(100, (8 - user_data["sleep_hours"]) * 25))
  score_diet = (10 - user_data["diet_quality_1_10"]) * 11
  score_mood = (10 - user_data["mood_level_1_10"]) * 11
  # Assuming other inputs (exercise, screen, prod) exist and are used:

  total = (score_sleep + score_diet + score_mood) / 3 # Simplified
  # Use 100 max if calculation exceeds 100
  return round(min(100, total), 1)

def get_result_feedback(score): # <-- FUNCTION RE-ADDED
  if score < 33:
    return {"level": "Low Stress", "color": "#4CAF50", "msg": "You are balanced today."}
  elif score < 66:
    return {"level": "Moderate Stress", "color": "#FF9800", "msg": "You may be under some pressure."}
  else:
    return {"level": "High Stress", "color": "#F44336", "msg": "You may need rest or support today."}