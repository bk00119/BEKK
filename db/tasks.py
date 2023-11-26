"""
This module interfaces to our tasks data.
"""

# from pymongo import MongoClient
import db.db_connect as dbc

test_tasks = {
    "task1": "SWE",
    "task2": "commits",
    "task3": "study"
}

# TASK COLLECTION:
# _id: ObjectID
# user_id: str(ObjectID)
# title: str
# content: str
# status: int
# likes: [str(ObjectID)]

TASKS_COLLECT = 'tasks'


def get_tasks():
    dbc.connect_db()
    return dbc.fetch_all_as_dict(dbc.DB, TASKS_COLLECT)


def get_test_tasks():
    return {
        "Tasks": ['task1', 'task2', 'task3']
    }
