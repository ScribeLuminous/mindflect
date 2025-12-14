# --- BurnoutLevelPage.py (FINAL CORRECTED CODE) ---

from ._anvil_designer import BurnoutLevelPageTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

# Assume this logic module exists to save data
# If you don't have this, you need to save the selection somewhere global.
from ... import assessment_logic 

class BurnoutLevelPage(BurnoutLevelPageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.label_error.visible = False

    # --- Crucial Setup for Radio Buttons ---
    # NOTE: Using 'assessment_logic' to store the selection

    group_name = 'current_situation' 
    self.radio_student.group_name = group_name
    self.radio_working.group_name = group_name
    self.radio_both.group_name = group_name
    self.radio_none.group_name = group_name

    self.radio_student.value = 'student'
    self.radio_working.value = 'working'
    self.radio_both.value = 'both'
    self.radio_none.value = 'none'

  def burnout_con_click(self, **event_args):
    # Check the selected value using ANY radio button in the group.
    selection = self.radio_student.selected_value

    if selection is None:
      # Validation failed: No selection made
      self.label_error.text = "Please select your current situation to continue."
      self.label_error.visible = True
      return

      # Validation passed
    self.label_error.visible = False

    # 1. Save the selection to your global logic module
    # Note: You need to define 'current_situation' in your assessment_logic.user_data
    assessment_logic.user_data['current_situation'] = selection

    # 2. Advance to the next form based on the selection
    if selection == 'student':
      # Starts Student questions, then personal questions
      open_form("BurnoutLevelPage.student_burnout_q1")

    elif selection == 'working':
      # Starts Working questions, then personal questions
      open_form("BurnoutLevelPage.work_burnout_q1")

    elif selection == 'both':
      # Starts Student questions (and must proceed to Working questions later), then personal questions
      open_form("BurnoutLevelPage.student_burnout_q1") 

    elif selection == 'none':
      # Skips job/school questions, goes straight to personal questions
      open_form("BurnoutLevelPage.personal_burnout_q1") 

  def radio_selection_clicked(self, **event_args):
    """This method is called when any radio button is selected.
           We connect ALL radio buttons (student, working, both, none) to this single handler 
           in the Design View."""

    # Hide the error message immediately after a selection is made
    self.label_error.visible = False

  def home_btn_click(self, **event_args):
    open_form("MainPage")
    pass