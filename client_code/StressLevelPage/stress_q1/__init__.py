from ._anvil_designer import stress_q1Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from ... import assessment_logic

class stress_q1(stress_q1Template):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.label_error.visible = False # Assume you have an error label
    self.stress_q1_ans.text = str(assessment_logic.user_data['sleep_hours'])

  def handle_input_and_advance(self):
    input_str = self.stress_q1_ans.text

    # Validation: MIN 0, MAX 12
    valid, result = assessment_logic.validate_input(input_str, 0, 12)

    if valid:
      assessment_logic.user_data['sleep_hours'] = result
      open_form("StressLevelPage.stress_q2")
    else:
      self.label_error.text = result
      self.label_error.visible = True

  def q1_next_btn_click(self, **event_args):
    self.handle_input_and_advance()

  def stress_q1_ans_pressed_enter(self, **event_args):
    self.handle_input_and_advance()
