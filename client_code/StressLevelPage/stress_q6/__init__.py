# --- stress_q6.py ---

from ._anvil_designer import stress_q6Template
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from ... import assessment_logic

class stress_q6(stress_q6Template):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.label_error.visible = False

    # Check if q6_submit_btn exists before trying to access it
    if hasattr(self, 'q6_submit_btn'):
      self.q6_submit_btn.enabled = False

      # Initialize text box with saved data
    saved_mood = assessment_logic.user_data.get('mood_level_1_10')
    if saved_mood is not None:
      self.stress_q6_ans.text = str(saved_mood)

    self.live_validate()

  def live_validate(self):
    """Validates input instantly (1-10, MUST be integer) and toggles error/Submit button."""
    input_str = self.stress_q6_ans.text

    # Strict Validation: MIN 1, MAX 10, MUST be integer
    valid, result = assessment_logic.validate_input(input_str, 1, 10, require_integer=True)

    if valid:
      self.label_error.visible = False
      if hasattr(self, 'q6_submit_btn'):
        self.q6_submit_btn.enabled = True
      return True

      # Validation failed.
    self.label_error.text = result 
    self.label_error.visible = True
    if hasattr(self, 'q6_submit_btn'):
      self.q6_submit_btn.enabled = False 
    return False

  def handle_input_and_submit(self):
    """Handles validation, saving, calculation, and form transition."""
    if self.live_validate(): 
      # 1. Save the input value
      assessment_logic.user_data['mood_level_1_10'] = int(float(self.stress_q6_ans.text))

      # 2. PERFORM FINAL CALCULATION
      # Corrected call: get_result_feedback returns the result_dict AND the score
      final_result, final_score = assessment_logic.get_result_feedback() 

      # 3. OPEN RESULTS PAGE and pass the data
      open_form("StressResultPage", result=final_result, score=final_score)

    # ===============================
    # EVENT HANDLERS (Cleaned and consolidated)
    # ===============================

  def q6_submit_btn_click(self, **event_args):
    """Called when the Submit button is clicked."""
    self.handle_input_and_submit()

  def stress_q6_ans_pressed_enter(self, **event_args):
    """Called when the user presses Enter in the text box."""
    self.handle_input_and_submit()

  def stress_q6_ans_change(self, **event_args):
    """Called when the text in the text box is edited (live validation)."""
    self.live_validate()

  def q5_back_btn_click(self, **event_args):
    """Go back to the previous question (Stress Q5)."""
    open_form("StressLevelPage.stress_q5")

  def home_btn_click(self, **event_args):
    """Navigates to the main page."""
    open_form('MainPage')