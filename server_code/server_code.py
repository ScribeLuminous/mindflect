import anvil.server
import pandas as pd
import joblib

stress_model = joblib.load("stress_level_classification_model.pkl")

@anvil.server.callable
def predict_stress(features):
  X = pd.DataFrame([features])

  probs = stress_model.predict_proba(X)[0]
  classes = stress_model.classes_

  prob_map = dict(zip(classes, probs))
  level = max(prob_map, key=prob_map.get)
  percent = round(prob_map[level] * 100)

  return {
    "level": level,
    "percent": percent,
    "probabilities": prob_map
  }