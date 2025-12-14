# --- personal_burnout_q6.py ---

from ._anvil_designer import personal_burnout_q6Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from .. import assessment_logic 


class personal_burnout_q6(personal_burnout_q6Template):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.label_error.visible = False

    # KEY: time_for_passion (Scale 0-10, integer)
    saved_time = assessment_logic.burnout_data.get("time_for_passion")

    if saved_time is not None:
      self.personal_burnout_q6_ans.text = str(saved_time)

    self.live_validate()

  def live_validate(self):
    """
        Validates input instantly (0-10, integer required) for time dedicated to passion/hobbies rating.
        """
    input_str = self.personal_burnout_q6_ans.text

    # Validation: MIN 0, MAX 10 (REQUIRES INTEGER for a rating scale)
    valid, result = assessment_logic.validate_input(input_str, 0, 10, require_integer=True)

    if valid:
      self.label_error.visible = False
      return True

      # Validation failed.
    self.label_error.text = result
    self.label_error.visible = True
    return False

  def submit_burnout_assessment(self):
    """Calculates and saves the final score, returning score and result dict."""
    # This calls the function defined in assessment_logic.py
    assessment_logic.submit_assessment()

def handle_input_and_advance(self):
  if self.live_validate():
    # 1. Save the final input value
    _, result = assessment_logic.validate_input(
      self.personal_burnout_q6_ans.text, 0, 10, require_integer=True
    )
    assessment_logic.burnout_data["time_for_passion"] = result

    user_type = assessment_logic.burnout_data.get("user_type")

    if user_type == "both":
      open_form("BurnoutLevelPage.work_burnout_q1")
    else:
      # 2. ASSESSMENT COMPLETE: Calculate and retrieve the score/result
      final_score, burnout_result = self.submit_burnout_assessment()

      # 3. OPEN RESULTS PAGE and pass the data
      open_form(
        "BurnoutResultPage", 
        result=burnout_result, 
        score=final_score
      )

  
    # --- Event Handlers ---

  def q6_next_btn_click(self, **event_args):
    self.handle_input_and_advance()

  def personal_burnout_q6_ans_pressed_enter(self, **event_args):
    self.handle_input_and_advance()

  def personal_burnout_q6_ans_change(self, **event_args):
    """Called when the text in the text box is edited (live validation)"""
    self.live_validate()

  def q6_back_btn_click(self, **event_args):
    """Go back to the previous question (Personal Q5)"""
    open_form("BurnoutLevelPage.personal_burnout_q5") 

  def home_btn_click(self, **event_args):
    open_form("MainPage")

  def q6_submit_btn_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass
