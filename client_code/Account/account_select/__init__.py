# -- login page --

from ._anvil_designer import account_selectTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.Users


class account_select(account_selectTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.label_error.visible = False  # Assuming you have an error label

  def login_btn_click(self, **event_args):
    """This method is called when the login button is clicked"""
    self.label_error.visible = False  # Clear any previous error

    try:
      # 1. Attempt to log in the user using the built-in form
      user = anvil.users.login_with_form()

      if user:
        # 2. If successful, navigate to the main application page
        open_form("MainPage.levelselect")
      else:
        # This catches the case where the user closes the login box
        pass

    except anvil.users.AuthenticationFailed:
      # 3. Handle login failures (e.g., wrong password)
      self.label_error.text = "Login failed. Check your email and password."
      self.label_error.visible = True

    except Exception as e:
      # Handle other potential errors (e.g., connectivity issues)
      print(f"An unexpected error occurred: {e}")
      self.label_error.text = "An unexpected error occurred during login."
      self.label_error.visible = True

  def account_btn_click(self, **event_args):
    """This method is called when the 'Create Account' button is clicked"""

    # NOTE: If "Account" is your sign-up form, this is correct.
    open_form("Account")
    # Alternatively, you could use: anvil.users.signup_with_form()

  def signup_btn_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass
