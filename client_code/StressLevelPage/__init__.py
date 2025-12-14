from ._anvil_designer import StressLevelPageTemplate
from anvil import *
import anvil.server
import anvil.users

class StressLevelPage(StressLevelPageTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

  def stress_con_click(self, **event_args):
    # This is the only line that matters here
    open_form("StressLevelPage.stress_q1") 
    pass

  def login_btn_click(self, **event_args):
    open_form("Account") 
    pass

  def home_btn_click(self, **event_args):
    open_form("MainPage") 
    pass
