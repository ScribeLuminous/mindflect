# -- BurnoutResultPage.py (FINAL, BURNOUT CODE) --

from ._anvil_designer import BurnoutResultPageTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import math


class BurnoutResultPage(BurnoutResultPageTemplate):
  def __init__(self, result, score, **properties):
    self.init_components(**properties)

    # Ensure score is an integer (1 to 100) for clean display
    score_int = round(max(1, min(100, score)))

    # Use 'score_int' for percent label
    self.percent_lbl.text = f"{score_int}%"

    # Use the level (e.g., "Low Burnout") for the title
    self.title_lbl.text = result["level"]

    # Use the result's color for styling 
    try:
      self.percent_lbl.foreground = result['color']
    except KeyError:
      print("Warning: 'color' key missing from result dict.")

      # Use score_int for the gauge
    self.draw_gauge(score_int)

    # Set the Explanation Label
    self.explanation_lbl.text = self.get_explanation(result["level"])

    # Set the Recommendations Label
    self.recs_lbl.text = self.get_recommendations(result["level"])

  def draw_gauge(self, percent):
    c = self.gauge_canvas

    # Clear/Reset context (best practice)
    c.reset_context()

    # --- DRAW BACKGROUND ARC ---
    c.begin_path()
    c.arc(150, 150, 120, 180 * math.pi / 180, 360 * math.pi / 180)  # Angles in radians
    c.line_width = 25  # Set line width for a thick arc
    c.line_cap = "round"
    c.stroke_style = "#e6e6e6"  # Set the background color
    c.stroke()
    c.close_path()

    # --- DRAW FILLED ARC ---
    angle_start_rad = 180 * math.pi / 180
    angle_end_rad = (180 + (percent / 100) * 180) * math.pi / 180

    # Use the calculated result color for the gauge fill
    fill_color = self.title_lbl.foreground or "#41b8d5" 

    c.begin_path()
    c.arc(150, 150, 120, angle_start_rad, angle_end_rad)  # Angles in radians
    c.line_width = 25
    c.line_cap = "round"
    c.stroke_style = fill_color  # Use the dynamic color
    c.stroke()
    c.close_path()

  def get_explanation(self, level):
    if "Low" in level:
      return (
        "Your burnout level is low. You have a good balance between demands "
        "and resources. Maintaining consistent healthy habits is key to resilience."
      )
    elif "Moderate" in level:
      return (
        "Your burnout level is moderate. You are currently under sustained pressure, "
        "which is taxing your reserves. It's time to proactively integrate recovery "
        "strategies to prevent escalation."
      )
    else:  # High Burnout
      return (
        "Your burnout level is high. You are likely experiencing significant "
        "emotional exhaustion and a decreased sense of accomplishment. This "
        "level requires immediate attention and significant changes to your routine."
      )

  def get_recommendations(self, level):
    if "Low" in level:
      return (
        "**Tips for Sustained Wellness:**\n"
        "- **Set Boundaries:** Define clear limits for study/work hours and stick to them.\n"
        "- **Diversify Hobbies:** Engage in activities completely unrelated to your main demands.\n"
        "- **Routine Check-ins:** Regularly assess your energy and mood to catch dips early."
      )
    elif "Moderate" in level:
      return (
        "**Recommendations for Recovery:**\n"
        "- **Restorative Breaks:** Schedule 15-minute breaks that involve no screens (e.g., walking, stretching).\n"
        "- **Time Management:** Practice saying 'No' to non-essential commitments to reclaim time.\n"
        "- **Mindful Sleep:** Establish a consistent, relaxing bedtime routine to maximize sleep quality."
      )
    else:  # High Burnout
      return (
        "**Urgent Action Plan (Prioritize Disengagement):**\n"
        "- **Seek Support:** Connect with a counsellor, student services, or HR immediately.\n"
        "- **Simplify Load:** Temporarily delegate, drop, or postpone non-critical tasks.\n"
        "- **Digital Detox:** Dedicate several hours daily, or one full weekend day, to being completely offline.\n"
        "- **Focus on Basics:** Ensure you are consistently meeting hydration, nutrition, and basic sleep needs."
      )

    # --- Other Handlers ---

  def plot_1_click(self, points, **event_args):
    """This method is called when a data point is clicked."""
    pass

  def save_btn_click_click(self, **event_args):
    alert("Burnout result saved (future user log feature).")
    pass

  def home_btn_click(self, **event_args):
    open_form("MainPage")