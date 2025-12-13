# --- stress_q4.py (FIXED for Live Validation, 1-10 Integer) ---

from ._anvil_designer import stress_q4Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from ... import assessment_logic

class stress_q4(stress_q4Template):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.label_error.visible = False
    self.q4_next_btn.enabled = False  # Disable the Next button initially
    self.stress_q4_ans.text = str(assessment_logic.user_data['diet_quality_1_10'])

    # Initial check to see if the default value is valid
    self.live_validate() 

  def live_validate(self):
    """Validates input instantly (1-10, MUST be integer) and toggles error/Next button."""
    input_str = self.stress_q4_ans.text

    # We temporarily allow a slightly wider range (0-11) during live typing
    # to prevent errors if the user is typing "1" or "10"
    valid, result = assessment_logic.validate_input(input_str, 0, 11)

    if valid:
      # Check 1: Must be a whole number
      if result != int(result):
        self.label_error.text = "Value must be a whole number (no decimals)."
        self.label_error.visible = True
        self.q4_next_btn.enabled = False
        return False

        # Check 2: Must be within the final 1-10 range
      if 1 <= int(result) <= 10:
        self.label_error.visible = False
        self.q4_next_btn.enabled = True # Enable the button
        return True

        # If it's 0 or 11 (the edges of the temporary range)
      self.label_error.text = "Value must be between 1 and 10."
      self.label_error.visible = True
      self.q4_next_btn.enabled = False
      return False

      # If we reach here, the input wasn't even a number or was outside the 0-11 range.
    self.label_error.text = result # error message from validate_input
    self.label_error.visible = True
    self.q4_next_btn.enabled = False 
    return False

  def handle_input_and_advance(self):
    # We rely on live_validate to check the final state before advancing
    if self.live_validate(): 
      # Data is valid, save it and advance
      # We already validated it's a whole number in 1-10, so we can cast to int safely.
      assessment_logic.user_data['diet_quality_1_10'] = int(float(self.stress_q4_ans.text))
      open_form("StressLevelPage.stress_q5")
      # No 'else' needed, as live_validate handles error display

  def q4_next_btn_click(self, **event_args):
    self.handle_input_and_advance()

  def stress_q4_ans_pressed_enter(self, **event_args):
    self.handle_input_and_advance()

    # --- NEW CHANGE EVENT HANDLER ---
  def stress_q4_ans_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    self.live_validate()

  def q3_back_btn_click(self, **event_args):
    open_form('StressLevelPage.stress_q3')
    pass
