from typing import Union
from fastapi import FastAPI

from opentelemetry.metrics import get_meter


app = FastAPI()

meter = get_meter("example-meter")
work_counter = meter.create_counter(
    "work.counter", unit="1", description="Counts the amount of work done"
)

@app.get("/")
def read_root():
    work_counter.add(1, {"work.type": "root"})
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int):
    work_counter.add(1, {"work.type": "item"})
    return {"item_id": item_id}