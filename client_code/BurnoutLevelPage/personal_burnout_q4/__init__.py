# --- personal_burnout_q4.py ---

from ._anvil_designer import personal_burnout_q4Template
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from .. import assessment_logic 


class personal_burnout_q4(personal_burnout_q4Template):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.label_error.visible = False
    self.q4_next_btn.enabled = False 

    # KEY: daily_steps (Max 20000, integer)
    saved_steps = assessment_logic.burnout_data.get("daily_steps")

    if saved_steps is not None:
      self.personal_burnout_q4_ans.text = str(saved_steps)

    self.live_validate()

  def live_validate(self):
    """
        Validates input instantly (0-20000, integer required) for daily steps.
        """
    input_str = self.personal_burnout_q4_ans.text

    # Validation: MIN 0, MAX 20000 (REQUIRES INTEGER for step count)
    # Note: We cap at 20000 based on your logic's divisor, but allow higher input if needed.
    # For strict validation, we use 20000 as max here.
    valid, result = assessment_logic.validate_input(input_str, 0, 20000, require_integer=True)

    if valid:
      self.label_error.visible = False
      self.q4_next_btn.enabled = True
      return True

      # Validation failed.
    self.label_error.text = result
    self.label_error.visible = True
    self.q4_next_btn.enabled = False
    return False

  def handle_input_and_advance(self):
    if self.live_validate():
      # Re-run validation to get the final numeric result (result)
      # Use a high maximum to capture inputs > 20000, as the calculation handles the scaling.
      _, result = assessment_logic.validate_input(
        self.personal_burnout_q4_ans.text, 0, 50000, require_integer=True # Use a higher practical max here
      )

      # SAVE: Save the result to the correct dictionary and key
      assessment_logic.burnout_data["daily_steps"] = result

      # ADVANCE: Next personal question is personal_burnout_q5
      open_form("BurnoutLevelPage.personal_burnout_q5")

    # --- Event Handlers ---

  def q4_next_btn_click(self, **event_args):
    self.handle_input_and_advance()

  def personal_burnout_q4_ans_pressed_enter(self, **event_args):
    self.handle_input_and_advance()

  def personal_burnout_q4_ans_change(self, **event_args):
    """Called when the text in the text box is edited (live validation)"""
    self.live_validate()

  def q4_back_btn_click(self, **event_args):
    """Go back to the previous question (Personal Q3)"""
    open_form("BurnoutLevelPage.personal_burnout_q3") 

  def home_btn_click(self, **event_args):
    open_form("MainPage")