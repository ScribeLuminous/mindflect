# --- assessment_logic.py ---

import anvil.server

# -----------------------------
# GLOBAL STORAGE (NO DEFAULTS)
# -----------------------------
user_data = {
  "sleep_hours": None,
  "daily_exercise_mins": None,
  "screen_time_hours": None,
  "diet_quality_1_10": None,
  "productivity_score_1_10": None,
  "mood_level_1_10": None
}

# -----------------------------
# VALIDATION (FINAL, SAFE)
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

  val = int(val) if require_integer else val

  if val < min_val or val > max_val:
    return False, f"Value must be between {min_val} and {max_val}."

  return True, val


# -----------------------------
# STRESS CALCULATION (0–100%)
# -----------------------------
def calculate_total_stress():
  for key, val in user_data.items():
    if val is None:
      raise ValueError("All questions must be answered.")

  score_sleep = max(0, min(100, (8 - user_data["sleep_hours"]) * 25))
  score_exercise = max(0, min(100, (60 - user_data["daily_exercise_mins"]) * 1.6))
  score_screen = max(0, min(100, (user_data["screen_time_hours"] / 16) * 100))

  score_diet = (10 - user_data["diet_quality_1_10"]) * 11
  score_prod = (10 - user_data["productivity_score_1_10"]) * 11
  score_mood = (10 - user_data["mood_level_1_10"]) * 11

  total = (
    score_sleep +
    score_exercise +
    score_screen +
    score_diet +
    score_prod +
    score_mood
  ) / 6

  return round(total, 1)


def get_result_feedback(score):
  if score < 33:
    return {"level": "Low Stress", "color": "#4CAF50", "msg": "You are balanced today."}
  elif score < 66:
    return {"level": "Moderate Stress", "color": "#FF9800", "msg": "You may be under some pressure."}
  else:
    return {"level": "High Stress", "color": "#F44336", "msg": "You may need rest or support today."}
