# -- StressResultPage.py (FINAL, FIXED IMPORT) --

from ._anvil_designer import StressResultPageTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.users 

import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import math

from .. import assessment_logic 

class StressResultPage(StressResultPageTemplate):
  def __init__(self, result, score, **properties):
    self.init_components(**properties)

    # Ensure score is an integer (1 to 100) for clean display
    score_int = round(max(1, min(100, score))) 

    # Use 'score_int' for percent label
    self.percent_lbl.text = f"{score_int}%"

    # Use the level (e.g., "Low Stress") for the title
    self.title_lbl.text = result['level']

    # Use the result's color for styling if provided
    if 'color' in result:
      self.percent_lbl.foreground = result['color'] 

      # Use score_int for the gauge
    self.draw_gauge(score_int)

    # Set the Explanation Label
    self.explanation_lbl.text = self.get_explanation(result['level'])

    # Set the Recommendations Label
    self.recs_lbl.text = self.get_recommendations(result['level'])


  def draw_gauge(self, percent):
    c = self.gauge_canvas

    # --- DRAW BACKGROUND ARC ---
    c.begin_path()
    c.arc(150, 150, 120, 180 * math.pi / 180, 360 * math.pi / 180) 
    c.line_width = 25 
    c.line_cap = "round"
    c.stroke_style = "#e6e6e6" 
    c.stroke()
    c.close_path()

    # --- DRAW FILLED ARC ---
    angle_start_rad = 180 * math.pi / 180
    angle_end_rad = (180 + (percent / 100) * 180) * math.pi / 180

    c.begin_path()
    c.arc(150, 150, 120, angle_start_rad, angle_end_rad) 
    c.line_width = 25
    c.line_cap = "round"
    c.stroke_style = "#41b8d5" 
    c.stroke()
    c.close_path()

  def plot_1_click(self, points, **event_args):
    pass

  def get_explanation(self, level):
    if "Low" in level:
      return "Your stress level appears to be low today. Keep maintaining healthy routines."
    elif "Moderate" in level:
      return "Your stress level is moderate. You are handling current demands well but under pressure."
    else:
      return "Your stress level is high today. Immediate action is recommended to reduce pressure."

  def get_recommendations(self, level):
    if "Low" in level:
      return "**Tips:** Prioritize sleep and exercise."
    elif "Moderate" in level:
      return "**Tips:** Take short breaks and practice mindfulness."
    else:
      return "**Action Plan:** Prioritize rest and reduce non-essential tasks."

  def home_btn_click(self, **event_args):
    open_form('MainPage')

  def save_btn_click(self, **event_args):
    # FIX: REMOVED 'import anvil.data_management' - THIS WAS THE CAUSE OF THE ERROR

    # 1. Calculate stress result logic
    try:
      # Note: assessment_logic.get_result_feedback() returns (result_dict, score)
      # You are re-calculating here to ensure you have the latest data for saving
      result_dict, score_val = assessment_logic.get_result_feedback()
    except Exception as e:
      Notification("Error calculating results. Please ensure all questions are answered.", style="warning").show()
      return

      # 2. Check Login
    if not anvil.users.get_user():
      choice = alert(
        "You need an account to save your stress history.",
        buttons=[("Login", "login"), ("Sign up", "signup"), ("Cancel", None)],
        dismissible=True
      )

      if choice == "login":
        open_form("Account.Login") # Adjust if your login form name is different
      elif choice == "signup":
        open_form("Account.Signup") # Adjust if your signup form name is different
      return

      # 3. Save result via Server Call
    try:
      # We call the server function by string name.
      # The server module 'data_management' is loaded automatically on the server.
      response = anvil.server.call(
        "save_daily_stress",
        score_val,
        result_dict["level"],
        dict(assessment_logic.user_data) 
      )

      if response and response.get("ok") is True:
        Notification("Stress saved for today 💙").show()
      else:
        msg = response.get("msg", "Could not save.") if response else "Unknown error."
        Notification(f"Save failed: {msg}", style="warning").show()

    except Exception as e:
      print(f"Save error: {e}")
      Notification("An unexpected error occurred while saving.", style="danger").show()