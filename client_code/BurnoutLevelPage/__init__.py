# --- BurnoutLevelPage.py (FINAL FIX for selected_value Error) ---

from ._anvil_designer import BurnoutLevelPageTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

# Assuming this path is correct for your structure
from .. import assessment_logic 

class BurnoutLevelPage(BurnoutLevelPageTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.label_error.visible = False

    # --- Crucial Setup for Radio Buttons ---
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

    # -----------------------------------------------------------------
    # FIX: Bypass the unreliable 'selected_value' property.
    # Check the 'checked' state of each radio button in the group.
    # -----------------------------------------------------------------
    selection = None

    radio_buttons = [
      self.radio_student,
      self.radio_working,
      self.radio_both,
      self.radio_none
    ]

    for radio in radio_buttons:
      # Check if this specific radio button is checked
      if radio.checked: 
        selection = radio.value
        break # Found the selection, stop the loop

    if selection is None:
      # Validation failed: No selection made
      self.label_error.text = "Please select your current situation to continue."
      self.label_error.visible = True
      return

      # Validation passed
    self.label_error.visible = False

    # 1. Save the selection
    assessment_logic.user_data['current_situation'] = selection

    # 2. Advance to the next form based on the selection
    if selection == 'student':
      open_form("BurnoutLevelPage.student_burnout_q1")
    elif selection == 'working':
      open_form("BurnoutLevelPage.work_burnout_q1")
    elif selection == 'both':
      open_form("BurnoutLevelPage.student_burnout_q1") 
    elif selection == 'none':
      open_form("BurnoutLevelPage.personal_burnout_q1") 

  def radio_selection_clicked(self, **event_args):
    """
        The shared handler for all radio buttons in the group.
        (Requires connecting all radio buttons to this method in the Designer).
        """
    self.label_error.visible = False

  def home_btn_click(self, **event_args):
    open_form("MainPage")
    pass