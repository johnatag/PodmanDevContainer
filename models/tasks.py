import datetime
from mongoengine import *

class Tasks(Document):
    task_id = ObjectIdField()
    title = StringField(required=True, max_length=200)
    description = StringField(required=True, max_length=200)
    posted = DateTimeField(default=datetime.datetime.utcnow())

    def __str__(self):
        return f"Task_id: {self.task_id},\nTitle: {self.title},\nDescription: {self.description},\nPosted: {self.posted}"


