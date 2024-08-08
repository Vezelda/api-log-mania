import requests
import json
import time
from datetime import datetime

while True:
    log = {
        "timestamp": datetime.utcnow().isoformat(),
        "service_name": "Service2",
        "log_level": "ERROR",
        "message": "Este es un mensaje de log de ejemplo de Service2"
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer token2"
    }
    response = requests.post("http://localhost:5000/logs", headers=headers, data=json.dumps(log))
    print("Log enviado:", response.status_code)
    time.sleep(15)
