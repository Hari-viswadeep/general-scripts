from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, EmailStr, Field
import requests
import datetime

# Configuration
PAGERDUTY_API_TOKEN = "YOUR_API_TOKEN"  # Replace with your PagerDuty API token
PAGERDUTY_API_BASE_URL = "https://api.pagerduty.com"  # API base URL
MAINTENANCE_WINDOW_DESCRIPTION = "Scheduled maintenance window"
MAX_DURATION_MINUTES = 30  # Maximum allowed duration

app = FastAPI()

class MaintenanceWindowRequest(BaseModel):
    service_ids: list[str]  # List of service IDs
    duration_minutes: int = Field(
        ...,
        gt=0,
        le=MAX_DURATION_MINUTES,
        description=f"Duration of the maintenance window in minutes (maximum {MAX_DURATION_MINUTES} minutes)."
    )

def create_maintenance_window(service_ids, start_time, end_time):
    """
    Calls the PagerDuty API to create a maintenance window for the given services.
    """
    url = f"{PAGERDUTY_API_BASE_URL}/maintenance_windows"
    headers = {
        "Authorization": f"Token token={PAGERDUTY_API_TOKEN}",
        "Content-Type": "application/json",
        "Accept": "application/vnd.pagerduty+json;version=2"
    }
    payload = {
        "maintenance_window": {
            "type": "maintenance_window",
            "start_time": start_time,
            "end_time": end_time,
            "description": MAINTENANCE_WINDOW_DESCRIPTION,
            "services": [{"id": service_id, "type": "service_reference"} for service_id in service_ids]
        }
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 201:
        return {"status": "success", "data": response.json()}
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Failed to create maintenance window: {response.text}"
        )

@app.post("/create-maintenance-window/")
async def create_maintenance_window_endpoint(
    usermail: EmailStr = Query(..., description="The email ID of the user making the request."),
    request: MaintenanceWindowRequest = None
):
    """
    API endpoint to create a maintenance window.
    - `usermail`: The email of the user making the request (mandatory).
    - `request`: Request body containing service IDs and duration.
    """
    if not request or not request.service_ids:
        raise HTTPException(status_code=400, detail="Service IDs are required.")

    # Calculate start and end times
    now = datetime.datetime.utcnow()
    start_time = now.isoformat() + "Z"
    end_time = (now + datetime.timedelta(minutes=request.duration_minutes)).isoformat() + "Z"

    # Call the function to create the maintenance window
    result = create_maintenance_window(request.service_ids, start_time, end_time)
    return {
        "message": "Maintenance window created successfully.",
        "requested_by": usermail,
        "details": result
    }

@app.get("/")
async def root():
    return {"message": "Welcome to the PagerDuty Maintenance Window API"}
