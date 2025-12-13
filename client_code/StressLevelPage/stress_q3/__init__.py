# --- stress_q3.py (FINAL VERIFIED CODE) ---

from ._anvil_designer import stress_q3Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from ... import assessment_logic

class stress_q3(stress_q3Template):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.label_error.visible = False
    self.q3_next_btn.enabled = False  # Disable the Next button initially
    self.stress_q3_ans.text = str(assessment_logic.user_data['screen_time_hours'])

    # Initial check to see if the default value is valid
    self.live_validate() 

  def live_validate(self):
    """Validates input instantly (0-16, allows float) and toggles error/Next button."""
    input_str = self.stress_q3_ans.text

    # Validation: MIN 0, MAX 16
    valid, result = assessment_logic.validate_input(input_str, 0, 16)

    if valid:
      self.label_error.visible = False
      self.q3_next_btn.enabled = True # Enable the button
      return True

      # If we reach here, validation failed.
    self.label_error.text = result 
    self.label_error.visible = True
    self.q3_next_btn.enabled = False # Disable the button
    return False

  def handle_input_and_advance(self):
    if self.live_validate(): 
      # Data is valid, save it and advance
      _, result = assessment_logic.validate_input(self.stress_q3_ans.text, 0, 16)

      assessment_logic.user_data['screen_time_hours'] = result
      open_form("StressLevelPage.stress_q4")

  def q3_next_btn_click(self, **event_args):
    self.handle_input_and_advance()

  def stress_q3_ans_pressed_enter(self, **event_args):
    self.handle_input_and_advance()

  def stress_q3_ans_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    self.live_validate()

  def q3_back_btn_click(self, **event_args):
    open_form("StressLevelPage.stress_q2")
    pass
