from ._anvil_designer import student_burnout_q1Template
from anvil import *
from ... import assessment_logic

class student_burnout_q1(student_burnout_q1Template):

  def __init__(self, **properties):
    self.init_components(**properties)
    self.label_error.visible = False
    self.q1_next_btn.enabled = False

    # SAFE READ (prevents KeyError)
    val = assessment_logic.burnout_data.get("study_hours_per_day")
    self.stress_q1_ans.text = "" if val is None else str(val)

  def live_validate(self):
    ok, res = assessment_logic.validate_number(
      self.stress_q1_ans.text, 0, 12
    )

    if ok:
      self.label_error.visible = False
      self.q1_next_btn.enabled = True
      return True

    self.label_error.text = res
    self.label_error.visible = True
    self.q1_next_btn.enabled = False
    return False

  def stress_q1_ans_change(self, **event_args):
    self.live_validate()

  def q1_next_btn_click(self, **event_args):
    if not self.live_validate():
      return

    _, value = assessment_logic.validate_number(
      self.stress_q1_ans.text, 0, 12
    )

    assessment_logic.burnout_data["study_hours_per_day"] = value
    open_form("BurnoutLevelPage.student_burnout_q2")
