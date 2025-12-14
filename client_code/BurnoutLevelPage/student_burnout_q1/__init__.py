# --- student_burnout_q1.py (FINAL, CLEAN HANDLERS) ---

from ._anvil_designer import student_burnout_q1Template
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from .. import assessment_logic 


class student_burnout_q1(student_burnout_q1Template):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.label_error.visible = False
    self.q1_next_btn.enabled = False 

    saved_study_hours = assessment_logic.burnout_data.get("study_hours_per_day")

    if saved_study_hours is not None:
      self.student_burnout_q1_ans.text = str(saved_study_hours)

    self.live_validate()

  def live_validate(self):
    """
        Validates input instantly (1-12, number required) and toggles error/Next button.
        """
    input_str = self.student_burnout_q1_ans.text

    # Validation: MIN 1, MAX 12 (Allows floats for hours)
    valid, result = assessment_logic.validate_input(input_str, 1, 12, require_integer=False)

    if valid:
      self.label_error.visible = False
      self.q1_next_btn.enabled = True
      return True

    self.label_error.text = result
    self.label_error.visible = True
    self.q1_next_btn.enabled = False
    return False

  def handle_input_and_advance(self):
    if self.live_validate():
      _, result = assessment_logic.validate_input(
        self.student_burnout_q1_ans.text, 1, 12, require_integer=False
      )

      assessment_logic.burnout_data["study_hours_per_day"] = result

      # Advance to the next student question
      open_form("BurnoutLevelPage.student_burnout_q2")

    # --- Event Handlers (Using the confirmed, standard names) ---

  def q1_next_btn_click(self, **event_args):
    self.handle_input_and_advance()

  def student_burnout_q1_ans_pressed_enter(self, **event_args):
    self.handle_input_and_advance()

  def student_burnout_q1_ans_change(self, **event_args):
    self.live_validate()

  def q1_back_btn_click(self, **event_args):
    open_form("BurnoutLevelPage") 

  def home_btn_click(self, **event_args):
    open_form("MainPage")