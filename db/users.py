"""
This module interfaces to our user data.
"""

import random

ID_LEN = 24
BIG_NUM = 100_000_000_000_000_000_000

MOCK_ID = '0' * ID_LEN

LEVEL = 'level'
MIN_USER_NAME_LEN = 2


test_users = {
    'user1234': 'pwpw123',
    'user456': 'pwpw456'
}


def _gen_id() -> str:
    _id = random.randint(0, BIG_NUM)
    _id = str(_id)
    _id = _id.rjust(ID_LEN, '0')
    return _id


def get_users():
    return {
        "Name": 'John Smith',
        "Goals": ['goal1', 'goal2'],
        "Groups": ['group1', 'group2']
    }


def get_test_user():
    return {'username': 'user1234', 'password': 'pwpw1234'}


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
