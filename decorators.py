import time
from functools import wraps
from opentelemetry.metrics import get_meter

meter = get_meter(__name__)

import time
from functools import wraps
from opentelemetry.metrics import get_meter

def count_endpoint_invokation(endpoint):
    @wraps(endpoint)
    async def wrapper(*args, **kwargs):
        metric_name = f"{endpoint.__name__}_invokation_counter"
        metric_description = f"Counts the number of successful invocations of the {endpoint.__name__} endpoint"

        counter = meter.create_counter(name=metric_name, description=metric_description, unit="1")
        try:
            response = await endpoint(*args, **kwargs)
            counter.add(1, {"invokation.status": "success"})
            return response
        except Exception as e:
            counter.add(1, {"invokation.status": "error"})
            raise e

    return wrapper