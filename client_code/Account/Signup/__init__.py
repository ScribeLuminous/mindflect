# -- sign up page -- 

from ._anvil_designer import SignupTemplate
from anvil import *
import anvil.users
import anvil.server

class Signup(SignupTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

  def signup_btn_click(self, **event_args):
    email = self.email_box.text
    password = self.password_box.text

    try:
      # Attempt to sign up
      user = anvil.users.signup_with_email(email, password)

      if user:
        # SUCCESS: Go to Account Page immediately
        # (Or you can send them to Login if you require email verification first)
        open_form('Account')

    except anvil.users.UserExists:
      self.error_lbl.text = "This email is already registered. Please log in."
      self.error_lbl.visible = True
    except anvil.users.PasswordNotComplex:
      self.error_lbl.text = "Password is too weak."
      self.error_lbl.visible = True

  def login_link_click(self, **event_args):
    open_form('Login')

  def home_btn_click(self, **event_args):
    open_form('MainPage')
    pass
