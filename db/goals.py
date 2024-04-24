"""
This module interfaces to our goals data.
"""

# from pymongo import MongoClient
import random
from bson.objectid import ObjectId
from datetime import datetime
import db.db_connect as dbc
import db.users as usrs
import db.tasks as tasks

# GOALS COLLECTION:
# _id: ObjectID
# user_id: str(ObjectID)
# is_completed: Bool
# content: str

GOALS_COLLECT = 'goals'
ID = '_id'
USER_ID = 'user_id'
IS_COMPLETED = 'is_completed'
CONTENT = 'content'
TASK_IDS = 'task_ids'
TIMESTAMP = 'timestamp'

ID_LEN = 24
BIG_NUM = 100_000_000_000_000_000_000
MOCK_ID = MOCK_ID = '0' * ID_LEN


def get_goals():
    dbc.connect_db()
    return dbc.fetch_all_as_dict(dbc.DB, GOALS_COLLECT, None)


def get_test_goals():
    return {
        "user_id": 'user123', 'is_completed': True,
        'content': 'complete 20 leetcode problems'
    }


def get_new_test_goals():
    '''
    sample task for testing set_goals()
    '''
    set_goal = {}
    _id = random.randint(0, BIG_NUM)
    _id = str(_id)
    _id = _id.rjust(ID_LEN, '0')
    set_goal[USER_ID] = '6575033f3b89d2b4f309d7af'
    set_goal[CONTENT] = 'read 5 books'
    set_goal[IS_COMPLETED] = False
    # set_goal[TASK_IDS] = []
    return set_goal


def id_exists(id: str) -> bool:
    dbc.connect_db()
    return dbc.fetch_one(GOALS_COLLECT, {ID: ObjectId(id)})


def set_goal(user_id: str, content: str, is_completed: bool):
    '''
    user sets/adds a goal, which is added to the Goals DB
    '''
    goal = {}
    goal[USER_ID] = user_id
    goal[CONTENT] = content
    goal[IS_COMPLETED] = is_completed  # DO WE NEED THIS??
    goal[TASK_IDS] = []  # SET TO AN EMPTY ARRAY
    goal[TIMESTAMP] = str(datetime.now())
    dbc.connect_db()
    _id = dbc.insert_one(GOALS_COLLECT, goal)
    return _id


def delete_set_goal(goal_id: str):
    if id_exists(goal_id):
        return dbc.del_one(GOALS_COLLECT, {ID: ObjectId(goal_id)})
    else:
        raise ValueError(f'Delete Goal Failed: {goal_id} not in database.')


def get_set_goal(goal_id: str):
    if id_exists(goal_id):
        return dbc.fetch_one(GOALS_COLLECT, {ID: ObjectId(goal_id)})
    else:
        raise ValueError(f'Get Goal Failed: {goal_id} not in database.')


def get_user_goals(user_id: str):
    if usrs.id_exists(user_id):
        goals = dbc.fetch_all_as_dict(dbc.DB, GOALS_COLLECT,
                                      {USER_ID: user_id})
        for goal_id in goals:
            goals[goal_id]['tasks'] = []
            for task_id in goals[goal_id]['task_ids']:
                goals[goal_id]['tasks'].append(tasks.get_task(task_id))
        return goals
    else:
        raise ValueError(f'Get User Goals Failed: {user_id} not in database.')


def add_task_to_goal(goal_id: str, task_id: str):
    if not id_exists(goal_id):
        raise ValueError(f'Add task to goal: {goal_id} not in database.')
    dbc.connect_db()
    dbc.update_one(
        GOALS_COLLECT,
        {ID: ObjectId(goal_id)},
        {"$addToSet": {TASK_IDS: task_id}}
    )


def check_task_completion(goal_id: str):
    if not id_exists(goal_id):
        raise ValueError('check_task_completion goal: '
                         + f'{goal_id} not in database.')
    data = get_set_goal(ObjectId(goal_id))
    if TASK_IDS not in data:
        raise ValueError('check_task_completion task_ids'
                         + f' not in goal: {goal_id}.')
    for task in data[TASK_IDS]:
        task_data = tasks.get_task(task)
        if tasks.IS_COMPLETED not in task_data:
            raise ValueError('check_task_completion is_completed'
                             + f' not in task_id: {task}.')
        if not task_data[tasks.IS_COMPLETED]:
            return False
    return True


def set_goal_completion(goal_id: str, is_completed: bool):
    if not id_exists(goal_id):
        raise ValueError('check_task_completion goal:'
                         + f' {goal_id} not in database.')
    dbc.connect_db()
    dbc.update_one(
        GOALS_COLLECT,
        {ID: ObjectId(goal_id)},
        {"$set": {IS_COMPLETED: is_completed}}
    )
