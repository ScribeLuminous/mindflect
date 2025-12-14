import anvil.server
import joblib
import pandas as pd
import anvil.files
from anvil.files import data_files

# --- 1. LOAD MODELS ---
# We load them globally so they stay in memory (much faster)

models = {}

def load_model(key, filename):
  try:
    models[key] = joblib.load(data_files[filename])
    print(f"Loaded {filename}")
  except (KeyError, FileNotFoundError):
    print(f"Warning: {filename} not found in Data Files")
    models[key] = None

# Load all 4 models
load_model('stress', 'mindflect_models/stress_level_classification_model.pkl')
load_model('personal', 'mindflect_models/burnout_personal_model.pkl')
load_model('work', 'mindflect_models/burnout_work_model.pkl')
load_model('study', 'mindflect_models/burnout_study_model.pkl')


# --- 2. PREDICTION FUNCTIONS WITH DEFAULTS ---

@anvil.server.callable
def predict_stress(features):
  """
    Predicts stress level [0, 1, 2] -> ['Low', 'Moderate', 'High']
    """
  model = models.get('stress')
  if not model:
    return {"level": "Error (Model Missing)", "percent": 0}

    # Ensure features are in a DataFrame with correct column order
    # The stress model expects these exact keys based on your training data
  X = pd.DataFrame([features])

  try:
    probs = model.predict_proba(X)[0]
    classes = model.classes_

    prob_map = dict(zip(classes, probs))
    level = max(prob_map, key=prob_map.get)

    # Convert probability to a 0-100 score for the gauge
    # (If High stress is 90% likely, score is 90)
    percent = round(prob_map[level] * 100)

    return {
      "level": str(level), # e.g., "High"
      "percent": percent,
      "probabilities": prob_map
    }
  except Exception as e:
    print(f"Stress Prediction Error: {e}")
    return {"level": "Error", "percent": 0}

@anvil.server.callable
def predict_burnout_personal(inputs):
  """
    Predicts personal burnout using defaults for missing demographics.
    """
  model = models.get('personal')
  if not model: return {"level": "Model Missing"}

    # Map your form inputs -> Model Column Names (UPPERCASE for Personal)
  data = {
    "DAILY_STRESS": inputs.get("daily_stress", 5),
    "SLEEP_HOURS": inputs.get("sleep_hours", 7),
    "DAILY_SHOUTING": inputs.get("daily_shouting", 0),
    "TIME_FOR_PASSION": inputs.get("time_for_passion", 2),
    "DAILY_STEPS": inputs.get("daily_steps", 5000),

    # Mappings (Best Effort)
    "FRUITS_VEGGIES": inputs.get("diet_quality", 3), # Map 1-10 diet to servings

    # DEFAULTS for missing fields
    "WEEKLY_MEDITATION": 2,       # Assume average
    "GENDER": "Female",           # Default required for OneHotEncoder
    "BMI_RANGE": "Normal"         # Default required for OneHotEncoder
  }

  X = pd.DataFrame([data])

  try:
    prediction = model.predict(X)[0]
    return {"level": str(prediction)}
  except Exception as e:
    print(f"Personal Burnout Error: {e}")
    return {"level": "Calculation Error"}

@anvil.server.callable
def predict_burnout_work(inputs):
  """
    Predicts work burnout using defaults.
    """
  model = models.get('work')
  if not model: return {"level": "Model Missing"}

    # Map Form -> Model Columns (UPPERCASE)
  data = {
    "DAILY_STRESS": inputs.get("daily_stress", 5), # Shared metric
    "WORK_LIFE_BALANCE_SCORE": inputs.get("work_life_balance", 5),
    "LOST_VACATION": inputs.get("lost_vacation", 0),
    "SUFFICIENT_INCOME": inputs.get("sufficient_income", 1), # 1=No, 2=Yes (Adjust based on model training)

    # DEFAULTS
    "GENDER": "Female",
    "BMI_RANGE": "Normal"
  }

  X = pd.DataFrame([data])

  try:
    prediction = model.predict(X)[0]
    return {"level": str(prediction)}
  except Exception as e:
    print(f"Work Burnout Error: {e}")
    return {"level": "Calculation Error"}

@anvil.server.callable
def predict_burnout_study(inputs):
  """
    Predicts study burnout using defaults.
    """
  model = models.get('study')
  if not model: return {"level": "Model Missing"}

    # Map Form -> Model Columns (LOWERCASE based on snippet)
  data = {
    "study_hours_per_day": inputs.get("study_hours_per_day", 4),
    "sleep_hours": inputs.get("sleep_hours", 7),
    "mental_health_rating": inputs.get("mental_health_rating", 5),
    "social_media_hours": inputs.get("social_media_hours", 2),
    "attendance_percentage": inputs.get("attendance_percentage", 90),
    "exam_score": inputs.get("exam_score", 75),

    # Mappings
    "exercise_frequency": inputs.get("daily_exercise_mins", 0), # Using mins as proxy for freq if needed

    # DEFAULTS
    "age": 21,                      # Avg student age
    "gender": "Female",             # Default for encoding
    "part_time_job": "No",          # Default
    "extracurricular_participation": inputs.get("extracurricular_participation", "No") # 'Yes'/'No'
  }

  X = pd.DataFrame([data])

  try:
    prediction = model.predict(X)[0]
    return {"level": str(prediction)}
  except Exception as e:
    print(f"Study Burnout Error: {e}")
    return {"level": "Calculation Error"}