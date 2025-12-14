# --- student_burnout_q4.py ---

from ._anvil_designer import student_burnout_q4Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from .. import assessment_logic 


class student_burnout_q4(student_burnout_q4Template):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.label_error.visible = False
    self.q4_next_btn.enabled = False 

    # KEY: attendance_percentage (Scale 0-100)
    saved_attendance = assessment_logic.burnout_data.get("attendance_percentage")

    if saved_attendance is not None:
      self.student_burnout_q4_ans.text = str(saved_attendance)

    self.live_validate()

  def live_validate(self):
    """
        Validates input instantly (0-100, integer required) for attendance percentage.
        """
    input_str = self.student_burnout_q4_ans.text

    # Validation: MIN 0, MAX 100 (REQUIRES INTEGER for a percentage)
    valid, result = assessment_logic.validate_input(input_str, 0, 100, require_integer=True)

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
      _, result = assessment_logic.validate_input(
        self.student_burnout_q4_ans.text, 0, 100, require_integer=True
      )

      # SAVE: Save the result to the correct dictionary and key
      assessment_logic.burnout_data["attendance_percentage"] = result

      # ADVANCE: Next question is student_burnout_q5
      open_form("BurnoutLevelPage.student_burnout_q5")

    # --- Event Handlers (Using standard names, assuming Designer linkage is now fixed) ---

  def q4_next_btn_click(self, **event_args):
    self.handle_input_and_advance()

  def student_burnout_q4_ans_pressed_enter(self, **event_args):
    self.handle_input_and_advance()

  def student_burnout_q4_ans_change(self, **event_args):
    """Called when the text in the text box is edited (live validation)"""
    self.live_validate()

  def q4_back_btn_click(self, **event_args):
    """Go back to the previous question (Q3)"""
    open_form("BurnoutLevelPage.student_burnout_q3") 

  def home_btn_click(self, **event_args):
    open_form("MainPage")