import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import math # Needed for checking NaN

# --- CONSTANTS & CONFIGURATION ---

# UI Colors (Material Design standard)
COLOR_LOW = "#4CAF50"      # Green
COLOR_MODERATE = "#FF9800" # Orange
COLOR_HIGH = "#F44336"     # Red
COLOR_UNKNOWN = "#9E9E9E"  # Grey

DISCLAIMER = """
⚠️ IMPORTANT: This result is an estimate based on self-reported answers. 
It is NOT a medical diagnosis. If you feel overwhelmed, please consult a professional.
"""

# Philippines Helplines Dictionary
PH_HELPLINES = [
  {"name": "NCMH Crisis Hotline", "contact": "0917-899-USAP (8727) / 1553"},
  {"name": "Hopeline PH", "contact": "0917-558-4673"},
  {"name": "In Touch Community", "contact": "0917-800-1123"}
]

# --- LOGIC FUNCTIONS ---

def get_stress_result(score):
  """
  Analyzes stress slider score (0-100).
  Returns a dict: {'level': str, 'color': str, 'tip': str}
  """
  if score is None:
    return {"level": "Unknown", "color": COLOR_UNKNOWN, "tip": "Please adjust the slider."}

  # Ensure score is float
  s = float(score)

  if s < 33:
    return {
      "level": "Low",
      "color": COLOR_LOW,
      "tip": "You are handling pressure well. Keep building resilience!"
    }
  elif s < 66:
    return {
      "level": "Moderate",
      "color": COLOR_MODERATE,
      "tip": "You are feeling pressure. Try 'micro-breaks' and prioritize tasks."
    }
  else:
    return {
      "level": "High",
      "color": COLOR_HIGH,
      "tip": "High arousal detected. Try Box Breathing and seek support."
    }

def get_burnout_result(score):
  """
  Analyzes burnout slider score (0-100).
  Handles NaN and Clamping as requested.
  """
  # 1. Handle Unknowns (None or NaN)
  if score is None or (isinstance(score, float) and math.isnan(score)):
    return {
      "level": "Unknown", 
      "color": COLOR_UNKNOWN, 
      "tip": "Move the slider to see your result."
    }

  # 2. Clamp values between 0.0 and 100.0
  s = float(score)
  s = max(0.0, min(100.0, s))

  # 3. Determine Level
  if s < 25:
    return {
      "level": "No/Low",
      "color": COLOR_LOW,
      "tip": "Engagement is good. Keep aligning work with your values."
    }
  elif s < 50:
    return {
      "level": "Low",
      "color": COLOR_LOW,
      "tip": "You are doing okay, but ensure you maintain boundaries."
    }
  elif s < 75:
    return {
      "level": "Moderate",
      "color": COLOR_MODERATE,
      "tip": "Cynicism may be setting in. Identify which work area is mismatched."
    }
  else:
    return {
      "level": "High",
      "color": COLOR_HIGH,
      "tip": "Severe exhaustion risk. Please consult a professional immediately."
    }