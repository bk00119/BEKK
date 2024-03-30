"""
This module interfaces to our user data.
"""

import random
# import uuid
from bson.objectid import ObjectId
from datetime import datetime, timedelta
import db.db_connect as dbc
import bcrypt
import jwt
from flask import make_response, jsonify
import db.auth as auth

USERS_COLLECT = 'users'

ID = '_id'
FIRST_NAME = 'first_name'
LAST_NAME = 'last_name'
USERNAME = 'username'
EMAIL = 'email'
STREAKS = 'streaks'
PASSWORD = 'password'
USER_ID = 'user_id'
REFRESH_TOKEN = 'refresh_token'
ACCESS_TOKEN = 'access_token'

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


def get_user_public(user_id: str):
    if id_exists(user_id):
        data = dbc.fetch_one(USERS_COLLECT, {ID: ObjectId(user_id)})
        return {
          EMAIL: data['email'],
          USERNAME: data['username'],
          FIRST_NAME: data['first_name'],
          LAST_NAME: data['last_name']
        }
    else:
        raise ValueError(f'Get failure: {user_id} not in database.')


def get_user_private(user_id: str):
    if id_exists(user_id):
        dbc.connect_db()
        data = dbc.fetch_one(USERS_COLLECT, {ID: ObjectId(user_id)})
        return data
    else:
        raise ValueError(f'Get failure: {user_id} not in database.')


def retrieve_user(username):
    if username:
        return test_users[username]
    else:
        return None


def get_test_user():
    # return {'username': 'user1234', 'password': 'pwpw1234'}
    return {'first_name': "John", "last_name": "Doe", "username": "johndoe123",
            "email": "johndoe@gmail.com",
            "streaks": {'num_streaks': 2, "updated": True}}


def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')


def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'),
                          hashed_password.encode('utf-8'))


def generate_access_token(user_id):
    # ACCESS TOKEN
    token_payload = {
        USER_ID: user_id,
        'exp': datetime.utcnow()
        + timedelta(seconds=auth.JWT_ACCESS_TOKEN_EXPIRATION)
    }
    access_token = jwt.encode(token_payload,
                              auth.SECRET_KEY, algorithm='HS256')
    return access_token


def generate_refresh_token(user_id):
    # REFRESH TOKEN
    token_payload = {
        USER_ID: user_id,
        'exp': datetime.utcnow()
        + timedelta(seconds=auth.JWT_REFRESH_TOKEN_EXPIRATION)
    }
    refresh_token = jwt.encode(token_payload,
                               auth.SECRET_KEY, algorithm='HS256')

    # STORE THE REFRESH TOKEN IN THE DATABASE
    # dbc already connected
    dbc.update_one(
      USERS_COLLECT,
      {ID: ObjectId(user_id)},
      {"$set": {"refresh_token": refresh_token}}
    )

    return refresh_token


def remove_user(user_id):
    dbc.connect_db()
    if id_exists(user_id):
        return dbc.del_one(USERS_COLLECT, {ID: ObjectId(user_id)})
    else:
        raise ValueError(f'Delete failure: {user_id} not in database.')


def signup(user):
    if not user:
        raise ValueError('User may not be blank')
    # username = user['username']
    # password = user['password']
    # if not username:
    #     raise ValueError('Username may not be blank')
    # if username in test_users:
    #     raise ValueError(f'Duplicate username: {username=}')
    # if not password:
    #     raise ValueError('Password may not be blank')
    # test_users[username] = password
    # return _gen_id()

    # NEED TO MODIFY THIS WHEN WORKING ON USER SIGN UP
    user[PASSWORD] = hash_password(user[PASSWORD])

    dbc.connect_db()
    _id = dbc.insert_one(USERS_COLLECT, user)
    return _id


def login(user):
    if not user:
        raise ValueError('User may not be blank')
    email = user['email']
    password = user['password']
    if not email:
        raise ValueError('Email may not be blank')
    if not password:
        raise ValueError('Password may not be blank')
    dbc.connect_db()
    data = dbc.fetch_one(USERS_COLLECT, {EMAIL: email})
    if not data:
        raise ValueError('Invalid email or password')

    # CHECK IF THE PASSWORD FROM REQUEST MATCHES THE STORED PASSWORD
    if verify_password(password, data[PASSWORD]):
        # GENERATE JWT TOKEN
        access_token = generate_access_token(data[ID])
        refresh_token = generate_refresh_token(data[ID])

        response = make_response(jsonify({'message': 'Login successful',
                                          'access_token': access_token,
                                          'refresh_token': refresh_token,
                                          ID: data[ID],
                                          USERNAME: data[USERNAME],
                                          FIRST_NAME: data[FIRST_NAME],
                                          LAST_NAME: data[LAST_NAME],
                                          EMAIL: data[EMAIL]}))
        return response

    else:
        raise ValueError('Invalid email or password')
