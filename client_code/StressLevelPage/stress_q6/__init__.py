# --- stress_q6.py (FINAL FIX) ---

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
    self.q6_submit_btn.enabled = False
    self.stress_q6_ans.text = str(assessment_logic.user_data['mood_level_1_10'])
    self.live_validate() 

  def live_validate(self):
    """Validates input instantly (1-10, MUST be integer) and toggles error/Submit button."""
    input_str = self.stress_q6_ans.text

    # Strict Validation: MIN 1, MAX 10, MUST be integer
    valid, result = assessment_logic.validate_input(input_str, 1, 10, require_integer=True)

    if valid:
      self.label_error.visible = False
      self.q6_submit_btn.enabled = True
      return True

      # If we reach here, the input wasn't valid (not a number, wrong range, or not integer).
    self.label_error.text = result 
    self.label_error.visible = True
    self.q6_submit_btn.enabled = False 
    return False

  def handle_input_and_submit(self):
    if self.live_validate(): 
      assessment_logic.user_data['mood_level_1_10'] = int(float(self.stress_q6_ans.text))

      # 2. PERFORM FINAL CALCULATION
      final_score = assessment_logic.calculate_total_stress()

      # This call should now work as get_result_feedback is defined
      final_result = assessment_logic.get_result_feedback(final_score) 

      # 3. OPEN RESULTS PAGE and pass the data
      open_form("StressResultPage", result=final_result, score=final_score)

  def q6_submit_btn_click(self, **event_args):
    self.handle_input_and_submit()

  def stress_q6_ans_pressed_enter(self, **event_args):
    self.handle_input_and_submit()

  def stress_q6_ans_change(self, **event_args):
    self.live_validate()

    # --- FIX for Warning ---
  def q5_back_btn_click(self, **event_args):
    # Alias method if designer expects q5_back_btn_click on q6_back_btn
    open_form("StressLevelPage.stress_q5")