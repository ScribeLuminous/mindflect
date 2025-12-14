# -- account page -- 
# -- show only once user is logged in successfully -- 

from ._anvil_designer import AccountTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Account(AccountTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def reflect_btn_click(self, **event_args):
    open_form("MainPage.levelselect")
    pass

  def logout_btn_click(self, **event_args):
    open_form("MainPage")
    pass
