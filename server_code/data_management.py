# --- data_management.py (Server Module) ---

import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users 
import anvil.tz

# ... (Existing log_stress_assessment and get_weekly_stress_logs functions) ...

# -----------------------------
# NEW FUNCTION FOR SAVING RESULTS (Required by StressResultPage)
# -----------------------------
@anvil.server.callable
def save_daily_stress(final_score, result_level, user_inputs):
  current_user = anvil.users.get_user()

  if not current_user:
    return {"ok": False, "msg": "User not logged in."}

    # Check if a log already exists for today to prevent duplicates
  today = anvil.tz.now().date()
  existing_log = app_tables.stress_logs.search(
    users=current_user,
    date=tables.query.less_than(today + anvil.server.time_delta(days=1)),
    date=tables.query.greater_than_or_equal_to(today)
  )

  if existing_log:
    return {"ok": False, "msg": "Already saved today."}

    # Save the data
  app_tables.stress_logs.add_row(
    users=current_user,
    date=anvil.tz.now(),
    total_score=final_score,
    level=result_level, # Save the level string

    # Save individual assessment inputs from the user_inputs dictionary
    sleep_hours=user_inputs.get("sleep_hours"),
    diet_quality=user_inputs.get("diet_quality_1_10"),
    mood_level=user_inputs.get("mood_level_1_10"),
    # Add other fields here...
  )

  return {"ok": True}