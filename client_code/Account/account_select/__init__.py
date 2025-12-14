# -- account_select page --
# -- activate only if user is not login and they finished the test

from ._anvil_designer import account_selectTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

import anvil.users

class account_select(account_selectTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

  def login_btn_click(self, **event_args):
    try:
      user = anvil.users.login_with_form()
      if user:
        self.raise_event("x-close-alert", value=True)
    except:
      Notification("Login failed").show()

  def signup_btn_click(self, **event_args):
    try:
      user = anvil.users.signup_with_form()
      if user:
        self.raise_event("x-close-alert", value=True)
    except:
      Notification("Signup failed").show()
