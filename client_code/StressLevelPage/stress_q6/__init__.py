from ._anvil_designer import stress_q6Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from ... import assessment_logic

class stress_q6(stress_q6Template):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.label_error.visible = False
    self.stress_q6_ans.text = str(assessment_logic.user_data['mood_level_1_10'])

  def handle_input_and_submit(self):
    input_str = self.stress_q6_ans.text

    # Validation: MIN 1, MAX 10. Check if input is a whole number (int).
    valid, result = assessment_logic.validate_input(input_str, 1, 10)

    if valid and result != int(result):
      valid = False
      result = "Please enter a whole number (1 to 10)."

    if valid:
      # 1. SAVE FINAL DATA POINT
      assessment_logic.user_data['mood_level_1_10'] = int(result)

      # 2. PERFORM FINAL CALCULATION
      final_score = assessment_logic.calculate_total_stress()
      final_result = assessment_logic.get_result_feedback(final_score)

      # 3. OPEN RESULTS PAGE and pass the data
      open_form("StressResultPage", result=final_result, score=final_score)
    else:
      self.label_error.text = result
      self.label_error.visible = True

  def q6_submit_btn_click(self, **event_args):
    self.handle_input_and_submit()

  def stress_q6_ans_pressed_enter(self, **event_args):
    self.handle_input_and_submit()