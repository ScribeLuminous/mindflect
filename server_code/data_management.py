# --- data_management.py (COMPLETE: ML + DATABASE) ---

import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users 
import anvil.tz
import datetime  # Standard Python datetime
import joblib
import pandas as pd
import anvil.files
from anvil.files import data_files

# =========================================================
# 1. LOAD ML MODELS
# =========================================================

models = {}

def load_model(key, filename):
  try:
    models[key] = joblib.load(data_files[f'mindflect_models/{filename}'])
    print(f"SUCCESS: Loaded {filename}")
  except (KeyError, FileNotFoundError):
    print(f"WARNING: Could not find 'mindflect_models/{filename}' in Data Files.")
    models[key] = None

load_model('stress', 'stress_level_classification_model.pkl')
load_model('personal', 'burnout_personal_model.pkl')
load_model('work', 'burnout_work_model.pkl')
load_model('study', 'burnout_study_model.pkl')


# =========================================================
# 2. PREDICTION FUNCTIONS
# =========================================================

@anvil.server.callable
def predict_stress(features):
  model = models.get('stress')
  if not model: 
    return {"level": "Error", "percent": 0}

  X = pd.DataFrame([features])
  try:
    probs = model.predict_proba(X)[0]
    classes = model.classes_
    prob_map = dict(zip(classes, probs))
    level = max(prob_map, key=prob_map.get)
    percent = round(prob_map[level] * 100)
    return {"level": str(level), "percent": percent}
  except Exception as e:
    print(f"Stress Error: {e}")
    return {"level": "Error", "percent": 0}

@anvil.server.callable
def predict_burnout(role, inputs):
  if role == 'student':
    model = models.get('study')
    data = {
      "study_hours_per_day": inputs.get("study_hours_per_day", 4),
      "sleep_hours": inputs.get("sleep_hours", 7),
      "mental_health_rating": inputs.get("mental_health_rating", 5),
      "social_media_hours": inputs.get("social_media_hours", 2),
      "attendance_percentage": inputs.get("attendance_percentage", 90),
      "exam_score": inputs.get("exam_score", 75),
      "exercise_frequency": inputs.get("daily_exercise_mins", 0),
      "age": 21, "gender": "Female", "part_time_job": "No",
      "extracurricular_participation": inputs.get("extracurricular_participation", "No")
    }
  elif role == 'worker':
    model = models.get('work')
    data = {
      "DAILY_STRESS": inputs.get("daily_stress", 5),
      "WORK_LIFE_BALANCE_SCORE": inputs.get("work_life_balance", 5),
      "LOST_VACATION": inputs.get("lost_vacation", 0),
      "SUFFICIENT_INCOME": inputs.get("sufficient_income", 1),
      "GENDER": "Female", "BMI_RANGE": "Normal"
    }
  else:
    model = models.get('personal')
    data = {
      "DAILY_STRESS": inputs.get("daily_stress", 5),
      "SLEEP_HOURS": inputs.get("sleep_hours", 7),
      "DAILY_SHOUTING": inputs.get("daily_shouting", 0),
      "TIME_FOR_PASSION": inputs.get("time_for_passion", 2),
      "DAILY_STEPS": inputs.get("daily_steps", 5000),
      "FRUITS_VEGGIES": inputs.get("diet_quality", 3),
      "WEEKLY_MEDITATION": 2, "GENDER": "Female", "BMI_RANGE": "Normal"
    }

  if not model: 
    return {"level": "Model Missing"}

  try:
    X = pd.DataFrame([data])
    prediction = model.predict(X)[0]
    return {"level": str(prediction)}
  except Exception as e:
    print(f"Burnout Prediction Error ({role}): {e}")
    return {"level": "Error"}


# =========================================================
# 3. DATABASE SAVING (FIXED DATE ERROR)
# =========================================================

