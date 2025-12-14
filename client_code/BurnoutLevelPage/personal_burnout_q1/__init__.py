# --- personal_burnout_q1.py ---

from ._anvil_designer import personal_burnout_q1Template
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from .. import assessment_logic 


class personal_burnout_q1(personal_burnout_q1Template):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.label_error.visible = False
    self.q1_next_btn.enabled = False 

    # KEY: daily_stress (Scale 0-10, integer)
    saved_rating = assessment_logic.burnout_data.get("daily_stress")

    if saved_rating is not None:
      self.personal_burnout_q1_ans.text = str(saved_rating)

    self.live_validate()

  def live_validate(self):
    """
        Validates input instantly (0-10, integer required) for daily stress rating.
        """
    input_str = self.personal_burnout_q1_ans.text

    # Validation: MIN 0, MAX 10 (REQUIRES INTEGER for a rating scale)
    valid, result = assessment_logic.validate_input(input_str, 0, 10, require_integer=True)

    if valid:
      self.label_error.visible = False
      self.q1_next_btn.enabled = True
      return True

      # Validation failed.
    self.label_error.text = result
    self.label_error.visible = True
    self.q1_next_btn.enabled = False
    return False

  def handle_input_and_advance(self):
    if self.live_validate():
      # Re-run validation to get the final numeric result (result)
      _, result = assessment_logic.validate_input(
        self.personal_burnout_q1_ans.text, 0, 10, require_integer=True
      )

      # SAVE: Save the result to the correct dictionary and key
      assessment_logic.burnout_data["daily_stress"] = result

      # ADVANCE: Next personal question is personal_burnout_q2
      open_form("BurnoutLevelPage.personal_burnout_q2")

    # --- Event Handlers ---

  def q1_next_btn_click(self, **event_args):
    self.handle_input_and_advance()

  def personal_burnout_q1_ans_pressed_enter(self, **event_args):
    self.handle_input_and_advance()

  def personal_burnout_q1_ans_change(self, **event_args):
    """Called when the text in the text box is edited (live validation)"""
    self.live_validate()

  def q1_back_btn_click(self, **event_args):
    """Go back to the last student question (Q6)"""
    open_form("BurnoutLevelPage.student_burnout_q6") 

  def home_btn_click(self, **event_args):
    open_form("MainPage")