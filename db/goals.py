"""
This module interfaces to our goals data.
"""

# from pymongo import MongoClient
# import random
# from bson.objectid import ObjectId
import db.db_connect as dbc

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
