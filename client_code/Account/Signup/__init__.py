# -- sign up page -- 

from ._anvil_designer import SignupTemplate
from anvil import *
import anvil.users

class Signup(SignupTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

  def signup_btn_click(self, **event_args):
    try:
      user = anvil.users.signup_with_form()
      if user:
        Notification("Account created successfully 💙").show()
        open_form("MainPage.levelselect")
    except:
      Notification("Signup failed. Try again.").show()