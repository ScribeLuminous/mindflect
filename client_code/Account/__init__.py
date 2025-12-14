# -- account page -- 
# -- show only once user is logged in successfully -- 

from ._anvil_designer import AccountTemplate
from anvil import *
import anvil.users
import plotly.graph_objects as go
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Account(AccountTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    # Security Check: If someone tries to open this form directly
    # without being logged in, kick them out.
    if not anvil.users.get_user():
      open_form('Login')
      return

    # Load graphs if user is logged in
    # self.load_user_graphs() 

  def reflect_btn_click(self, **event_args):
    open_form("MainPage.levelselect")

  def logout_btn_click(self, **event_args):
    # 1. Log the user out
    anvil.users.logout()

    # 2. Redirect to Main Page (or Login page)
    Notification("You have been logged out.").show()
    open_form("MainPage")

  def stress_plot_click(self, points, **event_args):
    pass

  def burnout_plot_click(self, points, **event_args):
    pass