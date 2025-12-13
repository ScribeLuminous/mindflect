# --- assessment_logic module ---

import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import math

# --- GLOBAL STORAGE ---
user_data = {
  "sleep_hours": 0,
  "daily_exercise_mins": 0,
  "screen_time_hours": 0,
  "diet_quality_1_10": 1,
  "productivity_score_1_10": 1,
  "mood_level_1_10": 1
}

# --- VALIDATION UTILITY ---
def validate_input(value_str, min_val, max_val):
  if value_str == 0 or value_str.strip() == "":
    return (False, "Please enter a number.")

  if not value_str.isdigit():
    return (False, "Only whole numbers are allowed.")

  val = int(value_str)

  if val < min_val or val > max_val:
    return (False, f"Value must be between {min_val} and {max_val}.")

  return (True, val)


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
  Calculates stress ONLY if all inputs are present.
  """
  data = user_data

  # 🔒 Guard clause
  for key, val in data.items():
    if val is None:
      raise ValueError("All questions must be answered before calculating stress.")

  # ---- NORMALIZED SCORING ----

  # 1. Sleep (inverse)
  score_sleep = max(0, min(100, (8 - data['sleep_hours']) * 25))

  # 2. Exercise (inverse)
  score_exercise = max(0, min(100, (60 - data['daily_exercise_mins']) * 1.6))

  # 3. Screen time (direct, corrected to 16h max)
  score_screen = max(0, min(100, (data['screen_time_hours'] / 16) * 100))

  # 4–6. Subjective scales
  score_diet = (10 - data['diet_quality_1_10']) * 11
  score_prod = (10 - data['productivity_score_1_10']) * 11
  score_mood = (10 - data['mood_level_1_10']) * 11

  total_score = (
    score_sleep +
    score_exercise +
    score_screen +
    score_diet +
    score_prod +
    score_mood
  ) / 6

  return round(total_score, 1)


def get_result_feedback(final_score):
  """Returns the text label and color based on the total score thresholds."""
  if final_score < 33:
    return {"level": "Low Stress", "color": "#4CAF50", "msg": "You are balanced."}
  elif final_score < 66:
    return {"level": "Moderate Stress", "color": "#FF9800", "msg": "You are under pressure."}
  else:
    return {"level": "High Stress", "color": "#F44336", "msg": "Critical levels detected."}


@anvil.server.callable
def save_daily_stress(score, level, inputs):
  user = anvil.users.get_user()
  if not user:
    raise Exception("User not logged in")

  app_tables.stress_logs.add_row(
    user=user,
    date=datetime.date.today(),
    stress_score=score,
    stress_level=level,
    inputs=inputs
  )
