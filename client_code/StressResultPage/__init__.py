from ._anvil_designer import StressResultPageTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class StressResultPage(StressResultPageTemplate):
  def __init__(self, result, **properties):
    self.init_components(**properties)

    self.percent_lbl.text = f"{result['percent']}%"
    self.title_lbl.text = "your stress level today"

    self.draw_gauge(result['percent'])
    self.explanation_lbl.text = self.get_explanation(result['level'])

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

def get_explanation(self, level):
  if level == "Low":
    return (
      "Your stress level appears to be low today. "
      "Keep maintaining healthy routines like good sleep and balanced activity."
    )
  elif level == "Moderate":
    return (
      "Your stress level is moderate. You may benefit from short breaks, "
      "light exercise, or mindful breathing."
    )
  else:
    return (
      "Your stress level is high today. Consider prioritizing rest, "
      "reducing screen time, and reaching out for support if needed."
    )


  def save_btn_click(self, **event_args):
    alert("Stress result saved (future user log feature).")
