
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

  def send_reset_btn_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass

  def forgot_pass_btn_click(self, **event_args):
    """Unhides the reset email box and button."""
    self.reset_email_box.visible = True
    self.send_reset_btn.visible = True
    self.reset_email_box.focus() 

  def send_reset_btn_click(self, **event_args):
    """Actually sends the email when the user clicks 'Send Link'"""
    email = self.reset_email_box.text.strip()

    if email:
      try:
        anvil.users.send_password_reset_email(email)
        Notification("Reset link sent!", style="success").show()

        # Optional: Hide them again after sending
        self.reset_email_box.visible = False
        self.send_reset_btn.visible = False
        self.reset_email_box.text = ""

      except Exception as e:
        alert(f"Error: {e}")
    else:
      Notification("Please enter an email address.", style="warning").show()
