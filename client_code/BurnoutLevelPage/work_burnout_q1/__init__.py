# --- work_burnout_q1.py ---

from ._anvil_designer import work_burnout_q1Template
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from .. import assessment_logic

class work_burnout_q1(work_burnout_q1Template):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.label_error.visible = False

    # 1. Disable Next button by default
    self.q1_next_btn.enabled = False 

    # 2. Load Saved Data
    saved = assessment_logic.burnout_data.get("work_life_balance")
    if saved is not None:
      self.work_burnout_q1_ans.text = str(saved)

    # 3. Trigger validation immediately (in case data was loaded)
    self.live_validate()

  def live_validate(self):
    """
    Validates input instantly (0-10, integer required).
    Toggles the error label and the Next button.
    """
    input_str = self.work_burnout_q1_ans.text

    # Validation: MIN 0, MAX 10 (Integer Required)
    valid, result = assessment_logic.validate_input(input_str, 0, 10, require_integer=True)

    if valid:
      self.label_error.visible = False
      self.q1_next_btn.enabled = True
      return True

    # Invalid
    self.label_error.text = result
    self.label_error.visible = True
    self.q1_next_btn.enabled = False
    return False

  def handle_input_and_advance(self):
    """Saves data and moves to the next page only if valid."""
    if self.live_validate():
      # Get the clean integer value
      _, result = assessment_logic.validate_input(
        self.work_burnout_q1_ans.text, 0, 10, require_integer=True
      )

      # Save to global logic
      assessment_logic.burnout_data["work_life_balance"] = result

      # Move to Q2
      open_form("BurnoutLevelPage.work_burnout_q2")

  # --- Event Handlers ---

  def q1_next_btn_click(self, **event_args):
    self.handle_input_and_advance()

  def work_burnout_q1_ans_pressed_enter(self, **event_args):
    self.handle_input_and_advance()

  def work_burnout_q1_ans_change(self, **event_args):
    """Called when text changes: runs live validation"""
    self.live_validate()

  def q1_back_btn_click(self, **event_args):
    """
    Logic: 
    - If user is 'Student + Working' (Both), they came from Student Q6.
    - If user is just 'Working', they came from the Start Page.
    """
    user_type = assessment_logic.user_data.get('current_situation')

    if user_type == 'both':
      open_form("BurnoutLevelPage.student_burnout_q6") 
    else:
      open_form("BurnoutLevelPage") # Back to start

  def home_btn_click(self, **event_args):
    open_form("MainPage")