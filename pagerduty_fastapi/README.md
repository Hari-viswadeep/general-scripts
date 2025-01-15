POST /create-maintenance-window: Accepts service IDs and duration (max 30 minutes) to create a maintenance window.
DELETE /delete-maintenance-window: Deletes a maintenance window using its ID.


Both endpoints require a user_email query parameter to ensure that user context is provided.

The duration for maintenance windows is capped at 30 minutes.

Create Maintenance Window:

curl -X POST "http://127.0.0.1:8000/create-maintenance-window?user_email=user@example.com" \
-H "Content-Type: application/json" \
-d '{"service_ids": ["SERVICE_ID_1", "SERVICE_ID_2"], "duration_minutes": 30}'

Delete Maintenance Window:
curl -X DELETE "http://127.0.0.1:8000/delete-maintenance-window?user_email=user@example.com" \
-H "Content-Type: application/json" \
-d '{"maintenance_window_id": "YOUR_MAINTENANCE_WINDOW_ID"}'


