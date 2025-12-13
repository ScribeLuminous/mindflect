# -- stress_q4.py (FINAL FULLY CORRECTED AND INDENTED) --

from ._anvil_designer import stress_q4Template
from anvil import *
from ... import assessment_logic

class stress_q4(stress_q4Template):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.label_error.visible = False
    self.q4_next_btn.enabled = False

    # --- FIX: Load saved data, if it exists (Indented correctly inside __init__) ---
    saved_value = assessment_logic.user_data['diet_quality_1_10']
    if saved_value is not None:
      # If data is saved, display it and enable the button
      self.stress_q4_ans.text = str(saved_value)
      self.q4_next_btn.enabled = True
    else:
      # Otherwise, start with an empty text box
      self.stress_q4_ans.text = "" 

  def live_validate(self):
    # All lines below are indented correctly inside the method
    valid, result = assessment_logic.validate_input(
      self.stress_q4_ans.text,
      1,
      10,
      require_integer=True
    )

    if valid:
      self.label_error.visible = False
      self.q4_next_btn.enabled = True
      return True

    self.label_error.text = result
    self.label_error.visible = True
    self.q4_next_btn.enabled = False
    return False

  def handle_input_and_advance(self):
    # 1. Check validation. If invalid, stop execution.
    if not self.live_validate():
      # live_validate already sets the error message and disables the button
      return

      # 2. VALIDATION PASSED: Now get the clean numeric result.
      # This code is aligned with the 'if' statement's scope.
    _, result = assessment_logic.validate_input(
      self.stress_q4_ans.text,
      1,
      10,
      require_integer=True
    )

    # 3. Save the result and advance
    assessment_logic.user_data["diet_quality_1_10"] = result
    open_form("StressLevelPage.stress_q5")
  
  def stress_q4_ans_change(self, **event_args):
    # Indented correctly
    self.live_validate()

  def stress_q4_ans_pressed_enter(self, **event_args):
    # Indented correctly
    self.handle_input_and_advance()

  def q4_next_btn_click(self, **event_args):
    # Indented correctly
    self.handle_input_and_advance()

  def q4_back_btn_click(self, **event_args):
    # Indented correctly
    open_form("StressLevelPage.stress_q3")