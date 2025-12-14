# --- assessment_logic.py ---

import anvil.server

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
  "burnout_role": None,

  # STUDENT
  "study_hours_per_day": None,
  "mental_health_rating": None,
  "social_media_hours": None,
  "attendance_percentage": None,
  "exam_score": None,
  "extracurricular_participation": None,

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
  "time_for_passion": None
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
  for key in [
    "sleep_hours",
    "daily_exercise_mins",
    "screen_time_hours",
    "diet_quality_1_10",
    "productivity_score_1_10",
    "mood_level_1_10"
  ]:
    if user_data[key] is None:
      raise ValueError("All stress questions must be answered.")

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

  return round(min(100, total), 1)

def get_stress_feedback(score):
  if score < 33:
    return "Low Stress"
  elif score < 66:
    return "Moderate Stress"
  else:
    return "High Stress"

# =============================
# BURNOUT CALCULATIONS
# =============================

def map_burnout_level(score):
  if score < 33:
    return "Low"
  elif score < 66:
    return "Moderate"
  else:
    return "High"

# ---------- PERSONAL ----------
def calculate_personal_burnout():
  d = burnout_data

  proxy = (
    0.35 * (d["daily_stress"] / 10) +
    0.20 * (1 - d["sleep_hours"] / 12) +
    0.15 * (d["daily_shouting"] / 10) +
    0.10 * (1 - d["time_for_passion"] / 10) +
    0.10 * (1 - d["diet_quality"] / 10) +
    0.10 * (1 - d["daily_steps"] / 20000)
  )

  score = round(min(100, proxy * 100), 1)
  return score, map_burnout_level(score)

# ---------- STUDY ----------
def calculate_study_burnout():
  d = burnout_data

  proxy = (
    0.35 * (d["study_hours_per_day"] / 12) +
    0.25 * (1 - d["mental_health_rating"] / 10) +
    0.15 * (d["social_media_hours"] / 12) +
    0.15 * (1 - d["attendance_percentage"] / 100) +
    0.10 * (1 - d["exam_score"] / 100)
  )

  score = round(min(100, proxy * 100), 1)
  return score, map_burnout_level(score)

# ---------- WORK ----------
def calculate_work_burnout():
  d = burnout_data

  proxy = (
    0.40 * (1 - d["work_life_balance"] / 10) +
    0.30 * (d["work_stress"] / 10) +
    0.15 * (d["lost_vacation"] / 60) +
    0.15 * (1 - d["sufficient_income"] / 10)
  )

  score = round(min(100, proxy * 100), 1)
  return score, map_burnout_level(score)

# ---------- COMBINED ----------
def calculate_combined_burnout(personal, study=None, work=None):
  scores = [personal]
  if study is not None:
    scores.append(study)
  if work is not None:
    scores.append(work)

  final = round(sum(scores) / len(scores), 1)
  return final, map_burnout_level(final)
