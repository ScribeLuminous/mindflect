# --- BurnoutLevelPage.py (FIXED for Radio Button Group Logic) ---

from ._anvil_designer import BurnoutLevelPageTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

# Assume this logic module exists to save data
# from ... import assessment_logic 

class BurnoutLevelPage(BurnoutLevelPageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.label_error.visible = False

    # --- Crucial Setup for Radio Buttons ---
    # 1. Set the same group_name for all radio buttons in the group
    # NOTE: This MUST match the group_name you set in the Design View.
    group_name = 'current_situation' 
    self.radio_student.group_name = group_name
    self.radio_working.group_name = group_name
    self.radio_both.group_name = group_name
    self.radio_none.group_name = group_name

    # 2. Set the unique value for each button
    # NOTE: This MUST be set in the Design View OR here, as these are the values saved.
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

    # 1. Save the data (Uncomment and ensure assessment_logic is imported)
    # assessment_logic.user_data['current_situation'] = selection

    # 2. Advance to the next form
    open_form("BurnoutLevelPage.burnout_q1")

  def radio_working_clicked(self, **event_args):
    """This method is called when any radio button is selected"""
    # We can use this to hide the error message immediately after a selection is made
    self.label_error.visible = False

  def home_btn_click(self, **event_args):
    open_form("MainPage")
    pass

  def radio_student_clicked(self, **event_args):
    """This method is called when this radio button is selected"""
    pass
