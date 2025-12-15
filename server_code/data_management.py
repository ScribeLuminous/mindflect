# --- data_management.py (COMPLETE: ML + DATABASE) ---

import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users 
import anvil.tz
import datetime
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

# Load your models
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
  # Set up data based on role
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
    return {"level":