# --- BurnoutLevelPage.py (FINAL – ANVIL CORRECT) ---

from ._anvil_designer import BurnoutLevelPageTemplate
from anvil import *
import anvil.server

from .. import assessment_logic


class BurnoutLevelPage(BurnoutLevelPageTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.label_error.visible = False

    # --- Group the radio buttons ---
    group_name = "current_situation"

    self.radio_student.group_name = group_name
    self.radio_working.group_name = group_name
    self.radio_both.group_name = group_name
    self.radio_none.group_name = group_name

    # Store semantic values
    self.radio_student.value = "student"
    self.radio_working.value = "working"
    self.radio_both.value = "both"
    self.radio_none.value = "none"


  def burnout_con_click(self, **event_args):
    """
    Handle Continue button click
    """

    selection = None

    # ✅ CORRECT: use `.selected`
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

    # --- Validation ---
    if selection is None:
      self.label_error.text = "Please select your current situation to continue."
      self.label_error.visible = True
      return

    self.label_error.visible = False

    # Save selection globally
    assessment_logic.user_data["current_situation"] = selection

    # --- Routing logic ---
    if selection == "student":
      open_form("BurnoutLevelPage.student_burnout_q1")

    elif selection == "working":
      open_form("BurnoutLevelPage.work_burnout_q1")

    elif selection == "both":
      # Start with student; later you’ll chain work → personal
      open_form("BurnoutLevelPage.student_burnout_q1")

    elif selection == "none":
      open_form("BurnoutLevelPage.personal_burnout_q1")


  def radio_selection_clicked(self, **event_args):
    """
    Attach this handler to ALL radio buttons
    """
    self.label_error.visible = False


  def home_btn_click(self, **event_args):
    open_form("MainPage")
