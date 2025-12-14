# --- data_management.py (FINAL CORRECTED SERVER CODE) ---

import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users # CRITICAL: Import must be correct and at top-level
import anvil.tz

# Function to save the stress log (including the ML result)
@anvil.server.callable
def log_stress_assessment(assessment_data, prediction_result):
  # Retrieve user object using the function from anvil.users
  current_user = anvil.users.get_user()

  if not current_user:
    # If the user is not logged in, you might save data differently or raise an error
    raise Exception("Must be logged in to save data.")

    # Combine assessment inputs and prediction result
  app_tables.stress_logs.add_row(
    users=current_user,
    date=anvil.tz.now(),
    # Ensure 'total_score' is being calculated and passed from the client
    total_score=assessment_data.get('total_score', 0), 

    # Mapping inputs from assessment_data to your database columns
    sleep_hours=assessment_data.get('sleep_hours'),
    diet_quality=assessment_data.get('diet_quality_1_10'),

    # Mapping results
    predicted_level=prediction_result['level'],
    # You will likely need to pass and save the guidance text here too
    # guidance=prediction_result['guidance'] 
  )

# Function to retrieve data for the weekly graph
@anvil.server.callable
def get_weekly_stress_logs():
  current_user = anvil.users.get_user()

  if not current_user:
    return []

    # Example query to fetch logs for the last 7 days
  seven_days_ago = anvil.tz.now() - anvil.server.time_delta(days=7)

  logs = app_tables.stress_logs.search(
    users=current_user,
    date=q.greater_than(seven_days_ago),
    tables.order_by("date", ascending=True)
  )

  # Return data formatted for a graph (e.g., list of dictionaries)
  return [
    {"date": row["date"].strftime("%b %d"), "score": row["total_score"]}  
    for row in logs
  ]