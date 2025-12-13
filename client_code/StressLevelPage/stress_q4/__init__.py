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
    self.stress_q4_ans.text = str(assessment_logic.user_data['diet_quality_1_10'])

  def handle_input_and_advance(self):
    input_str = self.stress_q4_ans.text

    # Validation: MIN 1, MAX 10. Check if input is a whole number (int).
    valid, result = assessment_logic.validate_input(input_str, 1, 10)

    if valid and result != int(result):
      valid = False
      result = "Please enter a whole number (1 to 10)."

    if valid:
      assessment_logic.user_data['diet_quality_1_10'] = int(result)
      open_form("StressLevelPage.stress_q5")
    else:
      self.label_error.text = result
      self.label_error.visible = True

  def q4_next_btn_click(self, **event_args):
    self.handle_input_and_advance()

  def stress_q4_ans_pressed_enter(self, **event_args):
    self.handle_input_and_advance()