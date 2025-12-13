from ._anvil_designer import levelselectTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class levelselect(levelselectTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def stress_btn_click(self, **event_args):
    open_form("StressLevelPage")
    pass

  def burnout_btn_click(self, **event_args):
    open_form("BurnoutLevelPage")
    pass

  def home_btn_click(self, **event_args):
    open_form('MainPage')
    pass

  def login_btn_click(self, **event_args):
    open_form('Account.Login')
    pass
