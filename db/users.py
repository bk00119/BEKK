"""
This module interfaces to our user data.
"""

import random
from bson.objectid import ObjectId
import db.db_connect as dbc

USERS_COLLECT = 'users'

ID = '_id'
FIRST_NAME = 'first_name'
LAST_NAME = 'last_name'
USERNAME = 'username'
EMAIL = 'email'
STREAKS = 'streaks'

ID_LEN = 24
BIG_NUM = 100_000_000_000_000_000_000

MOCK_ID = '0' * ID_LEN

LEVEL = 'level'
MIN_USER_NAME_LEN = 2


test_users = {
    'user1234': 'pwpw123',
    'user456': 'pwpw456'
}

sample_user = {
    FIRST_NAME: "John",
    LAST_NAME: "Doe",
    USERNAME: "johndoe123",
    EMAIL: "johndoe@gmail.com",
    STREAKS: {'num_streaks': 2, "updated": True}
}


def id_exists(id: str) -> bool:
    dbc.connect_db()
    return dbc.fetch_one(USERS_COLLECT, {ID: ObjectId(id)})


def _gen_id() -> str:
    _id = random.randint(0, BIG_NUM)
    _id = str(_id)
    _id = _id.rjust(ID_LEN, '0')
    return _id


def get_users():
    # return {
    #     "Name": 'John Smith',
    #     "Goals": ['goal1', 'goal2'],
    #     "Groups": ['group1', 'group2']
    # }
    return test_users


def get_user():
    return sample_user


def retrieve_user(username):
    if username:
        return test_users[username]
    else:
        return None


def get_test_user():
    # return {'username': 'user1234', 'password': 'pwpw1234'}
    return {'first_name': "John", "last_name": "Doe", "username": "johndoe123", "email": "johndoe@gmail.com", "streaks": {'num_streaks': 2, "updated": True}}


def signup(user):
    if not user:
        raise ValueError('User may not be blank')
    username = user['username']
    password = user['password']
    if not username:
        raise ValueError('Username may not be blank')
    if username in test_users:
        raise ValueError(f'Duplicate username: {username=}')
    if not password:
        raise ValueError('Password may not be blank')
    test_users[username] = password
    return _gen_id()
