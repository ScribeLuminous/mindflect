
from ._anvil_designer import LoginTemplate
from anvil import *
import anvil.users
import anvil.server

class Login(LoginTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

  def login_btn_click(self, **event_args):
    email = self.email_box.text
    password = self.password_box.text

    try:
      # Attempt to log in with email/password
      user = anvil.users.login_with_email(email, password)

      if user:
        # SUCCESS: Go to Account Page
        open_form('Account') 

    except anvil.users.AuthenticationFailed:
      self.error_lbl.text = "Incorrect email or password."
      self.error_lbl.visible = True

  def signup_link_click(self, **event_args):
    # Navigate to the Signup form
    open_form('Signup') 

  def home_btn_click(self, **event_args):
    open_form('MainPage')

  def email_box_change(self, **event_args):
    """This method is called when the text in this text area is edited"""
    pass

  def account_btn_click(self, **event_args):
    open_form('Account.Signup')
    pass
