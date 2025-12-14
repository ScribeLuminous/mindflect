# --- personal_burnout_q1.py (FINAL CORRECTED CODE) ---

from ._anvil_designer import personal_burnout_q1Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from ... import assessment_logic

class personal_burnout_q1(personal_burnout_q1Template):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.label_error.visible = False

    # Assuming the designer name for the button is q1_next_btn
    self.q1_next_btn.enabled = False 

    # FIX 1 & 2: Use self.burnout_personal_q1_ans.text to access the component
    saved_sleep_hours = assessment_logic.user_data.get("sleep_hours")

    # Initialize text box with saved data if it exists
    if saved_sleep_hours is not None:
      self.burnout_personal_q1_ans.text = str(saved_sleep_hours)

    self.live_validate()

  def live_validate(self):
    """Validates input instantly (0-12, allows float) and toggles error/Next button."""
    # FIX 2: Use self.burnout_personal_q1_ans.text
    input_str = self.burnout_personal_q1_ans.text

    # Validation: MIN 0, MAX 12 (Allows floats for sleep hours)
    valid, result = assessment_logic.validate_input(input_str, 0, 12)

    if valid:
      self.label_error.visible = False
      self.q1_next_btn.enabled = True
      return True

    # If we reach here, validation failed.
    self.label_error.text = result
    self.label_error.visible = True
    self.q1_next_btn.enabled = False
    return False

  def handle_input_and_advance(self):
    if self.live_validate():
      # Re-running validation just to get the final numeric result (result)
      # FIX 4: Use max 12 for consistency
      _, result = assessment_logic.validate_input(self.burnout_personal_q1_ans.text, 0, 12)

      assessment_logic.user_data["sleep_hours"] = result

      # FIX 3: Advance to the NEXT personal burnout question
      open_form("BurnoutLevelPage.personal_burnout_q2")

  def q1_next_btn_click(self, **event_args):
    self.handle_input_and_advance()

  def burnout_personal_q1_ans_pressed_enter(self, **event_args):
    self.handle_input_and_advance()

  def burnout_personal_q1_ans_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    self.live_validate()

  def home_btn_click(self, **event_args):
    open_form("MainPage")
    pass