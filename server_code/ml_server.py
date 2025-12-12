import anvil.files
from anvil.files import data_files
# ml_server (Server Module)
import anvil.server
import io
import joblib
import pandas as pd
import numpy as np
from anvil.files import data_files

# Cached models
_stress_model = None
_personal_model = None
_work_model = None
_study_model = None

def _load_models():
  global _stress_model, _personal_model, _work_model, _study_model
  if _stress_model is None:
    b = data_files['stress_model.pkl'].get_bytes()
    _stress_model = joblib.load(io.BytesIO(b))
  if _personal_model is None:
    b = data_files['burnout_personal_model.pkl'].get_bytes()
    _personal_model = joblib.load(io.BytesIO(b))
  if _work_model is None:
    b = data_files['burnout_work_model.pkl'].get_bytes()
    _work_model = joblib.load(io.BytesIO(b))
  if _study_model is None:
    b = data_files['burnout_study_model.pkl'].get_bytes()
    _study_model = joblib.load(io.BytesIO(b))

# ---------- burnout level mapping (0-100 => label)
def burnout_level_from_score(score: float) -> str:
  if score is None or (isinstance(score, float) and np.isnan(score)):
    return "Unknown"
  s = float(score)
  s = max(0.0, min(100.0, s))
  # CBI-like thresholds
  if s < 25:
    return "No/Low"
  elif s < 50:
    return "Low"
  elif s < 75:
    return "Moderate"
  else:
    return "High"

def combine_burnout_scores(personal=None, work=None, study=None, weights=None):
  default_weights = {'personal': 0.40, 'work': 0.35, 'study': 0.25}
  if weights is None:
    weights = default_weights.copy()
  else:
    for k,v in default_weights.items():
      weights.setdefault(k, v)
  values = {}
  if personal is not None: values['personal'] = float(personal)
  if work is not None: values['work'] = float(work)
  if study is not None: values['study'] = float(study)
  if len(values)==0:
    return None, {}
  avail_weights = {k: weights.get(k, 0.0) for k in values.keys()}
  total = sum(avail_weights.values())
  if total <= 0:
    n = len(values)
    avail_weights = {k: 1.0/n for k in values.keys()}
    total = 1.0
  norm = {k: v/total for k,v in avail_weights.items()}
  overall = sum(norm[k]*values[k] for k in values.keys())
  overall = float(max(0.0, min(100.0, overall)))
  breakdown = {'per_domain': values, 'norm_weights': norm, 'overall_score': overall}
  return overall, breakdown

# ---------- helpers to make DataFrame rows with expected columns
def _df_row_from_dict(dct, cols):
  row = {c: dct.get(c, None) for c in cols}
  return pd.DataFrame([row], columns=cols)

@anvil.server.callable
def predict_stress(inputs: dict):
  """
  Expects inputs matching training features for the stress model.
  Example keys: 'sleep_hours','daily_exercise_mins','screen_time_hours','diet_quality_1_10','productivity_score_1_10','mood_level_1_10'
  """
  _load_models()
  # If stress_model is a regressor, you may want .predict_proba not available; adjust as needed.
  try:
    cols = list(inputs.keys())
    X = pd.DataFrame([inputs], columns=cols)
    pred = _stress_model.predict(X)[0]
    resp = {'prediction': pred}
    # if classifier with classes and proba:
    if hasattr(_stress_model, 'predict_proba'):
      proba = _stress_model.predict_proba(X)[0].tolist()
      resp['proba'] = dict(zip(map(str,_stress_model.classes_), map(float, proba)))
    return resp
  except Exception as e:
    return {'error': str(e)}

