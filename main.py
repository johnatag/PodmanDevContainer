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

def check_mongodb_connection():
    try:
        # Get the MongoDB connection
        conn = connection.get_connection()

        # Check if the connection is alive
        if conn is not None and conn.is_primary:
            return True
        else:
            return False
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"MongoDB connection error: {e}")

@app.get("/")
@count_endpoint_invokation
async def get_status():
    try:
        return check_mongodb_connection()
    except:
        raise HTTPException(status_code=503, detail="MongoDB connection failed")

@app.head("/")
@count_endpoint_invokation
async def head_status():
    # Downstream Operation Status	Your API may depend on other APIs to operate. Make sure to check the operational status of the downstream APIs you depend on
    # Database connection	Your API may have an open connection to a data source. Make sure the connection is available at the time of the health check
    # Database response time	Measure the average response time to a typical DB query
    try:
        return check_mongodb_connection()
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

@app.delete("/tasks")
@count_endpoint_invokation
async def delete_all_tasks():
    try:
        Tasks.objects().delete()
        return "All tasks deleted successfully"
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to delete tasks: " + str(e))
    
@app.head("/tasks")
@count_endpoint_invokation
async def head_tasks():
    # Downstream Operation Status	Your API may depend on other APIs to operate. Make sure to check the operational status of the downstream APIs you depend on
    # Database connection	Your API may have an open connection to a data source. Make sure the connection is available at the time of the health check
    # Database response time	Measure the average response time to a typical DB query
    try:
        return check_mongodb_connection()
    except:
        raise HTTPException(status_code=503, detail="MongoDB connection failed")

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

@app.delete("/tasks/{id}")
@count_endpoint_invokation
async def delete_task(id: str):
    try:
        task = Tasks.objects.get(task_id=id)
        task.delete()
        return "Task deleted successfully"
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to delete task: " + str(e))

@app.head("/tasks/{id}")
@count_endpoint_invokation
async def head_task():
    # Downstream Operation Status	Your API may depend on other APIs to operate. Make sure to check the operational status of the downstream APIs you depend on
    # Database connection	Your API may have an open connection to a data source. Make sure the connection is available at the time of the health check
    # Database response time	Measure the average response time to a typical DB query
    try:
        return check_mongodb_connection()
    except:
        raise HTTPException(status_code=503, detail="MongoDB connection failed")