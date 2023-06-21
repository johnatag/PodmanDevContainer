import time
import requests
import schedule

from opentelemetry import trace

endpoints = [
    {
        "name": "GetStatus",
        "url": "http://localhost:8000/",
    },
    {
        "name": "AllTasks",
        "url": "http://localhost:8000/tasks",
    },
    {
        "name": "SpecificTask",
        "url": "http://localhost:8000/tasks/{id}",
    }
]

tracer = trace.get_tracer(__name__)

def perform_health_check():
    # Sample ID
    id_value = "6490609aa4f241ad5618f6f6"

    with tracer.start_as_current_span("Healthcheck"):
        for endpoint in endpoints:
            url = endpoint["url"].format(id=id_value)
            response = None
            try:
                with tracer.start_as_current_span(endpoint["name"]):
                    response = requests.head(url)
                    # Process the response
                    if response.status_code == 200:
                        print(f"{endpoint['name']} is available")
                    else:
                        print(f"{endpoint['name']} is down with status code {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"{endpoint['name']} is down with an exception: {e}")


schedule.every(1).minutes.do(perform_health_check)

while True:
    schedule.run_pending()
    time.sleep(1)

