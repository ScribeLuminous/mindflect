# --- assessment_logic.py (COMPLETE AND CORRECTED) ---

import anvil.server
import anvil.data_management
import anvil.stress_server
import anvil.burnout_server

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
# THRESHOLDS (New Helper Structures)
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
# STRESS CALCULATION (Updated to match thresholds and include final function)
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
      # We must use 'burnout_data' here if that's what's passed, 
      # but assuming 'user_data' is for the dedicated Stress track
      continue # Allow calculation even if some keys are None if you haven't answered all
      # raise ValueError("All stress questions must be answered.") 

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
  
    # Store results (optional)
    burnout_data["final_stress_score"] = final_score
  
    # Return the score and the dict the results form expects
    return stress_level_result, final_score # Returns result_dict, score_int
  
  
  # =============================
  # BURNOUT CALCULATIONS (Updated for centralized helper functions)
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
  
    # Check for presence of essential keys before calculation to avoid errors
    if not all(k in d and d[k] is not None for k in ["daily_stress", "sleep_hours", "daily_shouting", "time_for_passion", "diet_quality", "daily_steps"]):
      return 0, "Incomplete"
  
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
      return 0, "Incomplete"
  
      # NOTE: extracurricular_participation needs mapping if included in formula
  
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
      return 0, "Incomplete"
  
    proxy = (
      0.40 * (1 - d["work_life_balance"] / 10) +
      0.30 * (d["work_stress"] / 10) +
      0.15 * (d["lost_vacation"] / 60) +
      0.15 * (1 - d["sufficient_income"] / 10)
    )
  
    score = round(min(100, proxy * 100), 1)
    return score
  
  # ---------- COMBINED & FINAL BURNOUT SUBMISSION (New Function) ----------
  
  def submit_assessment():
    """
      Calculates the combined burnout score based on the user's role ('burnout_role').
      This function is called by the final form in the Burnout track.
      """
    personal_score = calculate_personal_burnout() # Always calculated if reached
    study_score = calculate_study_burnout()
    work_score = calculate_work_burnout()
  
    scores = [personal_score]
    role = burnout_data.get("burnout_role")
  
    if role == "student" or role == "both":
      if study_score != 0:
        scores.append(study_score)
  
    if role == "worker" or role == "both":
      if work_score != 0:
        scores.append(work_score)
  
      # Calculate the average of relevant scores
    final_score = round(sum(scores) / len(scores), 1)
  
    # Get final result dict
    burnout_level_result = get_burnout_level(final_score)
  
    burnout_data["final_burnout_score"] = final_score
  
    # Return the result for immediate use by the final form
    return burnout_level_result, final_score # Returns result_dict, score_int