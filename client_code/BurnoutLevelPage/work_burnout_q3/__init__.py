# --- stress_q1 ---

from ._anvil_designer import work_burnout_q3Template
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from ... import assessment_logic


class work_burnout_q3(work_burnout_q3Template):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.label_error.visible = False
    self.q1_next_btn.enabled = False  # Disable the Next button initially
    self.stress_q1_ans.text = str(assessment_logic.user_data["sleep_hours"])

    # Initial check to see if the default value is valid
    self.live_validate()

  def live_validate(self):
    """Validates input instantly (0-12, allows float) and toggles error/Next button."""
    input_str = self.stress_q1_ans.text

    # Validation: MIN 0, MAX 12
    # Note: We do not check for int() here, as sleep hours can be a decimal (e.g., 7.5)
    valid, result = assessment_logic.validate_input(input_str, 0, 12)

    if valid:
      self.label_error.visible = False
      self.q1_next_btn.enabled = True  # Enable the button
      return True

      # If we reach here, validation failed.
    self.label_error.text = result  # error message from validate_input
    self.label_error.visible = True
    self.q1_next_btn.enabled = False  # Disable the button
    return False

  def handle_input_and_advance(self):
    # We rely on live_validate to check the final state before advancing
    if self.live_validate():
      # Data is valid, save it and advance
      # Re-running validation just to get the final numeric result (result)
      _, result = assessment_logic.validate_input(self.stress_q1_ans.text, 0, 12)

      assessment_logic.user_data["sleep_hours"] = result
      open_form("StressLevelPage.stress_q2")
      # No 'else' needed, as live_validate handles error display

  def q1_next_btn_click(self, **event_args):
    self.handle_input_and_advance()

  def burnout_work_q3_ans_pressed_enter(self, **event_args):
    self.handle_input_and_advance()

    # --- THIS IS THE FUNCTION YOU ASKED FOR ---

  def burnout_work_q3_ans_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    self.live_validate()

  def home_btn_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass

  def q3_ans_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    pass

  def q3_ans_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    pass

  def q3_next_btn_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass

  def q3_back_btn_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass
