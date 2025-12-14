# -- BurnoutResultPage.py (FINAL COMPLETE CODE) --

from ._anvil_designer import BurnoutResultPageTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import math

# Adjust import based on your folder structure
from .. import assessment_logic

class BurnoutResultPage(BurnoutResultPageTemplate):
  def __init__(self, result, score, **properties):
    self.init_components(**properties)

    # Ensure score is 1-100
    score_int = round(max(1, min(100, score)))

    # Update UI Labels
    self.percent_lbl.text = f"{score_int}%"
    self.title_lbl.text = result["level"]

    # Set color if available
    if "color" in result:
      self.percent_lbl.foreground = result["color"]

      # Draw Gauge
    self.draw_gauge(score_int)

    # Set Text Content
    self.explanation_lbl.text = self.get_explanation(result["level"])
    self.recs_lbl.text = self.get_recommendations(result["level"])

  def draw_gauge(self, percent):
    c = self.gauge_canvas

    # Reset context to clear previous drawings
    c.reset_context()

    # Background Arc
    c.begin_path()
    c.arc(150, 150, 120, 180 * math.pi / 180, 360 * math.pi / 180)
    c.line_width = 25
    c.line_cap = "round"
    c.stroke_style = "#e6e6e6"
    c.stroke()
    c.close_path()

    # Filled Arc
    angle_start = 180 * math.pi / 180
    angle_end = (180 + (percent / 100) * 180) * math.pi / 180

    c.begin_path()
    c.arc(150, 150, 120, angle_start, angle_end)
    c.line_width = 25
    c.line_cap = "round"
    # Use dynamic color or default blue
    c.stroke_style = self.percent_lbl.foreground or "#41b8d5"
    c.stroke()
    c.close_path()

  def get_explanation(self, level):
    if "Low" in level:
      return "Your burnout level is low. You have a good balance between demands and resources."
    elif "Moderate" in level:
      return "Your burnout level is moderate. You are currently under sustained pressure."
    else:
      return "Your burnout level is high. You may be feeling depleted and cynical. Please prioritize recovery."

  def get_recommendations(self, level):
    if "Low" in level:
      return "**Tips:** Keep up your current boundaries and self-care routines."
    elif "Moderate" in level:
      return "**Tips:** Schedule disconnect time and review your workload."
    else:
      return "**Action Plan:** Speak to a supervisor or counselor, and take immediate rest."

  def home_btn_click(self, **event_args):
    open_form('MainPage')

  def save_btn_click(self, **event_args):
    # 1. Check Login
    if not anvil.users.get_user():
      choice = alert(
        "You need an account to save your results.",
        buttons=[("Login", "login"), ("Sign up", "signup"), ("Cancel", None)],
        dismissible=True
      )
      if choice == "login":
        open_form("Account.Login")
      elif choice == "signup":
        open_form("Account.Signup")
      return

      # 2. Save via Server
    try:
      score = int(self.percent_lbl.text.strip('%'))
      guidance = self.recs_lbl.text

      # Using the 'log_burnout_assessment' function we added to data_management.py
      anvil.server.call(
        "log_burnout_assessment",
        burnout_score=score,
        guidance=guidance,
        user_inputs=dict(assessment_logic.burnout_data)
      )
      Notification("Burnout result saved.").show()

    except Exception as e:
      print(f"Save error: {e}")
      Notification("Error saving result.", style="danger").show()