# -- login page -- 

from ._anvil_designer import LoginTemplate
from anvil import *
import anvil.Users

class Login(LoginTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.label_error.visible = False

  def login_btn_click(self, **event_args):
    self.label_error.visible = False
    try:
      # Calls the Anvil user authentication service
      user = anvil.users.login_with_form() 

      if user:
        open_form("MainPage.levelselect")
    except:
      self.label_error.text = "Invalid email or password."
      self.label_error.visible = True

  def signup_btn_click(self, **event_args):
    open_form("Signup")