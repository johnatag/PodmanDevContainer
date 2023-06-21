from fastapi import FastAPI, HTTPException
from mongoengine import connection
from bson import ObjectId
from decorators import count_endpoint_invokation
from models.tasks import Tasks

app = FastAPI()
connection.disconnect()
connection.connect(
    db='todo',
    username='root',
    password='rootpassword',
    host='mongodb',
    port=27017,
)

@app.get("/")
@count_endpoint_invokation
async def get_status():
    try:
        return connection._connections != 0
    except:
        raise HTTPException(status_code=500, detail="MongoDB connection failed")

@app.post("/tasks")
@count_endpoint_invokation
async def create_task(title: str, description: str):
    try:
        task = Tasks(task_id=ObjectId(), title=title, description=description)
        task.save()
        return "Task created successfully, {task}".format(task=task)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Task creation failed, {exception}".format(exception=e))

@app.get("/tasks")
@count_endpoint_invokation
async def get_tasks():
    try:
        all_tasks = Tasks.objects()
        serialized_tasks = [str(task) for task in all_tasks]
        return serialized_tasks
    except Exception as e:
        raise HTTPException(status_code=500, detail="Task query failed, {e}".format(e=e))

@app.get("/tasks/{id}")
@count_endpoint_invokation
async def get_task(id: str):
    try:
        task = Tasks.objects.get(task_id=id)
        return task.to_json()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve task: " + str(e))

@app.put("/tasks/{id}")
@count_endpoint_invokation
async def update_task(id: str, title: str, description: str):
    try:
        task = Tasks.objects.get(task_id=id)
        task.title = title
        task.description = description
        task.save()
        return "Task updated successfully"
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to update task: " + str(e))
    
@app.delete("/tasks")
@count_endpoint_invokation
async def delete_all_tasks():
    try:
        Tasks.objects().delete()
        return "All tasks deleted successfully"
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to delete tasks: " + str(e))

@app.delete("/tasks/{id}")
@count_endpoint_invokation
async def delete_task(id: str):
    try:
        task = Tasks.objects.get(task_id=id)
        task.delete()
        return "Task deleted successfully"
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to delete task: " + str(e))