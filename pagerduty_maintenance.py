import requests
import datetime

# Configuration
PAGERDUTY_API_TOKEN = "YOUR_API_TOKEN"  # Replace with your PagerDuty API token
PAGERDUTY_API_BASE_URL = "https://api.pagerduty.com"  # API base URL
SERVICE_IDS = ["SERVICE_ID_1", "SERVICE_ID_2"]  # Replace with your service IDs
MAINTENANCE_WINDOW_DESCRIPTION = "Scheduled maintenance window"

def create_maintenance_window(service_ids, start_time, end_time):
    """
    Creates a maintenance window for multiple services on PagerDuty.
    :param service_ids: List of service IDs to include in the maintenance window.
    :param start_time: Start time in ISO 8601 format.
    :param end_time: End time in ISO 8601 format.
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
        print("Successfully created maintenance window.")
        print(response.json())
    else:
        print(f"Failed to create maintenance window: {response.status_code} - {response.text}")

def main():
    # Set up start and end times for the maintenance window
    now = datetime.datetime.utcnow()
    start_time = now.isoformat() + "Z"  # Current UTC time in ISO 8601 format
    end_time = (now + datetime.timedelta(hours=2)).isoformat() + "Z"  # 2 hours from now

    # Create the maintenance window
    create_maintenance_window(SERVICE_IDS, start_time, end_time)

if __name__ == "__main__":
    main()
