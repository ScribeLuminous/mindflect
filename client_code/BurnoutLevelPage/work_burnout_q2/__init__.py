# --- work_burnout_q2.py ---

# --- work_burnout_q2.py (How stressful is your work day?) ---

from ._anvil_designer import work_burnout_q2Template
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

# Adjust import based on your folder structure
from .. import assessment_logic 

class work_burnout_q2(work_burnout_q2Template):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.label_error.visible = False

    # 1. Disable Next button by default
    self.q2_next_btn.enabled = False 

    # 2. Load Saved Data (Key: 'work_stress')
    saved = assessment_logic.burnout_data.get("work_stress")
    if saved is not None:
      self.work_burnout_q2_ans.text = str(saved)

    # 3. Trigger validation immediately
    self.live_validate()

  def live_validate(self):
    """
    Validates input instantly (0-10, integer required).
    """
    input_str = self.work_burnout_q2_ans.text

    # Validation: MIN 0, MAX 10 (Integer Required)
    valid, result = assessment_logic.validate_input(input_str, 0, 10, require_integer=True)

    if valid:
      self.label_error.visible = False
      self.q2_next_btn.enabled = True
      return True

    # Invalid
    self.label_error.text = result
    self.label_error.visible = True
    self.q2_next_btn.enabled = False
    return False

  def handle_input_and_advance(self):
    """Saves data and moves to Q3."""
    if self.live_validate():
      # Get the clean integer value
      _, result = assessment_logic.validate_input(
        self.work_burnout_q2_ans.text, 0, 10, require_integer=True
      )

      # Save to global logic (Key: 'work_stress')
      assessment_logic.burnout_data["work_stress"] = result

      # Move to Q3 (Lost Vacation)
      open_form("BurnoutLevelPage.work_burnout_q3")

  # --- Event Handlers ---

  def q2_next_btn_click(self, **event_args):
    self.handle_input_and_advance()

  def work_burnout_q2_ans_pressed_enter(self, **event_args):
    self.handle_input_and_advance()

  def work_burnout_q2_ans_change(self, **event_args):
    """Called when text changes: runs live validation"""
    self.live_validate()

  def q2_back_btn_click(self, **event_args):
    """Go back to Work Q1"""
    open_form("BurnoutLevelPage.work_burnout_q1") 

  def home_btn_click(self, **event_args):
    open_form("MainPage")