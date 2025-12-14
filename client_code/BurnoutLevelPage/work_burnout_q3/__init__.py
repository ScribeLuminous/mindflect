# --- work_burnout_q3.py ---

from ._anvil_designer import work_burnout_q3Template
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

# Adjust import based on your folder structure
from .. import assessment_logic 

class work_burnout_q3(work_burnout_q3Template):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.label_error.visible = False

    # 1. Disable Next button by default
    self.q3_next_btn.enabled = False 

    # 2. Load Saved Data (Key: 'lost_vacation')
    saved = assessment_logic.burnout_data.get("lost_vacation")
    if saved is not None:
      self.work_burnout_q3_ans.text = str(saved)

    # 3. Trigger validation immediately
    self.live_validate()

  def live_validate(self):
    """
    Validates input instantly (0-60+, integer required).
    """
    input_str = self.work_burnout_q3_ans.text

    # Validation: MIN 0, MAX 365 (Integer Required - days per year)
    # Note: Your logic divides by 60, so 60 is the 'max impact' threshold, 
    # but a user could theoretically lose more days.
    valid, result = assessment_logic.validate_input(input_str, 0, 365, require_integer=True)

    if valid:
      self.label_error.visible = False
      self.q3_next_btn.enabled = True
      return True

    # Invalid
    self.label_error.text = result
    self.label_error.visible = True
    self.q3_next_btn.enabled = False
    return False

  def handle_input_and_advance(self):
    """Saves data and moves to Q4."""
    if self.live_validate():
      # Get the clean integer value
      _, result = assessment_logic.validate_input(
        self.work_burnout_q3_ans.text, 0, 365, require_integer=True
      )

      # Save to global logic (Key: 'lost_vacation')
      assessment_logic.burnout_data["lost_vacation"] = result

      # Move to Q4 (Sufficient Income)
      open_form("BurnoutLevelPage.work_burnout_q4")

  # --- Event Handlers ---

  def q3_next_btn_click(self, **event_args):
    self.handle_input_and_advance()

  def work_burnout_q3_ans_pressed_enter(self, **event_args):
    self.handle_input_and_advance()

  def work_burnout_q3_ans_change(self, **event_args):
    """Called when text changes: runs live validation"""
    self.live_validate()

  def q3_back_btn_click(self, **event_args):
    """Go back to Work Q2"""
    open_form("BurnoutLevelPage.work_burnout_q2") 

  def home_btn_click(self, **event_args):
    open_form("MainPage")