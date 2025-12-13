# -- login page -- 

from ._anvil_designer import LoginTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Login(LoginTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

def login_btn_click(self, **event_args):
  try:
    anvil.users.login_with_form()
    open_form("MainPage.levelselect")
  except:
    Notification("Login failed").show()


  def account_btn_click(self, **event_args):
    open_form("Account")
    pass
