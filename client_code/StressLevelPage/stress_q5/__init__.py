# --- stress_q5.py (FIXED for Live Validation, 1-10 Integer, + Handler Fix) ---

from ._anvil_designer import stress_q5Template
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from ... import assessment_logic

class stress_q5(stress_q5Template):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.label_error.visible = False
    self.q5_next_btn.enabled = False
    self.stress_q5_ans.text = str(assessment_logic.user_data['productivity_score_1_10'])
    self.live_validate() 

  def live_validate(self):
    """Validates input instantly (1-10, MUST be integer) and toggles error/Next button."""
    input_str = self.stress_q5_ans.text

    # Use require_integer=True in validate_input for cleaner check
    valid, result = assessment_logic.validate_input(input_str, 1, 10, require_integer=True)

    if valid:
      self.label_error.visible = False
      self.q5_next_btn.enabled = True
      return True

      # If we reach here, validation failed.
    self.label_error.text = result 
    self.label_error.visible = True
    self.q5_next_btn.enabled = False 
    return False

  def handle_input_and_advance(self):
    if self.live_validate(): 
      # Data is valid, save it and advance
      assessment_logic.user_data['productivity_score_1_10'] = int(float(self.stress_q5_ans.text))
      open_form("StressLevelPage.stress_q6")

  def q5_next_btn_click(self, **event_args):
    self.handle_input_and_advance()

    # --- FIX for Warning ---
  def q4_next_btn_click(self, **event_args):
    # Alias method if designer expects q4_next_btn_click on q5_next_btn
    self.handle_input_and_advance()

  def stress_q5_ans_pressed_enter(self, **event_args):
    self.handle_input_and_advance()

  def stress_q5_ans_change(self, **event_args):
    self.live_validate()

  def q5_back_btn_click(self, **event_args):
    open_form('StressLevelPage.stress_q4')

  def home_btn_click(self, **event_args):
    open_form('MainPage')
    pass
