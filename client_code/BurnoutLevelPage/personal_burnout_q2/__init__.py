# --- personal_burnout_q2.py ---

from ._anvil_designer import personal_burnout_q2Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from .. import assessment_logic 


class personal_burnout_q2(personal_burnout_q2Template):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.label_error.visible = False
    self.q2_next_btn.enabled = False 

    # KEY: sleep_hours (from personal burnout section, up to 12 hours)
    saved_hours = assessment_logic.burnout_data.get("sleep_hours")

    if saved_hours is not None:
      self.personal_burnout_q2_ans.text = str(saved_hours)

    self.live_validate()

  def live_validate(self):
    """
        Validates input instantly (0-12, number required) for daily sleep hours.
        """
    input_str = self.personal_burnout_q2_ans.text

    # Validation: MIN 0, MAX 12 (Allows floats for hours, like 7.5)
    valid, result = assessment_logic.validate_input(input_str, 0, 12, require_integer=False)

    if valid:
      self.label_error.visible = False
      self.q2_next_btn.enabled = True
      return True

      # Validation failed.
    self.label_error.text = result
    self.label_error.visible = True
    self.q2_next_btn.enabled = False
    return False

  def handle_input_and_advance(self):
    if self.live_validate():
      # Re-run validation to get the final numeric result (result)
      _, result = assessment_logic.validate_input(
        self.personal_burnout_q2_ans.text, 0, 12, require_integer=False
      )

      # SAVE: Save the result to the correct dictionary and key
      assessment_logic.burnout_data["sleep_hours"] = result

      # ADVANCE: Next personal question is personal_burnout_q3
      open_form("BurnoutLevelPage.personal_burnout_q3")

    # --- Event Handlers ---

  def q2_next_btn_click(self, **event_args):
    self.handle_input_and_advance()

  def personal_burnout_q2_ans_pressed_enter(self, **event_args):
    self.handle_input_and_advance()

  def personal_burnout_q2_ans_change(self, **event_args):
    """Called when the text in the text box is edited (live validation)"""
    self.live_validate()

  def q2_back_btn_click(self, **event_args):
    """Go back to the previous question (Personal Q1)"""
    open_form("BurnoutLevelPage.personal_burnout_q1") 

  def home_btn_click(self, **event_args):
    open_form("MainPage")