# --- student_burnout_q3.py ---

from ._anvil_designer import student_burnout_q3Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from .. import assessment_logic 


class student_burnout_q3(student_burnout_q3Template):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.label_error.visible = False
    self.q3_next_btn.enabled = False 

    # KEY: social_media_hours (Max 12 hours/day)
    saved_hours = assessment_logic.burnout_data.get("social_media_hours")

    if saved_hours is not None:
      self.student_burnout_q3_ans.text = str(saved_hours)

    self.live_validate()

  def live_validate(self):
    """
        Validates input instantly (0-12, number required) and toggles error/Next button.
        This question asks for daily social media hours.
        """
    input_str = self.student_burnout_q3_ans.text

    # Validation: MIN 0, MAX 12 (Allows floats for hours)
    valid, result = assessment_logic.validate_input(input_str, 0, 12, require_integer=False)

    if valid:
      self.label_error.visible = False
      self.q3_next_btn.enabled = True
      return True

      # Validation failed.
    self.label_error.text = result
    self.label_error.visible = True
    self.q3_next_btn.enabled = False
    return False

  def handle_input_and_advance(self):
    if self.live_validate():
      # Re-run validation to get the final numeric result (result)
      _, result = assessment_logic.validate_input(
        self.student_burnout_q3_ans.text, 0, 12, require_integer=False
      )

      # SAVE: Save the result to the correct dictionary and key
      assessment_logic.burnout_data["social_media_hours"] = result

      # ADVANCE: Next question is student_burnout_q4
      open_form("BurnoutLevelPage.student_burnout_q4")

    # --- Event Handlers ---

  def q3_next_btn_click(self, **event_args):
    self.handle_input_and_advance()

  def student_burnout_q3_ans_pressed_enter(self, **event_args):
    self.handle_input_and_advance()

  def student_burnout_q3_ans_change(self, **event_args):
    """Called when the text in the text box is edited (live validation)"""
    self.live_validate()

  def q3_back_btn_click(self, **event_args):
    """Go back to the previous question (Q2)"""
    open_form("BurnoutLevelPage.student_burnout_q2") 

  def home_btn_click(self, **event_args):
    open_form("MainPage")