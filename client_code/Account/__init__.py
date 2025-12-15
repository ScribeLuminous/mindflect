# -- account page -- 
# -- show only once user is logged in successfully -- 

from ._anvil_designer import AccountTemplate
from anvil import *
import anvil.users
import plotly.graph_objects as go
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import random

class Account(AccountTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    # 1. Security Check
    if not anvil.users.get_user():
      open_form('Account.Login') 
      return

    # 2. Load Content
    self.load_history_graphs()
    self.load_dashboard_content()

  def load_dashboard_content(self):
    """Fetches user profile data and updates labels."""
    try:
      data = anvil.server.call('get_user_profile_data')
    except Exception as e:
      print(f"Server Error: {e}")
      return

    if not data: 
      return

    # --- 1. GREETING ---
    self.greet_lbl.text = f"Hello, {data['username']}!"

    # =================================================
    # STRESS SECTION
    # =================================================

    # Random Stress Encouragement
    stress_quotes = [
      "Believe you can and you're halfway there.",
      "One small positive thought can change your whole day.",
      "Don't be pushed around by the fears in your mind.",
      "Your mental health is a priority.",
      "Take a deep breath. You got this."
    ]
    self.encouragement_lbl.text = f"✨ {random.choice(stress_quotes)}"

    # Stress Recommendations
    s_level = data.get('latest_stress_level') 
    s_text = ""

    if s_level and "Low" in s_level:
      s_text = "• Try to read a book\n• Take a short walk\n• Spend time with a pet\n• Listen to calming music"
      self.stress_recs.foreground = "#4CAF50"
    elif s_level and "Moderate" in s_level:
      s_text = "• Write down your thoughts in a diary\n• Get a change of scenery\n• Take a walk, yoga or dance"
      self.stress_recs.foreground = "#FF9800"
    elif s_level and "High" in s_level:
      s_text = "• Consider talking with a professional\n• Practice intense physical activity\n• Reach out to a trusted friend"
      self.stress_recs.foreground = "#F44336"
    else:
      s_text = "No stress data yet."
      self.stress_recs.foreground = "gray"

    self.stress_recs.text = s_text

    # =================================================
    # BURNOUT SECTION
    # =================================================

    # Random Burnout Encouragement
    burnout_quotes = [
      "Rest is not idleness, it is the key to better work.",
      "You can't pour from an empty cup.",
      "It's okay to take a break. The world will wait.",
      "Burnout is nature's way of telling you, you've been going through the motions.",
      "Self-care is how you take your power back."
    ]
    self.burn_encouragement_lbl.text = f"🌿 {random.choice(burnout_quotes)}"

    # Burnout Recommendations
    b_level = data.get('latest_burnout_level')
    b_text = ""

    # FIX: Check "if b_level" first
    if b_level and "Low" in b_level:
      b_text = (
        "• Prioritize your self-care.\n"
        "• Set small boundaries at your responsibilities.\n"
        "• Take short breaks.\n"
        "• Learn to say 'no' to non-essential tasks."
      )
      self.burnout_recs.foreground = "#4CAF50" # Green

    elif b_level and "Moderate" in b_level:
      b_text = (
        "• Schedule downtime and stick to it.\n"
        "• Delegate tasks or ask for help.\n"
        "• Do meditation.\n"
        "• Limit social media use."
      )
      self.burnout_recs.foreground = "#FF9800" # Orange

    elif b_level and "High" in b_level:
      b_text = (
        "• Seek support from a professional.\n"
        "• Focus on rest and recovery.\n"
        "• Take a break from work or responsibilities."
      )
      self.burnout_recs.foreground = "#F44336" # Red

    else:
      b_text = "No burnout data yet."
      self.burnout_recs.foreground = "gray"

    self.burnout_recs.text = b_text


  # --- GRAPH LOGIC ---
  def load_history_graphs(self):
    try:
      stress_data, burnout_data = anvil.server.call('get_user_history')
    except Exception:
      return 

    # Stress Plot
    if stress_data:
      dates = [x['date'] for x in stress_data]
      scores = [x['score'] for x in stress_data]
      self.stress_plot.data = [go.Scatter(x=dates, y=scores, mode='lines+markers', name='Stress', line=dict(color='#4CAF50', width=3))]
      self.stress_plot.layout = go.Layout(title="Weekly Stress Tracker", yaxis=dict(range=[0, 100]), margin=dict(t=40, b=40, l=40, r=40))
    else:
      self.stress_plot.layout = go.Layout(title="No Stress Data Yet")

    # Burnout Plot
    if burnout_data:
      dates = [x['date'] for x in burnout_data]
      scores = [x['score'] for x in burnout_data]
      self.burnout_plot.data = [go.Scatter(x=dates, y=scores, mode='lines+markers', name='Burnout', line=dict(color='#FF5722', width=3))]
      self.burnout_plot.layout = go.Layout(title="Burnout Risk Over Time", yaxis=dict(range=[0, 100]), margin=dict(t=40, b=40, l=40, r=40))
    else:
      self.burnout_plot.layout = go.Layout(title="No Burnout Data Yet")

  # --- HANDLERS ---
  def reflect_btn_click(self, **event_args):
    open_form("MainPage.levelselect")

  def logout_btn_click(self, **event_args):
    anvil.users.logout()
    open_form("MainPage")

  def stress_plot_click(self, points, **event_args): pass
  def burnout_plot_click(self, points, **event_args): pass