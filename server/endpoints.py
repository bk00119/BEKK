"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""
from http import HTTPStatus
from flask import Flask, request
from flask_restx import Resource, Api, fields
from db import profiles as pf
from db import tasks as tasks
import werkzeug.exceptions as wz
# import db.db as db

app = Flask(__name__)
api = Api(app)

# Endpoints
LOGIN_EP = '/login'
LOGOUT_EP = '/logout'
SIGNUP_EP = '/signup'
PROFILE_EP = '/profile'
CREATEPROFILE_EP = '/createProfile'
VIEWTASKS_EP = '/viewTasks'
POSTTASK_EP = '/postTask'
VIEWGOALS_EP = '/viewGoals'
POSTGOAL_EP = '/postGoal'
DELETEGOAL_EP = '/deleteGoal'
VIEWGROUPS_EP = '/viewGroups'
POSTGROUP_EP = '/postGroup'
DELETEGROUP_EP = '/deleteGroup'
LIKETASK_EP = '/likeTask'
UNLIKETASK_EP = '/unlikeTask'
PROFILEVALIDATION_EP = '/profilevalidation'
REMOVEPROFILE_EP = '/removeProfile'
VIEWPROFILE_EP = '/viewProfile'


# Responses
TOKEN_RESP = 'token'
USERNAME_RESP = 'username'
PASSWORD_RESP = 'password'
PROFILE_VALID_RESP = "profilevalidation"
TASK_RESP = 'task'
MESSAGE_RESP = 'message'
GOAL_RESP = 'goal'
GROUP_RESP = 'group'
LIKE_RESP = 'liked'
UNLIKE_RESP = 'unliked'


NAME = 'Name'
GOALS = 'Goals'
GROUPS = 'Groups'
PRIVATE = "Private"

TASKS = 'Tasks'
TASK_ID = 'Task ID'
PROFILE = {
    NAME: 'John Smith',
    GOALS: ['cs hw2', 'fin hw3'],
    GROUPS: ['cs', 'fin'],
    PRIVATE: False
}
PROFILE_ID = "Profile ID"
TASK_NAME = 'task name'
TASK_DESCRIPTION = 'task description'
LIKE = False


# User Example Data
TEST_USER_TOKEN = 'ABC123'
TEST_PROFILE = {
    NAME: 'John Smith',
    GOALS: ['cs hw2', 'fin hw3'],
    GROUPS: ['cs', 'fin'],
    PRIVATE: False
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
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
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
        user_id = request.args[PROFILE_ID]
        profile = pf.get_profile(user_id)
        return profile


new_profile_field = api.model('NewProfile', {
    pf.NAME: fields.String,
    pf.GOALS: fields.List(fields.String()),
    pf.GROUPS: fields.List(fields.String()),
    pf.PRIVATE: fields.Boolean
})


@api.route(f'{CREATEPROFILE_EP}', methods=['POST'])
@api.expect(new_profile_field)
class CreateProfile(Resource):
    """
    This class will save user profile and return save status
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def post(self):
        name = request.json[pf.NAME]
        goals = request.json[pf.GOALS]
        private = request.json[pf.PRIVATE]
        groups = request.json[pf.GROUPS]
        try:
            new_id = pf.add_profile(name, goals, private, groups)
            if new_id is None:
                raise wz.ServiceUnavailable('We have a technical problem.')
            return {PROFILE_ID: new_id}
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


@api.route(f'{REMOVEPROFILE_EP}', methods=['POST'])
class RemoveProfile(Resource):
    """
    This class will remove user profile and return remove status
    """
    def post(self):
        profile_id = request.json[pf.MOCK_ID]
        try:
            pf.del_profile(profile_id)
            return {MESSAGE_RESP: 'YOU HAVE SUCCESSFULLY REMOVED YOUR PROFILE'}
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


@api.route(f'{VIEWTASKS_EP}', methods=['GET'])
class ViewTasks(Resource):
    """
    This class will show tasks for the user profile
    """
    def get(self):
        # return jsonify(tasks.get_tasks())
        return {
            TASKS: tasks.get_tasks()
        }


@api.route(f'{PROFILEVALIDATION_EP}', methods=['GET'])
class ProfileValidation(Resource):
    """
    This class validates the user profile
    """
    def get(self):
        return {
            PROFILE_VALID_RESP: True
        }


new_task_field = api.model('NewTask', {
    tasks.USER_ID: fields.String,
    tasks.TITLE: fields.String,
    tasks.CONTENT: fields.String
})


@api.route(f'{POSTTASK_EP}', methods=['POST'])
@api.expect(new_task_field)
@api.response(HTTPStatus.OK, 'Success')
@api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
class PostTask(Resource):
    """
    This class is for posting task
    """
    # def post(self):
    #     data = request.get_json()
    #     print(data['username'])
    #     return {
    #         TASK_RESP: TEST_TASK,
    #         USERNAME_RESP: data[USERNAME_RESP]
    #     }
    def post(self):
        user_id = request.json[tasks.USER_ID]
        title = request.json[tasks.TITLE]
        content = request.json[tasks.CONTENT]
        try:
            new_id = tasks.add_task(user_id, title, content)
            if new_id is None:
                raise wz.ServiceUnavailable('Error')
            return {TASK_ID: new_id}
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


@api.route(f'{VIEWGOALS_EP}', methods=['GET'])
class ViewGoals(Resource):
    """
    This class shows goals on the user profile.
    """
    def get(self):
        return {
            GOALS: pf.get_goals()
        }


@api.route(f'{POSTGOAL_EP}', methods=['POST'])
class PostGoal(Resource):
    """
    This class posts goals to user profile.
    """
    def post(self):
        id = request.json[pf.MOCK_ID]
        goals = request.json[pf.GOALS]
        try:
            addGoal = pf.add_goal(id, goals)
            if addGoal is False:
                raise wz.ServiceUnavailable('Error')
            return {GOALS: addGoal}
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


@api.route(f'{DELETEGOAL_EP}', methods=['POST'])
class DeleteGoal(Resource):
    """
    This class deletes goals from user profile.
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
            GROUPS: pf.get_groups()
        }


