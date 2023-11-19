"""
This module interfaces to our tasks data.
"""

from pymongo import MongoClient

test_tasks = {
    "task1": "SWE",
    "task2": "commits",
    "task3": "study"
}


def get_tasks():
    client = MongoClient()
    db = client.BEKK_DB
    tasks = db.tasks
    data = {}
    # data = []
    for task in tasks.find():
        # Convert ObjectId to String so it is JSON serializable
        # task['_id'] = str(task['_id'])
        key = str(task['_id'])
        del task['_id']
        data[key] = task
        # data.append(task)
    return data


def get_test_tasks():
    return {
        "Tasks": ['task1', 'task2', 'task3']
    }
