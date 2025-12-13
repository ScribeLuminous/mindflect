from ._anvil_designer import StressLevelPageTemplate
from anvil import *

class StressLevelPage(StressLevelPageTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

  def stress_con_click(self, **event_args):
    # This is the only line that matters here
    open_form("StressLevelPage.stress_q1") 
    pass