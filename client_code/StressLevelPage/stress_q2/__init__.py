from ._anvil_designer import stress_q2Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from ... import assessment_logic

class stress_q2(stress_q2Template):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.label_error.visible = False
    self.stress_q2_ans.text = str(assessment_logic.user_data['daily_exercise_mins'])

  def handle_input_and_advance(self):
    input_str = self.stress_q2_ans.text

    # Validation: MIN 0, MAX 60
    valid, result = assessment_logic.validate_input(input_str, 0, 60)

    if valid:
      assessment_logic.user_data['daily_exercise_mins'] = result
      open_form("StressLevelPage.stress_q3")
    else:
      self.label_error.text = result
      self.label_error.visible = True

  def q2_next_btn_click(self, **event_args):
    self.handle_input_and_advance()

  def stress_q2_ans_pressed_enter(self, **event_args):
    self.handle_input_and_advance()