# --- student_burnout_q6.py ---

from ._anvil_designer import student_burnout_q6Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from .. import assessment_logic 


class student_burnout_q6(student_burnout_q6Template):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.label_error.visible = False

    # --- Radio Button Setup ---
    group_name = 'extracurricular'
    self.q6_yes.group_name = group_name
    self.q6_no.group_name = group_name

    # Assign values for storage
    self.q6_yes.value = 'yes'
    self.q6_no.value = 'no'

    # Load saved data
    saved_selection = assessment_logic.burnout_data.get("extracurricular_participation")
    if saved_selection == 'yes':
      self.q6_yes.selected = True
    elif saved_selection == 'no':
      self.q6_no.selected = True

  def get_selected_value(self):
    """Helper to find the value of the selected radio button."""
    if self.q6_yes.selected:
      return self.q6_yes.value
    if self.q6_no.selected:
      return self.q6_no.value
    return None

  def handle_input_and_advance(self):
    selection = self.get_selected_value()

    if selection is None:
      # Validation failed: No selection made
      self.label_error.text = "Please select an option to continue."
      self.label_error.visible = True
      return

      # Validation passed
    self.label_error.visible = False

    # 1. Save the selection
    assessment_logic.burnout_data["extracurricular_participation"] = selection

    # 2. Student assessment is COMPLETE. Advance to personal burnout questions.
    open_form("BurnoutLevelPage.personal_burnout_q1") 

    # --- Event Handlers ---

  def q6_next_btn_click(self, **event_args):
    self.handle_input_and_advance()

  def radio_selection_clicked(self, **event_args):
    """Shared handler for both radio buttons to clear the error message."""
    self.label_error.visible = False

  def q6_yes_clicked(self, **event_args):
    self.radio_selection_clicked()

  def q6_no_clicked(self, **event_args):
    self.radio_selection_clicked()

  def q6_back_btn_click(self, **event_args):
    """Go back to the previous question (Q5)"""
    open_form("BurnoutLevelPage.student_burnout_q5") 

  def home_btn_click(self, **event_args):
    open_form("MainPage")