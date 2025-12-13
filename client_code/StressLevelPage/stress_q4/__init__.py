from ._anvil_designer import stress_q4Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class stress_q4(stress_q4Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def q4_next_btn_click(self, **event_args):
    open_form("StressLevelPage.stress_q5")
    pass

  def stress_q4_ans_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    pass
