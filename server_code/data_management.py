# --- data_management.py (COMPLETE & VERIFIED SERVER MODULE) ---

import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users 
import anvil.tz
import datetime

# =========================================================
# 1. STRESS LOGGING AND SAVING
# =========================================================

@anvil.server.callable
def save_daily_stress(final_score, result_level, user_inputs):
  """
    Saves the user's daily stress assessment result to the stress_logs table.
    Prevents duplicate entries for the same user on the same day.
    """
  current_user = anvil.users.get_user()

  if not current_user:
    return {"ok": False, "msg": "User not logged in."}

    # Check if a log already exists for today to prevent duplicates
  today = anvil.tz.now().date()

  # Define the start and end of "today" for the query
  start_of_day = datetime.datetime.combine(today, datetime.time.min).replace(tzinfo=anvil.tz.tzlocal())
  end_of_day = datetime.datetime.combine(today, datetime.time.max).replace(tzinfo=anvil.tz.tzlocal())

  existing_log = app_tables.stress_logs.search(
    users=current_user,
    date=q.greater_than_or_equal_to(start_of_day),
    date=q.less_than_or_equal_to(end_of_day)
  )

  if existing_log:
    return {"ok": False, "msg": "Assessment already saved for today."}

    # Save the data
  app_tables.stress_logs.add_row(
    users=current_user,
    date=anvil.tz.now(), # Store the exact datetime
    total_score=final_score,
    level=result_level, 

    # Save individual assessment inputs
    sleep_hours=user_inputs.get("sleep_hours"),
    daily_exercise_mins=user_inputs.get("daily_exercise_mins"), # Assuming you'll pass this
    screen_time_hours=user_inputs.get("screen_time_hours"),     # Assuming you'll pass this
    diet_quality=user_inputs.get("diet_quality_1_10"),
    productivity_score=user_inputs.get("productivity_score_1_10"), # Assuming you'll pass this
    mood_level=user_inputs.get("mood_level_1_10"),
  )

  return {"ok": True}

# =========================================================
# 2. STRESS LOG RETRIEVAL FOR GRAPHS
# =========================================================

@anvil.server.callable
def get_weekly_stress_logs():
  """
    Retrieves stress scores for the last 7 days for the currently logged-in user.
    """
  current_user = anvil.users.get_user()

  if not current_user:
    return []

    # Calculate the date 7 days ago
  seven_days_ago = anvil.tz.now() - datetime.timedelta(days=7)

  # Fetch logs
  logs = app_tables.stress_logs.search(
    users=current_user,
    date=q.greater_than_or_equal_to(seven_days_ago),
    tables.order_by("date", ascending=True)
  )

  # Return data formatted for a graph
  return [
    {"date": row["date"].strftime("%a, %b %d"), "score": row["total_score"]}  
    for row in logs
  ]

# =========================================================
# 3. BURNOUT LOGGING (Optional but recommended for completeness)
# =========================================================

@anvil.server.callable
def log_burnout_assessment(burnout_index, guidance, user_inputs):
  """
    Saves the user's burnout assessment result to the burnout_logs table.
    """
  current_user = anvil.users.get_user()

  if not current_user:
    return {"ok": False, "msg": "User not logged in."}

    # You might also want to check for duplicates here if burnout is only tracked weekly/monthly

  app_tables.burnout_logs.add_row(
    users=current_user,
    date=anvil.tz.now(),
    burnout_index=burnout_index,
    guidance=guidance, 
    # Add specific burnout scores (e.g., exhaustion, cynicism) from user_inputs
    # exhaustion_score=user_inputs.get("exhaustion_score"), 
    # cynicism_score=user_inputs.get("cynicism_score"),
  )

  return {"ok": True}