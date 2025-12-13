# -- StressResultPage.py (FIXED) --

from ._anvil_designer import StressResultPageTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class StressResultPage(StressResultPageTemplate):
  # 1. FIXED __init__ to accept 'score'
  def __init__(self, result, score, **properties):
    self.init_components(**properties)

    # Ensure score is an integer (1 to 100) for clean display
    score_int = round(max(1, min(100, score))) 

    # 2. FIXED: Use 'score_int' for percent label
    self.percent_lbl.text = f"{score_int}%"

    # Use the level (e.g., "Low Stress") for the title
    self.title_lbl.text = result['level']

    # Use the result's color for styling if you've set it up
    self.percent_lbl.foreground = result['color']

    # Use score_int for the gauge
    self.draw_gauge(score_int)

    # Set the Explanation Label
    self.explanation_lbl.text = self.get_explanation(result['level'])

    # 3. NEW: Set the Recommendations Label
    self.recs_lbl.text = self.get_recommendations(result['level'])


  def draw_gauge(self, percent):
    c = self.gauge_canvas
    c.clear()

    # background arc
    c.arc(150, 150, 120, 180, 360, fill="#e6e6e6")

    # filled arc
    angle = 180 + (percent / 100) * 180
    c.arc(150, 150, 120, 180, angle, fill="#41b8d5")

  def plot_1_click(self, points, **event_args):
    """This method is called when a data point is clicked."""
    pass

  def save_btn_click_click(self, **event_args):
    alert("Stress result saved (future user log feature).")
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

    # 4. NEW METHOD: Provides specific actions based on stress level
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