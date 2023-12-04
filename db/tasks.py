"""
This module interfaces to our tasks data.
"""

# from pymongo import MongoClient
import random
from bson.objectid import ObjectId
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

ID = '_id'
USER_ID = 'user_id'
TITLE = 'title'
CONTENT = 'content'
STATUS = 'status'
LIKES = 'likes'

ID_LEN = 24
BIG_NUM = 100_000_000_000_000_000_000
MOCK_ID = MOCK_ID = '0' * ID_LEN


def get_tasks():
    dbc.connect_db()
    return dbc.fetch_all_as_dict(dbc.DB, TASKS_COLLECT)


def get_test_tasks():
    return {
        "Tasks": ['task1', 'task2', 'task3']
    }


def get_new_test_task():
    """
    example task for testing add_task()
    """
    test_task = {}
    _id = random.randint(0, BIG_NUM)
    _id = str(_id)
    _id = _id.rjust(ID_LEN, '0')
    test_task[USER_ID] = 'test123'
    test_task[TITLE] = 'Test Title'
    test_task[CONTENT] = 'Test Content'
    return test_task


def id_exists(id: str) -> bool:
    dbc.connect_db()
    return dbc.fetch_one(TASKS_COLLECT, {ID: ObjectId(id)})


def add_task(user_id: str, title: str, content: str):
    if not user_id:
        raise ValueError('user_id may not be blank')
    if not title:
        raise ValueError('title may not be blank')
    if not content:
        raise ValueError('content may not be blank')
    task = {}
    task[USER_ID] = user_id
    task[TITLE] = title
    task[CONTENT] = content
    task[STATUS] = 1
    task[LIKES] = []
    dbc.connect_db()
    _id = dbc.insert_one(TASKS_COLLECT, task)
    return _id


def del_task(task_id: str):
    if id_exists(task_id):
        return dbc.del_one(TASKS_COLLECT, {ID: ObjectId(task_id)})
    else:
        raise ValueError(f'Delete failure: {task_id} not in database.')


def get_task(task_id: str):
    if id_exists(task_id):
        return dbc.fetch_one(TASKS_COLLECT, {ID: ObjectId(task_id)})
    else:
        raise ValueError(f'Get failure: {task_id} not in database.')
