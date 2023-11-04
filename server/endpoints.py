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
LOGOUT_EP = '/logout'
SIGNUP_EP = '/signup'
PROFILE_EP = '/profile'
VIEWTASKS_EP = '/viewTasks'
POSTTASK_EP = '/postTask'

# Responses
TOKEN_RESP = 'token'
USERNAME_RESP = 'username'
TASK_RESP = 'task'
MESSAGE_RESP = 'message'

NAME = 'Name'
GOALS = 'Goals'
GROUPS = 'Groups'

TASKS = 'Tasks'


# User Example Data
TEST_USER_TOKEN = 'ABC123'
TEST_PROFILE = {
    NAME: 'John Smith',
    GOALS: ['cs hw2', 'fin hw3'],
    GROUPS: ['cs', 'fin']
}


@api.route(f'{LOGIN_EP}', methods=['POST'])
class Login(Resource):
    """
    This class supports fetching a user data for login
    """
    def post(self):
        return {
            TOKEN_RESP: TEST_USER_TOKEN
        }


@api.route(f'{LOGOUT_EP}', methods=['POST'])
class Logout(Resource):
    """
    This class supports fetching a user data for logout
    """
    def post(self):
        return {
            MESSAGE_RESP: 'YOU HAVE SUCCESSFULLY LOGGED OUT'
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
            TOKEN_RESP: TEST_USER_TOKEN,
            USERNAME_RESP: data[USERNAME_RESP]
        }


@api.route(f'{PROFILE_EP}', methods=['GET'])
class Profile(Resource):
    """
    This class will deliver contents for user profile.
    """
    def get(self):
        return TEST_PROFILE


@api.route(f'{VIEWTASKS_EP}', methods=['GET'])
class ViewTasks(Resource):
    """
    This class will show tasks for the user profile
    """
    def get(self):
        return {
            TASKS: ['task1', 'task2', 'task3', 'task4']
        }


@api.route(f'{POSTTASK_EP}', methods=['POST'])
class PostTask(Resource):
    """
    This class post task to user profile
    """
    def post(self):
        data = request.get_json()
        print(data['task'])
        return {
            TASK_RESP: data[TASK_RESP]
        }
