import datetime
import requests
import os

def log_crm_heartbeat():
    """Logs a heartbeat message every 5 minutes."""
    now = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    log_message = f"{now} CRM is alive\n"
    
    log_file_path = "/tmp/crm_heartbeat_log.txt"

    # Append to the log file
    with open(log_file_path, "a") as f:
        f.write(log_message)
    
    # Optional: ping GraphQL hello field
    try:
        response = requests.post(
            "http://localhost:8000/graphql/",
            json={"query": "{ hello }"},
            timeout=5
        )
        if response.status_code == 200:
            with open(log_file_path, "a") as f:
                f.write(f"{now} GraphQL endpoint responsive\n")
        else:
            with open(log_file_path, "a") as f:
                f.write(f"{now} GraphQL endpoint returned {response.status_code}\n")
    except Exception as e:
        with open(log_file_path, "a") as f:
            f.write(f"{now} GraphQL endpoint error: {e}\n")

