"""
This module interfaces to our tasks data.
"""

# from pymongo import MongoClient
import random
from datetime import datetime
from bson.objectid import ObjectId
import db.db_connect as dbc
import db.users as usrs
import db.goals as goals

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
GOAL_ID = 'goal_id'
IS_COMPLETED = 'is_completed'
TIMESTAMP = 'timestamp'

ID_LEN = 24
BIG_NUM = 100_000_000_000_000_000_000
MOCK_ID = MOCK_ID = '0' * ID_LEN


def id_exists(id: str) -> bool:
    dbc.connect_db()
    return dbc.fetch_one(TASKS_COLLECT, {ID: ObjectId(id)})


def get_task(task_id: str):
    if id_exists(task_id):
        return dbc.fetch_one(TASKS_COLLECT, {ID: ObjectId(task_id)})
    else:
        raise ValueError(f'Get failure: {task_id} not in database.')


def get_tasks(filter=None):
    dbc.connect_db()
    return dbc.fetch_all_as_dict(dbc.DB, TASKS_COLLECT, filter)


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
    test_task[USER_ID] = '6575033f3b89d2b4f309d7af'
    test_task[GOAL_ID] = '65d2dd8abe686c2ec340e298'
    test_task[CONTENT] = 'attend CS101 Office Hours'
    test_task[IS_COMPLETED] = False

    return test_task


def add_task(user_id: str, goal: str, content: str, is_completed: bool):
    # if not user_id:
    #     raise ValueError('user_id may not be blank')
    # if not title:
    #     raise ValueError('title may not be blank')
    # if not content:
    #     raise ValueError('content may not be blank')
    task = {}
    task[USER_ID] = user_id
    # task[GOAL_ID] = goal
    task[CONTENT] = content
    task[IS_COMPLETED] = is_completed
    task[TIMESTAMP] = str(datetime.now())
    dbc.connect_db()
    _id = dbc.insert_one(TASKS_COLLECT, task)

    # UPDATE GOAL
    dbc.update_one(
        goals.GOALS_COLLECT,
        {goals.ID: ObjectId(goal)},
        {"$addToSet": {goals.TASK_IDS: _id}}
    )
    return _id


def update_task(task_id: str, content: str, is_completed: bool):
    if id_exists(task_id):
        if content is not None and is_completed is not None:
            # UPDATE BOTH CONTENT AND IS_COMPLETED
            dbc.update_one(
                TASKS_COLLECT,
                {ID: ObjectId(task_id)},
                {"$set": {CONTENT: content, IS_COMPLETED: is_completed}},
            )
        elif content is not None:
            dbc.update_one(
                TASKS_COLLECT,
                {ID: ObjectId(task_id)},
                {"$set": {CONTENT: content}},
            )
        elif is_completed is not None:
            dbc.update_one(
                TASKS_COLLECT,
                {ID: ObjectId(task_id)},
                {"$set": {IS_COMPLETED: is_completed}},
            )
        else:
            raise ValueError(f'Task update failure: task {task_id}'
                             + ' needs one of content value'
                             + ' or is_completed value')
    else:
        raise ValueError(f'Task update failure: task {task_id}'
                         + 'not in database.')


def del_task(task_id: str):
    if id_exists(task_id):
        return dbc.del_one(TASKS_COLLECT, {ID: ObjectId(task_id)})
    else:
        raise ValueError(f'Delete failure: {task_id} not in database.')


def get_user_tasks(user_id: str):
    if usrs.id_exists(user_id):
        return dbc.fetch_all_as_dict(dbc.DB, TASKS_COLLECT, {USER_ID: user_id})
    else:
        raise ValueError(f'Get failure: {user_id} not in database.')


def is_task_liked(task_id: str, user_id: str):
    if id_exists(task_id):
        task = dbc.fetch_one(
            TASKS_COLLECT,
            {ID: ObjectId(task_id), LIKES: {"$in": [user_id]}}
        )
        if task:
            return True
        return False
    else:
        raise ValueError(f'Task like failure: task {task_id} not in database.')


def like_task(task_id: str, user_id: str):
    if id_exists(task_id):
        if is_task_liked(task_id, user_id):
            raise ValueError('Task like failure: ' +
                             f'user {user_id} already liked ' +
                             f'task {task_id}')
        dbc.update_one(
            TASKS_COLLECT,
            {ID: ObjectId(task_id)},
            {"$addToSet": {"likes": user_id}}
        )
    else:
        raise ValueError(f'Task like failure: task {task_id} not in database.')


def unlike_task(task_id: str, user_id: str):
    if id_exists(task_id):
        if not is_task_liked(task_id, user_id):
            raise ValueError('Task unlike failure: ' +
                             f'user {user_id} not liked ' +
                             f'task {task_id}')
        dbc.update_one(
            TASKS_COLLECT,
            {ID: ObjectId(task_id)},
            {"$pull": {"likes": user_id}}
        )
    else:
        raise ValueError('Task unlike failure: ' +
                         f'task {task_id} not in database.')