@anvil.server.callable
def predict_burnout(personal_inputs=None, work_inputs=None, study_inputs=None, return_scores=False):
  """
  personal_inputs/work_inputs/study_inputs are dicts matching pipeline columns.
  Returns labels and numeric domain scores (0-100) if available.
  """
  _load_models()
  results = {}
  # PERSONAL
  if personal_inputs is not None:
    cols_p = list(personal_inputs.keys())
    Xp = pd.DataFrame([personal_inputs], columns=cols_p)
    try:
      pred_p = _personal_model.predict(Xp)[0]   # label like "Low"/"Moderate"/"High" if classifier
      results['personal_label'] = str(pred_p)
    except Exception as e:
      results['personal_label'] = "Unknown"
    # If your personal_model produced numeric scores or you also saved proxy formula, optionally compute numeric:
    if hasattr(_personal_model, "predict_proba"):
      # fallback: use proba to compute pseudo-score (optional)
      proba = _personal_model.predict_proba(Xp)[0]
      # compute weighted numeric: assume classes ordered low->high
      try:
        classes = list(_personal_model.classes_)
        # assign 0,50,100 mapping as rough numeric
        mapping = {classes[i]: i*50.0 for i in range(len(classes))}
        numeric = sum(mapping[c]*p for c,p in zip(classes,proba))
        results['personal_score_est'] = float(numeric)
      except Exception:
        results['personal_score_est'] = None

  # WORK
  if work_inputs is not None:
    cols_w = list(work_inputs.keys())
    Xw = pd.DataFrame([work_inputs], columns=cols_w)
    try:
      pred_w = _work_model.predict(Xw)[0]
      results['work_label'] = str(pred_w)
    except Exception as e:
      results['work_label'] = "Unknown"
    if hasattr(_work_model, "predict_proba"):
      proba = _work_model.predict_proba(Xw)[0]
      try:
        classes = list(_work_model.classes_)
        mapping = {classes[i]: i*50.0 for i in range(len(classes))}
        numeric = sum(mapping[c]*p for c,p in zip(classes,proba))
        results['work_score_est'] = float(numeric)
      except Exception:
        results['work_score_est'] = None

  # STUDY
  if study_inputs is not None:
    cols_s = list(study_inputs.keys())
    Xs = pd.DataFrame([study_inputs], columns=cols_s)
    try:
      pred_s = _study_model.predict(Xs)[0]
      results['study_label'] = str(pred_s)
    except Exception as e:
      results['study_label'] = "Unknown"
    if hasattr(_study_model, "predict_proba"):
      proba = _study_model.predict_proba(Xs)[0]
      try:
        classes = list(_study_model.classes_)
        mapping = {classes[i]: i*50.0 for i in range(len(classes))}
        numeric = sum(mapping[c]*p for c,p in zip(classes,proba))
        results['study_score_est'] = float(numeric)
      except Exception:
        results['study_score_est'] = None

  # If the model pipelines include a final regressor that outputs numeric burnout score (0-100),
  # replace the above proba->score mapping with direct numeric outputs.

  # Combine numeric scores if available (prefer direct numeric from model; else use estimated)
  personal_score = results.get('personal_score_est', None)
  work_score = results.get('work_score_est', None)
  study_score = results.get('study_score_est', None)

  # Only combine using available numeric scores; if none present, attempt fallback: convert labels to numeric via mapping
  def label_to_numeric(lbl):
    if lbl in (None, "Unknown"): return None
    # map textual labels to rough numeric centers:
    m = {'No/Low': 12.5, 'Low': 37.5, 'Moderate': 62.5, 'High': 87.5,
         'Low': 37.5, 'Moderate':62.5, 'High':87.5}
    return m.get(lbl, None)

  if personal_score is None:
    personal_score = label_to_numeric(results.get('personal_label'))
  if work_score is None:
    work_score = label_to_numeric(results.get('work_label'))
  if study_score is None:
    study_score = label_to_numeric(results.get('study_label'))

  overall, breakdown = combine_burnout_scores(personal=personal_score, work=work_score, study=study_score)
  if overall is not None:
    results['overall_score'] = float(overall)
    results['overall_label'] = burnout_level_from_score(overall)
  else:
    results['overall_score'] = None
    results['overall_label'] = "Unknown"

  return results
