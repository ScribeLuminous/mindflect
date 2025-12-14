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
    self.q6_next_btn.enabled = False 

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
      self.q6_next_btn.enabled = True
      return True

      # Validation failed.
    self.label_error.text = result
    self.label_error.visible = True
    self.q6_next_btn.enabled = False
    return False

  def submit_burnout_assessment(self):
    """
        PLACEHOLDER: This function should be defined in assessment_logic.py.
        It calculates the total burnout score and saves it to a final key.
        """
    assessment_logic.submit_assessment()


  def handle_input_and_advance(self):
    if self.live_validate():
      # 1. Save the final input value
      _, result = assessment_logic.validate_input(
        self.personal_burnout_q6_ans.text, 0, 10, require_integer=True
      )
      assessment_logic.burnout_data["time_for_passion"] = result

      # 2. Determine next step based on user type
      user_type = assessment_logic.burnout_data.get("user_type")

      if user_type == "both":
        # User still needs to complete the Work section
        open_form("BurnoutLevelPage.work_burnout_q1")
      else:
        # Assessment is complete (Student only). SUBMIT, then go to results.
        self.submit_burnout_assessment()
        open_form("BurnoutResultPage") 


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