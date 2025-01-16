from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List
import requests
import datetime

app = FastAPI()

PAGERDUTY_API_TOKEN = "YOUR_API_TOKEN"  # Replace with your PagerDuty API token
PAGERDUTY_API_BASE_URL = "https://api.pagerduty.com"
MAINTENANCE_WINDOW_DESCRIPTION = "Scheduled maintenance window"

# Pydantic Models
class MaintenanceWindowCreateRequest(BaseModel):
    service_ids: List[str]
    duration_minutes: int

class MaintenanceWindowDeleteRequest(BaseModel):
    maintenance_window_id: str


def create_maintenance_window(service_ids: List[str], duration_minutes: int):
    if duration_minutes > 30:
        raise HTTPException(status_code=400, detail="Duration cannot exceed 30 minutes.")
    
    now = datetime.datetime.utcnow()
    start_time = now.isoformat() + "Z"
    end_time = (now + datetime.timedelta(minutes=duration_minutes)).isoformat() + "Z"

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
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)

def delete_maintenance_window(maintenance_window_id: str):
    url = f"{PAGERDUTY_API_BASE_URL}/maintenance_windows/{maintenance_window_id}"
    headers = {
        "Authorization": f"Token token={PAGERDUTY_API_TOKEN}",
        "Accept": "application/vnd.pagerduty+json;version=2"
    }

    response = requests.delete(url, headers=headers)
    if response.status_code == 204:
        return {"status": "success", "message": f"Maintenance window {maintenance_window_id} deleted successfully."}
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)

# FastAPI create maintenance window
@app.post("/create-maintenance-window")
async def create_window(request: MaintenanceWindowCreateRequest, user_email: str = Query(..., description="User email is mandatory")):
    """
    Create a maintenance window.
    """
    try:
        result = create_maintenance_window(request.service_ids, request.duration_minutes)
        return {
            "status": "success",
            "message": "Maintenance window created successfully.",
            "data": result
        }
    except HTTPException as e:
        raise e

# FastAPI delete maintenance window
@app.delete("/delete-maintenance-window")
async def delete_window(request: MaintenanceWindowDeleteRequest, user_email: str = Query(..., description="User email is mandatory")):
    """
    Delete a maintenance window.
    """
    try:
        result = delete_maintenance_window(request.maintenance_window_id)
        return {
            "status": "success",
            "message": "Maintenance window deleted successfully.",
            "data": result
        }
    except HTTPException as e:
        raise e
