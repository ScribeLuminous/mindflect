# --- stress_server (Server Module) ---

import anvil.server
import anvil.users
from anvil.tables import app_tables
import datetime

@anvil.server.callable
def save_daily_stress(score, level, inputs):
  user = anvil.users.get_user()
  if not user:
    return False

  app_tables.stress_logs.add_row(
    user=user,
    date=datetime.date.today(),
    stress_score=score,
    stress_level=level,
    inputs=inputs
  )
  return True
