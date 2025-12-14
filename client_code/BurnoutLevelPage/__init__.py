from ._anvil_designer import BurnoutLevelPageTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

# Ensure this import matches your file structure
# If 'assessment_logic' is in a folder above, use 'from .. import assessment_logic'
# If it is in the same folder, use 'from . import assessment_logic'
from .. import assessment_logic 

class BurnoutLevelPage(BurnoutLevelPageTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.label_error.visible = False

    # --- Setup Radio Buttons ---
    group_name = 'current_situation' 
    self.radio_student.group_name = group_name
    self.radio_working.group_name = group_name
    self.radio_both.group_name = group_name
    self.radio_none.group_name = group_name

    # These are the VALUES we will check for later
    self.radio_student.value = 'student'
    self.radio_working.value = 'working'
    self.radio_both.value = 'both'
    self.radio_none.value = 'none'

  # --- EVENT HANDLERS (Must be aligned with __init__) ---

  def burnout_con_click(self, **event_args):
    """This handles the Continue button click"""

    # 1. Manual Loop to find selected value (Fixes 'selected_value' error)
    selection = None
    radio_buttons = [
      self.radio_student,
      self.radio_working,
      self.radio_both,
      self.radio_none
    ]

    for radio in radio_buttons:
      if radio.selected:
        selection = radio.value
        break 

    # 2. Validate Selection
    if selection is None:
      self.label_error.text = "Please select your current situation to continue."
      self.label_error.visible = True
      return

    self.label_error.visible = False

    # 3. Save to Global Logic
    assessment_logic.user_data['current_situation'] = selection

    # 4. Navigate (Must match values set in __init__)
    if selection == 'student':
      open_form("BurnoutLevelPage.student_burnout_q1")

    elif selection == 'working':
      open_form("BurnoutLevelPage.work_burnout_q1")

    elif selection == 'both':
      open_form("BurnoutLevelPage.student_burnout_q1") 

    elif selection == 'none':
      open_form("BurnoutLevelPage.personal_burnout_q1") 

  def home_btn_click(self, **event_args):
    """This handles the Home button click"""
    open_form("MainPage")

  def radio_selection_clicked(self, **event_args):
    """Shared handler to hide error when radio buttons are clicked"""
    self.label_error.visible = False

  # --- Placeholder handlers to satisfy Designer warnings ---
  def radio_student_clicked(self, **event_args):
    pass
  def radio_working_clicked(self, **event_args):
    pass
  def radio_both_clicked(self, **event_args):
    pass
  def radio_none_clicked(self, **event_args):
    pass