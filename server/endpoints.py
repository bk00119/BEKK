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
VIEWGOALS_EP = '/viewGoals'
POSTGOAL_EP = '/postGoal'
VIEWGROUPS_EP = '/viewGroups'
POSTGROUP_EP = '/postGroup'
LIKETASK_EP = '/likeTask'


# Responses
TOKEN_RESP = 'token'
USERNAME_RESP = 'username'
TASK_RESP = 'task'
MESSAGE_RESP = 'message'
GOAL_RESP = 'goal'
GROUP_RESP = 'group'
LIKE_RESP = 'liked'


NAME = 'Name'
GOALS = 'Goals'
GROUPS = 'Groups'

TASKS = 'Tasks'

TASK_NAME = 'task name'
TASK_DESCRIPTION = 'task description'
LIKE = False


# User Example Data
TEST_USER_TOKEN = 'ABC123'
TEST_PROFILE = {
    NAME: 'John Smith',
    GOALS: ['cs hw2', 'fin hw3'],
    GROUPS: ['cs', 'fin']
}

# Task Example Data
TEST_TASK = {
    TASK_NAME: "SWE",
    TASK_DESCRIPTION: "BEKK final project",
    LIKE: True
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
            TASKS: ['task', 'task1', 'task2', 'task3', 'task4']
        }


@api.route(f'{POSTTASK_EP}', methods=['POST'])
class PostTask(Resource):
    """
    This class post task to user profile
    """
    def post(self):
        data = request.get_json()
        print(data['username'])
        return {
            TASK_RESP: TEST_TASK,
            USERNAME_RESP: data[USERNAME_RESP]
        }


@api.route(f'{VIEWGOALS_EP}', methods=['GET'])
class ViewGoals(Resource):
    """
    This class shows goals on the user profile.
    """
    def get(self):
        return {
            GOALS: ['goal', 'goal1', 'goal2', 'goal3', 'goal4']
        }


@api.route(f'{POSTGOAL_EP}', methods=['POST'])
class PostGoal(Resource):
    """
    This class posts goals to user profile.
    """
    def post(self):
        data = request.get_json()
        print(data['username'])
        return {
            GOAL_RESP: TEST_TASK,
            USERNAME_RESP: data[USERNAME_RESP]
        }


@api.route(f'{VIEWGROUPS_EP}', methods=['GET'])
class ViewGroup(Resource):
    """
    This class shows the groups for each user.
    """
    def get(self):
        return {
            GROUPS: ['group', 'group1', 'group2', 'group3', 'group4']
        }


@api.route(f'{POSTGROUP_EP}', methods=['POST'])
class PostGroup(Resource):
    """
    This class posts group to the user profile.
    """
    def post(self):
        data = request.get_json()
        print(data['username'])
        return {
            GROUP_RESP: TEST_TASK,
            USERNAME_RESP: data[USERNAME_RESP]
        }


@api.route(f'{LIKETASK_EP}', methods=['POST'])
class LikeTask(Resource):
    """
    This class likes the taks under user's task lists
    """
    def post(self):
        data = request.get_json()
        print(data['username'])
        return {
            LIKE_RESP: TEST_TASK,
            USERNAME_RESP: data[USERNAME_RESP]
        }
