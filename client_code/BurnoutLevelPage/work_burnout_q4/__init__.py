# --- work_burnout_q4.py (FIXED) ---

from ._anvil_designer import work_burnout_q4Template
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

# Adjust import based on your folder structure
from .. import assessment_logic 

class work_burnout_q4(work_burnout_q4Template):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.label_error.visible = False

    # 1. Disable Next button by default
    self.q4_next_btn.enabled = False 

    # 2. Load Saved Data for THIS question (Sufficient Income)
    # Note: Accessing burnout_data, not user_data
    saved = assessment_logic.burnout_data.get("sufficient_income")

    if saved is not None:
      self.work_burnout_q4_ans.text = str(saved)

    # 3. Trigger validation immediately
    self.live_validate()

  def live_validate(self):
    """
    Validates input instantly (0-10, integer required).
    """
    input_str = self.work_burnout_q4_ans.text

    # Validation: MIN 0, MAX 10 (Standard rating scale)
    valid, result = assessment_logic.validate_input(input_str, 0, 10, require_integer=True)

    if valid:
      self.label_error.visible = False
      self.q4_next_btn.enabled = True
      return True

    # Invalid
    self.label_error.text = result
    self.label_error.visible = True
    self.q4_next_btn.enabled = False
    return False

  def handle_input_and_advance(self):
    """Saves data and transitions to the Personal section."""
    if self.live_validate():
      # Get the clean integer value
      _, result = assessment_logic.validate_input(
        self.work_burnout_q4_ans.text, 0, 10, require_integer=True
      )

      # 1. Save to global logic (Key: 'sufficient_income')
      assessment_logic.burnout_data["sufficient_income"] = result

      # 2. TRANSITION: Work Section Complete -> Start Personal Section
      open_form("BurnoutLevelPage.personal_burnout_q1")

  # --- Event Handlers ---

  def q4_next_btn_click(self, **event_args):
    self.handle_input_and_advance()

  def work_burnout_q4_ans_pressed_enter(self, **event_args):
    self.handle_input_and_advance()

  def work_burnout_q4_ans_change(self, **event_args):
    """Called when text changes: runs live validation"""
    self.live_validate()

  def q4_back_btn_click(self, **event_args):
    """Go back to Work Q3"""
    open_form("BurnoutLevelPage.work_burnout_q3") 

  def home_btn_click(self, **event_args):
    open_form("MainPage")