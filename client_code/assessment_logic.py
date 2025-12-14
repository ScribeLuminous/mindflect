# --- assessment_logic.py (FINAL FIXED VERSION) ---

import anvil.server
import anvil.users

# =============================
# GLOBAL STORAGE
# =============================

user_data = {
  # STRESS
  "sleep_hours": None,
  "daily_exercise_mins": None,
  "screen_time_hours": None,
  "diet_quality_1_10": None,
  "productivity_score_1_10": None,
  "mood_level_1_10": None,

  # ROLE
  "current_situation": None
}

burnout_data = {
  # ROLE
  "burnout_role": None, # e.g., 'student', 'worker', 'both'

  # STUDENT
  "study_hours_per_day": None,
  "mental_health_rating": None,
  "social_media_hours": None,
  "attendance_percentage": None,
  "exam_score": None,
  "extracurricular_participation": None, # 'yes' or 'no'

  # WORK
  "work_life_balance": None,
  "work_stress": None,
  "lost_vacation": None,
  "sufficient_income": None,

  # PERSONAL
  "daily_stress": None,
  "sleep_hours": None,
  "daily_shouting": None,
  "daily_steps": None,
  "diet_quality": None,
  "time_for_passion": None,

  # FINAL RESULTS (Store results here after calculation)
  "final_burnout_score": None,
  "final_stress_score": None
}

# =============================
# THRESHOLDS
# =============================

STRESS_THRESHOLDS = {
  "Low Stress": {"min": 0, "max": 33, "color": "#4CAF50"},      
  "Moderate Stress": {"min": 34, "max": 66, "color": "#FFC107"}, 
  "High Stress": {"min": 67, "max": 100, "color": "#F44336"}    
}

BURNOUT_THRESHOLDS = {
  "Low Burnout": {"min": 0, "max": 33, "color": "#4CAF50"},      
  "Moderate Burnout": {"min": 34, "max": 66, "color": "#FFC107"}, 
  "High Burnout": {"min": 67, "max": 100, "color": "#F44336"}    
}


# =============================
# VALIDATION
# =============================
def validate_input(value_str, min_val, max_val, require_integer=False):
  if value_str is None or str(value_str).strip() == "":
    return False, "Please enter a number."

  try:
    val = float(value_str)
  except ValueError:
    return False, "Please enter a valid number."

  if require_integer and not val.is_integer():
    return False, "Only whole numbers are allowed."

  val = int(val) if require_integer else val

  if not (min_val <= val <= max_val):
    return False, f"Value must be between {min_val} and {max_val}."

  return True, val

# =============================
# STRESS CALCULATION
# =============================

def calculate_total_stress():

  score_sleep = max(0, min(100, (8 - (user_data["sleep_hours"] or 8)) * 25))
  score_exercise = max(0, min(100, (60 - (user_data["daily_exercise_mins"] or 60)) * 1.6))
  score_screen = max(0, min(100, ((user_data["screen_time_hours"] or 0) / 16) * 100))
  score_diet = (10 - (user_data["diet_quality_1_10"] or 10)) * 11
  score_prod = (10 - (user_data["productivity_score_1_10"] or 10)) * 11
  score_mood = (10 - (user_data["mood_level_1_10"] or 10)) * 11

  total = (
    score_sleep +
    score_exercise +
    score_screen +
    score_diet +
    score_prod +
    score_mood
  ) / 6

  return round(min(100, total), 1)

def get_stress_level(score):
  """Retrieves the level and color from the thresholds."""
  for level, threshold in STRESS_THRESHOLDS.items():
    if threshold["min"] <= score <= threshold["max"]:
      return {"level": level, "color": threshold["color"]}
  return {"level": "Undefined Stress", "color": "#808080"} 


def get_result_feedback(): 
  """Calculates the final stress score, level, and returns the result dict for the form."""
  final_score = calculate_total_stress()
  stress_level_result = get_stress_level(final_score)

  # FIX: Access burnout_data directly (removed 'assessment_logic.' prefix)
  burnout_data["final_stress_score"] = final_score

  return stress_level_result, final_score 


