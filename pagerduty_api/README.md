pip install fastapi uvicorn requests

uvicorn app:app --reload


curl -X POST "http://127.0.0.1:8000/create-maintenance-window/?usermail=user@example.com" \
-H "Content-Type: application/json" \
-d '{
  "service_ids": ["SERVICE_ID_1", "SERVICE_ID_2"],
  "duration_minutes": 30
}'
