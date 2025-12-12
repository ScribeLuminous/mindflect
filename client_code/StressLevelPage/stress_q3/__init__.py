from ._anvil_designer import stress_q3Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class stress_q3(stress_q3Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def q3_next_btn_click(self, **event_args):
    open_form("StressLevelPage.stress_q2")
    pass
