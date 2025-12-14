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

    # CRITICAL: Strip whitespace before trying conversion
  value_str = str(value_str).strip()
  if value_str == "":
    return False, "Please enter a number."

  try:
    val = float(value_str)
  except ValueError:
    return False, "Please enter a valid number."

  if require_integer and not val.is_integer():
    return False, "Only whole numbers are allowed."

    # Convert to integer if required for clean saving
  val_final = int(val) if require_integer else val 

  if val_final < min_val or val_final > max_val:
    return False, f"Value must be between {min_val} and {max_val}."

    # Return True and the cleaned numeric value
  return True, val_final


# -----------------------------
# STRESS CALCULATION (Example - kept for completeness)
# -----------------------------
def calculate_total_stress():
  for key, val in user_data.items():
    if val is None and key != 'current_situation': # Exclude current_situation from required check
      raise ValueError("All stress questions must be answered.")

    # ... (rest of your calculation logic here) ...
    # Placeholder return for demonstration
  return 50.0