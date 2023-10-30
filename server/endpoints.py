"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""

from flask import Flask, request
from flask_restx import Resource, Api
# import db.db as db

app = Flask(__name__)
api = Api(app)

# Endpoints
LOGIN_EP = '/login'
SIGNUP_EP = '/signup'
PROFILE_EP = '/profile'
VIEWTASKS_EP = '/viewTasks'

# Responses
TOKEN_RESP = 'token'
USERNAME_RESP = 'username'

NAME = 'Name'
GOALS = 'Goals'
GROUPS = 'Groups'

TASKS = 'Tasks'


@api.route(f'{LOGIN_EP}', methods=['POST'])
class Login(Resource):
    """
    This class supports fetching a user data for login
    """
    def post(self):
        return {
            TOKEN_RESP: 'ABC123'
        }


@api.route(f'{SIGNUP_EP}', methods=['POST'])
class Signup(Resource):
    """
    This class supports fetching a user data for signup
    """
    def post(self):
        data = request.get_json()
        print(data['username'])
        return {
            TOKEN_RESP: 'ABC123',
            USERNAME_RESP: data[USERNAME_RESP]
        }


@api.route(f'{PROFILE_EP}', methods=['GET'])
class Profile(Resource):
    """
    This class will deliver contents for user profile.
    """
    def get(self):
        return {
                NAME: 'John Smith',
                GOALS: ['cs hw2', 'fin hw3'],
                GROUPS: ['cs', 'fin']
            }


@api.route(f'{VIEWTASKS_EP}', methods=['GET'])
class ViewTasks(Resource):
    """
    This class will show tasks for the user profile
    """
    def get(self):
        return {
            TASKS: ['task1', 'task2', 'task3', 'task4']
        }