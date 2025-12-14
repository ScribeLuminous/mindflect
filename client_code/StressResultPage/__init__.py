# -- StressResultPage.py (FINAL, WORKING CODE) --

from ._anvil_designer import StressResultPageTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import math

class StressResultPage(StressResultPageTemplate):
  def __init__(self, result, score, **properties):
    self.init_components(**properties)

    # Ensure score is an integer (1 to 100) for clean display
    score_int = round(max(1, min(100, score))) 

    # Use 'score_int' for percent label
    self.percent_lbl.text = f"{score_int}%"

    # Use the level (e.g., "Low Stress") for the title
    self.title_lbl.text = result['level']

    # Use the result's color for styling if you've set it up
    # NOTE: This line requires 'color' key in 'result' dict, if error occurs, comment it out.
    # self.percent_lbl.foreground = result['color'] 

    # Use score_int for the gauge
    self.draw_gauge(score_int)

    # Set the Explanation Label
    self.explanation_lbl.text = self.get_explanation(result['level'])

    # Set the Recommendations Label
    self.recs_lbl.text = self.get_recommendations(result['level'])


  def draw_gauge(self, percent):
    c = self.gauge_canvas

    # NOTE: Clear is not a standard method, but we can reset the drawing context 
    # for a clean start if needed, though for a simple static gauge, redrawing is enough.
    # c.reset_context() 

    # --- DRAW BACKGROUND ARC ---
    c.begin_path()
    c.arc(150, 150, 120, 180 * math.pi / 180, 360 * math.pi / 180) # Angles in radians
    c.line_width = 25 # Set line width for a thick arc
    c.line_cap = "round"
    c.stroke_style = "#e6e6e6" # Set the color
    c.stroke()
    c.close_path()

    # --- DRAW FILLED ARC ---
    angle_start_rad = 180 * math.pi / 180
    angle_end_rad = (180 + (percent / 100) * 180) * math.pi / 180

    c.begin_path()
    c.arc(150, 150, 120, angle_start_rad, angle_end_rad) # Angles in radians
    c.line_width = 25
    c.line_cap = "round"
    c.stroke_style = "#41b8d5" # Set the color
    c.stroke()
    c.close_path()

  def plot_1_click(self, points, **event_args):
    """This method is called when a data point is clicked."""
    pass

  def get_explanation(self, level):
    # Using 'in level' allows matching "Low Stress" with "Low"
    if "Low" in level:
      return (
        "Your stress level appears to be low today. You have a good foundation "
        "of healthy habits, which is highly protective against future stress buildup."
      )
    elif "Moderate" in level:
      return (
        "Your stress level is moderate. You are handling current demands well, "
        "but you are under pressure. Pay attention to early warning signs."
      )
    else: # High Stress
      return (
        "Your stress level is high today. This level can impact your health, "
        "mood, and performance. Immediate action is recommended to reduce pressure."
      )

  def get_recommendations(self, level):
    if "Low" in level:
      return (
        "**Tips for Maintenance:**\n"
        "- **Sleep:** Continue to prioritize 7-9 hours of sleep nightly.\n"
        "- **Exercise:** Maintain your current routine or explore new enjoyable activities.\n"
        "- **Diet:** Focus on variety and hydration to sustain energy."
      )
    elif "Moderate" in level:
      return (
        "**Recommendations for Balance:**\n"
        "- **Breaks:** Incorporate short, scheduled 5-minute mental breaks every hour.\n"
        "- **Mindfulness:** Dedicate 10 minutes daily to deep breathing or meditation.\n"
        "- **Screen Time:** Use screen-limiting apps after work hours to wind down."
      )
    else: # High Stress
      return (
        "**Urgent Action Plan:**\n"
        "- **Prioritize Rest:** Reduce non-essential tasks to free up mental energy.\n"
        "- **Hydrate & Nourish:** Focus on simple, nutrient-dense meals; avoid excess caffeine.\n"
        "- **Reach Out:** Talk to a trusted friend or professional about your feelings."
      )

  def home_btn_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass

  def save_btn_click(self, **event_args):
    import anvil.users
    import anvil.server
    from .. import assessment_logic
  
    # 1️⃣ Calculate stress result
    try:
      score = assessment_logic.calculate_total_stress()
      result = assessment_logic.get_result_feedback(score)
    except Exception as e:
      Notification("Please complete all questions before saving.", style="warning").show()
      return
  
    # 2️⃣ If NOT logged in → prompt user
    if not anvil.users.get_user():
      choice = alert(
        "You need an account to save your stress history.",
        buttons=[
          ("Login", "login"),
          ("Sign up", "signup"),
          ("Cancel", None)
        ],
        dismissible=True
      )
  
      if choice == "login":
        open_form("Login")
      elif choice == "signup":
        open_form("Signup")
  
      # 🚨 STOP execution if not logged in
      return
  
    # 3️⃣ Save result (user IS logged in)
    try:
      response = anvil.server.call(
        "save_daily_stress",
        score,
        result["level"],
        dict(assessment_logic.user_data)  # defensive copy
      )
  
      if response and response.get("ok") is True:
        Notification("Stress saved for today 💙").show()
      else:
        Notification(
          "Could not save your stress result. Please try again.",
          style="warning"
        ).show()
  
    except Exception as e:
      print("Save error:", e)
      Notification(
        "An unexpected error occurred while saving.",
        style="danger"
      ).show()
