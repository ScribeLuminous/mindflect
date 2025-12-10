from ._anvil_designer import StressLevelPageTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class StressLevelPage(StressLevelPageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def stress_con_click(self, **event_args):
    open_form("MainPage.levelselect")
    pass
