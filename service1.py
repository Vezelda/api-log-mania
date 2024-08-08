import requests
import json
import time
from datetime import datetime

while True:
    log = {
        "timestamp": datetime.utcnow().isoformat(),
        "service_name": "Service1",
        "log_level": "INFO",
        "message": "Este es un mensaje de log de ejemplo de Service1"
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer token1"
    }
    response = requests.post("http://localhost:5000/logs", headers=headers, data=json.dumps(log))
    print("Log enviado:", response.status_code)
    time.sleep(10)
