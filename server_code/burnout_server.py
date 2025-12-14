# --- burnout_server.py (Server Module) ---

import anvil.server
import anvil.users
from anvil.tables import app_tables
import datetime

@anvil.server.callable
def save_daily_burnout(
  burnout_score,
  burnout_level,
  burnout_type,   # "personal", "study", "work", or "combined"
  inputs
):
  """
    Saves one burnout entry per user per day per burnout type
    """

  user = anvil.users.get_user()
  if not user:
    return {"ok": False, "msg": "User not logged in"}

  today = datetime.date.today()

  # Prevent duplicate saves for same day + type
  existing = app_tables.burnout_logs.search(
    user=user,
    date=today,
    burnout_type=burnout_type
  )

  if len(existing) > 0:
    return {"ok": False, "msg": "Burnout already saved today"}

  app_tables.burnout_logs.add_row(
    user=user,
    date=today,
    burnout_type=burnout_type,
    burnout_score=burnout_score,
    burnout_level=burnout_level,
    inputs=inputs
  )

  return {"ok": True}
