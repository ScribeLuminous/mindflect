# --- personal_burnout_q6.py ---

from ._anvil_designer import personal_burnout_q6Template
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

# Note: Ensure this import path matches your project structure
from .. import assessment_logic 

class personal_burnout_q6(personal_burnout_q6Template):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.label_error.visible = False

    # Disable next/submit button by default until valid input
    # (Assuming you have a button named q6_submit_btn or q6_next_btn)
    if hasattr(self, 'q6_submit_btn'):
      self.q6_submit_btn.enabled = False

      # Load saved data if it exists
    saved_time = assessment_logic.burnout_data.get("time_for_passion")
    if saved_time is not None:
      self.personal_burnout_q6_ans.text = str(saved_time)

    self.live_validate()

  def live_validate(self):
    """Validates input instantly (0-10, integer required)."""
    input_str = self.personal_burnout_q6_ans.text

    # Validation: MIN 0, MAX 10 (REQUIRES INTEGER)
    valid, result = assessment_logic.validate_input(input_str, 0, 10, require_integer=True)

    if valid:
      self.label_error.visible = False
      # Enable buttons if they exist
      if hasattr(self, 'q6_submit_btn'):
        self.q6_submit_btn.enabled = True
      return True

      # Validation failed.
    self.label_error.text = result
    self.label_error.visible = True
    if hasattr(self, 'q6_submit_btn'):
      self.q6_submit_btn.enabled = False
    return False

  def submit_burnout_assessment(self):
    """Calculates and returns the final score and result dict."""
    # FIXED: Added 'return' so the data gets back to the handler
    return assessment_logic.submit_assessment()

    # FIXED: Moved inside class and corrected logic
  def handle_input_and_advance(self):
    if self.live_validate():
      # 1. Save the final input value
      _, result = assessment_logic.validate_input(
        self.personal_burnout_q6_ans.text, 0, 10, require_integer=True
      )
      assessment_logic.burnout_data["time_for_passion"] = result

      # 2. Check User Role (student vs worker vs both)
      # Note: Using 'burnout_role' as defined in your assessment_logic.py
      role = assessment_logic.burnout_data.get("burnout_role")

      if role == "both":
        # If doing both, move to Work track now
        open_form("BurnoutLevelPage.work_burnout_q1")
      else:
        # 3. ASSESSMENT COMPLETE

        # FIXED: Correct unpacking order. 
        # Logic returns (dict, int) -> We capture as (burnout_result, final_score)
        burnout_result, final_score = self.submit_burnout_assessment()

        # 4. OPEN RESULTS PAGE
        open_form(
          "BurnoutResultPage", 
          result=burnout_result, 
          score=final_score
        )

    # --- Event Handlers ---

  def q6_submit_btn_click(self, **event_args):
    self.handle_input_and_advance()

  def personal_burnout_q6_ans_pressed_enter(self, **event_args):
    self.handle_input_and_advance()

  def personal_burnout_q6_ans_change(self, **event_args):
    self.live_validate()

  def q6_back_btn_click(self, **event_args):
    open_form("BurnoutLevelPage.personal_burnout_q5") 

  def home_btn_click(self, **event_args):
    open_form("MainPage")