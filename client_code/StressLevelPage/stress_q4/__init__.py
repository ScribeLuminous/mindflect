# -- stress_q4.py (FINAL & VERIFIED WORKING VERSION) --

from ._anvil_designer import stress_q4Template
from anvil import *
import anvil.users
from ... import assessment_logic
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class stress_q4(stress_q4Template):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.label_error.visible = False
    self.q4_next_btn.enabled = False

    # --- Load saved data, if it exists ---
    saved_value = assessment_logic.user_data.get('diet_quality_1_10')
    if saved_value is not None:
      # If data is saved, display it and enable the button
      self.stress_q4_ans.text = str(saved_value)
      self.q4_next_btn.enabled = True
    else:
      # Otherwise, start with an empty text box
      self.stress_q4_ans.text = "" 

  def live_validate(self):
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
      return

      # 2. VALIDATION PASSED: Now get the clean numeric result.
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
    self.live_validate()

  def stress_q4_ans_pressed_enter(self, **event_args):
    self.handle_input_and_advance()

  def q4_next_btn_click(self, **event_args):
    self.handle_input_and_advance()

  def q4_back_btn_click(self, **event_args):
    open_form("StressLevelPage.stress_q3")

  def home_btn_click(self, **event_args):
    open_form('MainPage')
    pass