@api.route(f'{POSTGROUP_EP}', methods=['POST'])
class PostGroup(Resource):
    """
    This class posts group to the user profile.
    """
    # def post(self):
    #     data = request.get_json()
    #     print(data['username'])
    #     return {
    #         GROUP_RESP: TEST_TASK,
    #         USERNAME_RESP: data[USERNAME_RESP]
    #     }
    def post(self):
        id = request.json.get(pf.MOCK_ID, None)
        groups = request.json.get(pf.GROUPS, None)
        try:
            id = pf.add_group(id, groups)
            if id is None:
                raise wz.ServiceUnavailable('Error')
            return {
                MESSAGE_RESP: 'YOU HAVE SUCCESSFULLY ADDED GROUP TO PROFILE'
            }
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


@api.route(f'{DELETEGROUP_EP}', methods=['POST'])
class DeleteGroup(Resource):
    """
    This class deletes group of the user profile.
    """
    def post(self):
        data = request.get_json()
        print(data['username'])
        return {
            GROUP_RESP: TEST_TASK,
            USERNAME_RESP: data[USERNAME_RESP]
        }


like_task_field = api.model('LikeTask', {
    tasks.ID: fields.String,
    tasks.USER_ID: fields.String,
})


@api.route(f'{LIKETASK_EP}', methods=['POST'])
@api.expect(like_task_field)
@api.response(HTTPStatus.OK, 'Success')
@api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
class LikeTask(Resource):
    """
    This class likes the taks under user's task lists
    """
    def post(self):
        task_id = request.json[tasks.ID]
        user_id = request.json[tasks.USER_ID]
        try:
            tasks.like_task(task_id, user_id)
            return {
                MESSAGE_RESP: 'YOU HAVE SUCCESSFULLY LIKED THE TASK'
            }
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


@api.route(f'{UNLIKETASK_EP}', methods=['POST'])
@api.expect(like_task_field)
@api.response(HTTPStatus.OK, 'Success')
@api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
class UnlikeTask(Resource):
    """
    This class likes the taks under user's task lists
    """
    def post(self):
        task_id = request.json[tasks.ID]
        user_id = request.json[tasks.USER_ID]
        try:
            tasks.unlike_task(task_id, user_id)
            return {
                MESSAGE_RESP: 'YOU HAVE SUCCESSFULLY UNLIKED THE TASK'
            }
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')
