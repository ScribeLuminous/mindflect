import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

# --- GLOBAL STORAGE ---
# We store the raw answers here as the user moves through forms
user_data = {
  "sleep_hours": 7,          # Default healthy
  "daily_exercise_mins": 30, # Default healthy
  "screen_time_hours": 4,    # Default moderate
  "diet_quality_1_10": 5,
  "productivity_score_1_10": 5,
  "mood_level_1_10": 5
}

# --- CALCULATOR LOGIC ---
def calculate_total_stress():
  """
  Normalizes all inputs to a 0-100 Stress Scale and returns the average.
  0 = Zen/Relaxed
  100 = Maximum Stress
  """
  data = user_data # Alias for easier reading

  # 1. Sleep Logic (Inverse: Less sleep = More stress)
  # Benchmark: < 4 hours is max stress (100), 8+ hours is zero stress (0)
  # Formula: (8 - hours) * 25 (clamped)
  val_sleep = float(data['sleep_hours'])
  score_sleep = max(0, min(100, (8 - val_sleep) * 25))

  # 2. Exercise Logic (Inverse: Less exercise = More stress)
  # Benchmark: 0 mins is max stress (100), 60+ mins is zero stress (0)
  val_exercise = float(data['daily_exercise_mins'])
  score_exercise = max(0, min(100, (60 - val_exercise) * 1.6))

  # 3. Screen Time Logic (Direct: More screens = More stress)
  # Benchmark: 12+ hours is max stress (100), 0 hours is zero stress
  val_screen = float(data['screen_time_hours'])
  score_screen = max(0, min(100, (val_screen / 12) * 100))

  # 4. Subjective Scales (1-10) (Inverse: Low rating = High Stress)
  # 1 = 100 Stress, 10 = 0 Stress
  score_diet = (10 - data['diet_quality_1_10']) * 11
  score_prod = (10 - data['productivity_score_1_10']) * 11
  score_mood = (10 - data['mood_level_1_10']) * 11

  # --- FINAL CALCULATION ---
  # We average all 6 scores to get the Total Stress Level
  total_score = (score_sleep + score_exercise + score_screen + score_diet + score_prod + score_mood) / 6

  return round(total_score, 1)

def get_result_feedback(final_score):
  """Returns the text label and color based on the calculated score."""
  if final_score < 33:
    return {"level": "Low Stress", "color": "#4CAF50", "msg": "You are balanced."}
  elif final_score < 66:
    return {"level": "Moderate Stress", "color": "#FF9800", "msg": "You are under pressure."}
  else:
    return {"level": "High Stress", "color": "#F44336", "msg": "Critical levels detected."}