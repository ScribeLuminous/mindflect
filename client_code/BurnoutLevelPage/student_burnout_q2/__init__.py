# --- student_burnout_q2.py ---

from ._anvil_designer import student_burnout_q2Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from .. import assessment_logic 


class student_burnout_q2(student_burnout_q2Template):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.label_error.visible = False
    self.q2_next_btn.enabled = False 

    # KEY: mental_health_rating (Scale 1-10)
    saved_rating = assessment_logic.burnout_data.get("mental_health_rating")

    if saved_rating is not None:
      self.student_burnout_q2_ans.text = str(saved_rating)

    self.live_validate()

  def live_validate(self):
    """
        Validates input instantly (1-10, integer required) and toggles error/Next button.
        This question asks for Mental Health Rating.
        """
    input_str = self.student_burnout_q2_ans.text

    # Validation: MIN 1, MAX 10 (REQUIRES INTEGER for a rating scale)
    valid, result = assessment_logic.validate_input(input_str, 1, 10, require_integer=True)

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
        self.student_burnout_q2_ans.text, 1, 10, require_integer=True
      )

      # SAVE: Save the result to the correct dictionary and key
      assessment_logic.burnout_data["mental_health_rating"] = result

      # ADVANCE: Next question is student_burnout_q3
      open_form("BurnoutLevelPage.student_burnout_q3")

    # --- Event Handlers ---

# Replace your current q2_next_btn_click with this:
  def q2_next_btn_click(self, **event_args):
    # This directly includes the logic from handle_input_and_advance
    if self.live_validate():
      # Re-run validation to get the final numeric result (result)
      _, result = assessment_logic.validate_input(
        self.student_burnout_q2_ans.text, 1, 10, require_integer=True
      )
  
      # SAVE: Save the result
      assessment_logic.burnout_data["mental_health_rating"] = result
  
      # ADVANCE: Next question is student_burnout_q3
      open_form("BurnoutLevelPage.student_burnout_q3")

  def student_burnout_q2_ans_pressed_enter(self, **event_args):
    self.handle_input_and_advance()

  def student_burnout_q2_ans_change(self, **event_args):
    """Called when the text in the text box is edited (live validation)"""
    self.live_validate()

  def q2_back_btn_click(self, **event_args):
    """Go back to the previous question (Q1)"""
    open_form("BurnoutLevelPage.student_burnout_q1") 

  def home_btn_click(self, **event_args):
    open_form("MainPage")