@anvil.server.callable
def save_daily_stress(final_score, result_level, user_inputs):
  current_user = anvil.users.get_user()
  if not current_user: 
    return {"ok": False, "msg": "User not logged in."}

  # --- FIX: Use datetime.datetime.now(anvil.tz.tzlocal()) ---
  now = datetime.datetime.now(anvil.tz.tzlocal())
  today = now.date()

  start_of_day = datetime.datetime.combine(today, datetime.time.min).replace(tzinfo=anvil.tz.tzlocal())
  end_of_day = datetime.datetime.combine(today, datetime.time.max).replace(tzinfo=anvil.tz.tzlocal())

  existing_log = app_tables.stress_logs.search(
    users=current_user,
    date=q.all_of(
      q.greater_than_or_equal_to(start_of_day),
      q.less_than_or_equal_to(end_of_day)
    )
  )

  if len(existing_log) > 0:
    return {"ok": False, "msg": "Assessment already saved for today."}

  app_tables.stress_logs.add_row(
    users=current_user,
    date=now,  # <--- FIXED
    total_score=final_score,
    level=result_level,
    sleep_hours=user_inputs.get("sleep_hours"),
    daily_exercise_mins=user_inputs.get("daily_exercise_mins"),
    screen_time_hours=user_inputs.get("screen_time_hours"),      
    diet_quality=user_inputs.get("diet_quality_1_10"),
    productivity_score=user_inputs.get("productivity_score_1_10"), 
    mood_level=user_inputs.get("mood_level_1_10"),
  )
  return {"ok": True}

@anvil.server.callable
def log_burnout_assessment(burnout_score, guidance, user_inputs):
  current_user = anvil.users.get_user()
  if not current_user: 
    return {"ok": False, "msg": "Not logged in"}

  # --- FIX: Use correct time function here too ---
  now = datetime.datetime.now(anvil.tz.tzlocal())

  app_tables.burnout_logs.add_row(
    users=current_user,
    date=now, # <--- FIXED
    burnout_score=burnout_score, 
    guidance=guidance, 
  )
  return {"ok": True}


# =========================================================
# 4. HISTORY & PROFILE
# =========================================================

@anvil.server.callable
def get_user_history():
  user = anvil.users.get_user()
  if not user: 
    return [], []

  stress_rows = app_tables.stress_logs.search(tables.order_by("date"), users=user)
  stress_history = [{"date": r['date'], "score": r['total_score']} for r in stress_rows]

  burnout_rows = app_tables.burnout_logs.search(tables.order_by("date"), users=user)
  burnout_history = [{"date": r['date'], "score": r['burnout_score']} for r in burnout_rows]

  return stress_history, burnout_history

@anvil.server.callable
def get_user_profile_data():
  """
  Fetches user's name, latest levels, AND SCRES.
  """
  user = anvil.users.get_user()
  if not user: 
    return None

  username = user['username'] or user['email'].split('@')[0]

  # --- 1. Get Latest Stress ---
  latest_stress = "Unknown"
  latest_stress_score = 0  # Default to 0

  stress_log = app_tables.stress_logs.search(
    tables.order_by("date", ascending=False),
    users=user
  )

  if len(stress_log) > 0:
    # Get Score
    latest_stress_score = stress_log[0]['total_score'] or 0

    # Get Level (or calculate if missing)
    saved_level = stress_log[0]['level']
    if saved_level:
      latest_stress = saved_level
    else:
      if latest_stress_score < 40: 
        latest_stress = "Low Stress"
      elif latest_stress_score < 80: 
        latest_stress = "Moderate Stress"
      else: 
        latest_stress = "High Stress"

  # --- 2. Get Latest Burnout ---
  latest_burnout = "Unknown"
  latest_burnout_score = 0 # Default to 0

  burnout_log = app_tables.burnout_logs.search(
    tables.order_by("date", ascending=False),
    users=user
  )

  if len(burnout_log) > 0:
    # Get Score
    latest_burnout_score = burnout_log[0]['burnout_score'] or 0

    # Calculate Level
    if latest_burnout_score <= 33: 
      latest_burnout = "Low Burnout"
    elif latest_burnout_score <= 66: 
      latest_burnout = "Moderate Burnout"
    else: 
      latest_burnout = "High Burnout"

  return {
    "username": username,
    "latest_stress_level": latest_stress,
    "latest_stress_score": latest_stress_score,   # <--- Sending this now
    "latest_burnout_level": latest_burnout,
    "latest_burnout_score": latest_burnout_score  # <--- Sending this now
  }