# =============================
# BURNOUT CALCULATIONS
# =============================

def get_burnout_level(score):
  """Retrieves the level and color from the thresholds."""
  for level, threshold in BURNOUT_THRESHOLDS.items():
    if threshold["min"] <= score <= threshold["max"]:
      return {"level": level, "color": threshold["color"]}
  return {"level": "Undefined Burnout", "color": "#808080"} 


# ---------- PERSONAL ----------
def calculate_personal_burnout():
  d = burnout_data

  # Check for presence of essential keys before calculation
  if not all(k in d and d[k] is not None for k in ["daily_stress", "sleep_hours", "daily_shouting", "time_for_passion", "diet_quality", "daily_steps"]):
    return 0

  proxy = (
    0.35 * (d["daily_stress"] / 10) +
    0.20 * (1 - d["sleep_hours"] / 12) +
    0.15 * (d["daily_shouting"] / 10) +
    0.10 * (1 - d["time_for_passion"] / 10) +
    0.10 * (1 - d["diet_quality"] / 10) +
    0.10 * (1 - d["daily_steps"] / 20000)
  )

  score = round(min(100, proxy * 100), 1)
  return score

# ---------- STUDY ----------
def calculate_study_burnout():
  d = burnout_data

  if not all(k in d and d[k] is not None for k in ["study_hours_per_day", "mental_health_rating", "social_media_hours", "attendance_percentage", "exam_score"]):
    return 0

  proxy = (
    0.35 * (d["study_hours_per_day"] / 12) +
    0.25 * (1 - d["mental_health_rating"] / 10) +
    0.15 * (d["social_media_hours"] / 12) +
    0.15 * (1 - d["attendance_percentage"] / 100) +
    0.10 * (1 - d["exam_score"] / 100)
  )

  score = round(min(100, proxy * 100), 1)
  return score

# ---------- WORK ----------
def calculate_work_burnout():
  d = burnout_data

  if not all(k in d and d[k] is not None for k in ["work_life_balance", "work_stress", "lost_vacation", "sufficient_income"]):
    return 0

  proxy = (
    0.40 * (1 - d["work_life_balance"] / 10) +
    0.30 * (d["work_stress"] / 10) +
    0.15 * (d["lost_vacation"] / 60) +
    0.15 * (1 - d["sufficient_income"] / 10)
  )

  score = round(min(100, proxy * 100), 1)
  return score

# ---------- COMBINED & FINAL BURNOUT SUBMISSION ----------

def submit_assessment():
  """Calculates burnout using the ML models on the server."""

  role = burnout_data.get("burnout_role")

  # 1. Call the appropriate ML model based on role
  # Note: We pass the whole 'burnout_data' dict, and the server picks what it needs
  if role == "student":
    result = anvil.server.call('predict_burnout_study', burnout_data)
    final_level = result['level']
    # Map text level to a score for the gauge (Approximate)
    final_score = 30 if "Low" in final_level else (60 if "Moderate" in final_level else 85)

  elif role == "worker":
    result = anvil.server.call('predict_burnout_work', burnout_data)
    final_level = result['level']
    final_score = 30 if "Low" in final_level else (60 if "Moderate" in final_level else 85)

  else: 
    # Fallback to Personal or Average if 'Both' (or define logic for 'Both')
    result = anvil.server.call('predict_burnout_personal', burnout_data)
    final_level = result['level']
    final_score = 30 if "Low" in final_level else (60 if "Moderate" in final_level else 85)

    # Format for the UI
  burnout_level_result = {
    "level": final_level,
    "color": "#4CAF50" if "Low" in final_level else ("#FFC107" if "Moderate" in final_level else "#F44336")
  }

  burnout_data["final_burnout_score"] = final_score

  return burnout_level_result, final_score