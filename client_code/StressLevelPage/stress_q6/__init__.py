from ._anvil_designer import stress_q6Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class stress_q6(stress_q6Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def q6_submit_btn_click(self, **event_args):
    try:
      features = {
        "sleep_hours": float(self.stress_q1Template.text),
        "daily_exercise_mins": float(self.stress_q2Template.text),
        "screen_time_hours": float(self.stress_q3Template.text),
        "diet_quality_1_10": int(self.stress_q4Template.text),
        "productivity_score_1_10": int(self.stress_q5Template.text),
        "mood_level_1_10": int(self.stress_q6Template.text),
      }
    except:
      alert("Please enter valid numbers for all questions.")
      open_form("StressLevelPage.stress_q1")
      return

    result = anvil.server.call("predict_stress", features)
    open_form("StressResultPage", result=result)
