from ._anvil_designer import stress_q1Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class stress_q1(stress_q1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

  def q1_next_btn_click(self, **event_args):
    open_form("StressLevelPage.stress_q2")
  pass

  def stress_q1_ans_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    pass
