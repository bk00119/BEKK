"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""
from http import HTTPStatus
from flask import Flask, request
from flask_restx import Resource, Api, fields
from db import profiles as pf
from db import tasks as tasks
from db import users as users
from db import goals as gls
# from db import posts as psts # delete this line after blueprint testing
import werkzeug.exceptions as wz
# from bson.objectid import ObjectId
# import db.db as db
from flask_cors import CORS
# from apis import api


app = Flask(__name__)
CORS(app)
api = Api(app)

# COMMON KEYWORDS
CREATE = 'create'
USER = 'User'
VIEW = 'view'
DELETE = 'delete'
TASKS = 'Tasks'
TASK = 'Task'
GOALS = 'Goals'
GOAL = 'Goal'
PUBLIC = 'Public'
LIKE = 'like'
UNLIKE = 'unlike'

# Endpoints
LOGIN_EP = '/login'
LOGOUT_EP = '/logout'
SIGNUP_EP = '/signup'
PROTECTED_EP = '/protected'
VIEWUSERPUBLIC_EP = f'/{VIEW}/{USER}/{PUBLIC}'
VIEWUSERTASKS_EP = f'/{VIEW}/{USER}/{TASKS}'
VIEWTASKS_EP = f'/{VIEW}/{TASKS}'
CREATETASK_EP = f'/{CREATE}/{TASK}'
VIEWUSERGOALS_EP = f'/{VIEW}/{USER}/{GOALS}'
SETUSERGOAL_EP = f'/set/{USER}/{GOAL}'
DELETEGOAL_EP = f'/{DELETE}/{GOAL}'
LIKETASK_EP = f'/{LIKE}/{TASK}'
UNLIKETASK_EP = f'/{UNLIKE}/{TASK}'
# CREATEPOST_EP = '/createPost' # delete this line after blueprint testing

# these endpoints are subject to deletion
PROFILE_EP = '/profile'
VIEWPROFILE_EP = '/viewProfile'
CREATEPROFILE_EP = '/createProfile'
REMOVEPROFILE_EP = '/removeProfile'
VIEWPROFILEGROUPS_EP = '/viewProfileGroups'
ADDGROUP_EP = '/addGroup'
DELETEGROUP_EP = '/deleteGroup'
PROFILEVALIDATION_EP = '/profilevalidation'

# Responses
TOKEN_RESP = 'token'  # REMOVE IT AFTER DEVELOPING SIGNUP()
REFRESH_TOKEN_RESP = 'refresh_token'
ACCESS_TOKEN_RESP = 'access_token'
USERNAME_RESP = 'username'
PASSWORD_RESP = 'password'
PROFILE_VALID_RESP = "profilevalidation"
TASK_RESP = 'task'
MESSAGE_RESP = 'message'
GOAL_RESP = 'goal'
GROUP_RESP = 'group'
LIKE_RESP = 'liked'
UNLIKE_RESP = 'unliked'
USER_RESP = 'user'


NAME = 'Name'
GOALS = 'Goals'
GROUPS = 'Groups'
PRIVATE = "Private"

TASKS = 'Tasks'
TASK_ID = 'Task ID'
USER_ID = 'User ID'
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


new_user_id_field = api.model("User", {
    users.ID: fields.String
})


@api.route(f'{VIEWUSERPUBLIC_EP}', methods=['POST'])
@api.expect(new_user_id_field)
@api.response(HTTPStatus.OK, 'Success')
@api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
class ViewUserPublic(Resource):
    """
    This class supports fetching a user data for public
    """
    def post(self):
        """
        posts the user data for login
        """
        user_id = request.json[users.ID]
        try:
            return users.get_user_public(user_id)
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


@api.route(f'{PROTECTED_EP}', methods=['OPTIONS'])
class Protected(Resource):
    """
    This class verifies the user with its access token
    """
    def options(self):
        """
        gets the user's access token for authentication
        """
        access_token = request.cookies.get('access_token')
        print("ACCESS: ", access_token)
        # return ValueError('Missing access token')

        # if not access_token:
        #   return ValueError('Missing access token')

        # try:
        #     payload = jwt.decode(access_token,
        # auth.SECRET_KEY, algorithms=['HS256'])
        #     user_id = payload['user_id']
        #     print('USER ID: ', user_id)
        #     return {'message': f'Access granted to {user_id}'}

        # except jwt.ExpiredSignatureError:
        #     return ValueError('Access token expired')

        # except jwt.InvalidTokenError:
        #     return ValueError('Invalid access token')
        return {
            'test': 'YOU HAVE SUCCESSFULLY LOGGED OUT'
        }


user_login_field = api.model("User", {
    users.EMAIL: fields.String,
    users.PASSWORD: fields.String
})


@api.route(f'{LOGIN_EP}', methods=['POST'])
@api.expect(user_login_field)
@api.response(HTTPStatus.OK, 'Success')
@api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
class Login(Resource):
    """
    This class supports fetching a user data for login
    """
    def post(self):
        """
        posts the user data for login
        """
        data = request.get_json()
        try:
            return users.login(data)
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')
        # return {
        #     TOKEN_RESP: TEST_USER_TOKEN
        # }


@api.route(f'{LOGOUT_EP}', methods=['POST'])
class Logout(Resource):
    """
    This class supports fetching a user data for logout
    """
    def post(self):
        """
        posts the user data for logout
        """
        return {
            MESSAGE_RESP: 'YOU HAVE SUCCESSFULLY LOGGED OUT'
        }


# @api.route(f'{SIGNUP_EP}', methods=['POST'])
# class Signup(Resource):
#     """
#     This class supports fetching a user data for signup
#     """
#     @api.response(HTTPStatus.OK, 'Success')
#     @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
#     def post(self):
#         data = request.get_json()
#         print(data['username'])
#         return {
#             TOKEN_RESP: TEST_USER_TOKEN,
#             USERNAME_RESP: data[USERNAME_RESP]
#         }


profile_id = api.model("Profile", {
    PROFILE_ID: fields.String
})


@api.route(f'{PROFILE_EP}', methods=['POST'])
@api.expect(profile_id)
@api.response(HTTPStatus.OK, 'Success')
@api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
class Profile(Resource):
    """
    This class will deliver contents for any user profile.
    """
    def post(self):
        """
        posts the user's id for fetching user's profile data
        """
        user_id = request.json[PROFILE_ID]
        try:
            profile = pf.get_profile(user_id)
            if profile is None:
                raise wz.ServiceUnavailable('We have a technical problem.')
            return profile
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


new_profile_field = api.model('NewProfile', {
    pf.NAME: fields.String,
    pf.GOALS: fields.List(fields.String()),
    pf.TASKS: fields.List(fields.String()),
    pf.POSTS: fields.List(fields.String()),
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
        """
        posts the user's profile data for creating a new user profile
        """
        name = request.json[pf.NAME]
        goals = request.json[pf.GOALS]
        tasks = request.json[pf.TASKS]
        posts = request.json[pf.POSTS]
        private = request.json[pf.PRIVATE]
        try:
            new_id = pf.add_profile(name, goals, tasks, posts, private)
            if new_id is None:
                raise wz.ServiceUnavailable('We have a technical problem.')
            return {PROFILE_ID: new_id}
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


del_profile_field = api.model('RemoveProfile', {
    pf.MOCK_ID: fields.String
})


@api.route(f'{REMOVEPROFILE_EP}', methods=['POST'])
@api.expect(del_profile_field)
@api.response(HTTPStatus.OK, 'Success')
@api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
class RemoveProfile(Resource):
    """
    This class will remove user profile and return remove status
    """
    def post(self):
        """
        posts the user's id for deleting the user's profile
        """
        profile_id = request.json[pf.MOCK_ID]
        try:
            pf.del_profile(profile_id)
            return {MESSAGE_RESP: 'YOU HAVE SUCCESSFULLY REMOVED YOUR PROFILE'}
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


# =====================Task Endpoint START=====================

@api.route(f'{VIEWTASKS_EP}', methods=['GET', 'POST'])
class ViewTasks(Resource):
    """
    Admin can view all tasks here
    """
    def get(self):
        """
        View all tasks globally
        """
        return {
            TASKS: tasks.get_tasks()
        }


@api.route(f'{VIEWUSERTASKS_EP}/<code>', methods=['GET'])
class ViewUserTasks(Resource):
    """
    View a single User's Tasks
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def get(self, code):
        try:
            return {
                TASKS: tasks.get_user_tasks(code)
            }
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


new_task_field = api.model('NewTask', {
    tasks.USER_ID: fields.String,
    tasks.GOAL_ID: fields.String,
    tasks.IS_COMPLETED: fields.Boolean,
    tasks.CONTENT: fields.String,
})


@api.route(f'{CREATETASK_EP}', methods=['POST'])
@api.expect(new_task_field)
@api.response(HTTPStatus.OK, 'Success')
@api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
class PostTask(Resource):
    """
    This class is for posting task
    """
    def post(self):
        """
        Allows user to create a new task
        (session management in needed to prevent
        this ep from creating tasks for other users)
        """
        user_id = request.json[tasks.USER_ID]
        goal = request.json[tasks.GOAL_ID]
        is_completed = request.json[tasks.IS_COMPLETED]
        content = request.json[tasks.CONTENT]
        try:
            new_id = tasks.add_task(user_id, goal, is_completed, content)
            if new_id is None:
                raise wz.ServiceUnavailable('Error')
            return {TASK_ID: new_id}
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


# =====================Task Endpoint END=====================


user_goals_field = api.model('UserGoals', {
    gls.USER_ID: fields.String,
})


@api.route(f'{VIEWUSERGOALS_EP}', methods=['POST'])
@api.expect(user_goals_field)
@api.response(HTTPStatus.OK, 'Success')
@api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
class ViewUserGoals(Resource):
    """
    This class shows user's goals based on user_id.
    """
    def post(self):
        """
        gets all the goals of a user based on user_id
        """
        user_id = request.json[gls.USER_ID]
        try:
            return {
                GOALS: gls.get_user_goals(user_id)
            }
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


new_goal_field = api.model('NewGoal', {
    gls.USER_ID: fields.String,
    gls.CONTENT: fields.String,
    gls.IS_COMPLETED: fields.Boolean
})


@api.route(f'{SETUSERGOAL_EP}', methods=['POST'])
@api.expect(new_goal_field)
@api.response(HTTPStatus.OK, 'Success')
@api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
class SetUserGoal(Resource):
    """
    This class posts goals to user profile.
    """
    def post(self):
        """
        posts a new goal data to create a new goal
        """
        user_id = request.json[gls.USER_ID]
        content = request.json[gls.CONTENT]
        is_completed = request.json[gls.IS_COMPLETED]
        try:
            setGoal = gls.set_goal(user_id, content, is_completed)
            if setGoal is False:
                raise wz.ServiceUnavailable('Error')
            return {GOALS: setGoal}
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


# @api.route(f'{DELETEGOAL_EP}', methods=['POST'])
# class DeleteGoal(Resource):
#     """
#     This class deletes goals from user profile.
#     """
#     def post(self):
#         data = request.get_json()
#         print(data['username'])
#         return {
#             GOAL_RESP: TEST_TASK,
#             USERNAME_RESP: data[USERNAME_RESP]
#         }


new_profileGroup_field = api.model('NewGroup', {
    pf.MOCK_ID: fields.String,
})


@api.route(f'{VIEWPROFILEGROUPS_EP}', methods=['POST'])
@api.expect(new_profileGroup_field)
@api.response(HTTPStatus.OK, 'Success')
@api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
class ViewProfileGroup(Resource):
    """
    This class shows the groups for each user.
    """
    def post(self):
        """
        posts a user's id to get the user's profile groups
        """
        user_id = request.json[pf.MOCK_ID]
        return {
            GROUPS: pf.get_groups(str(user_id))
        }


new_group_field = api.model('NewGroup', {
    pf.MOCK_ID: fields.String,
    pf.GROUP: fields.String
})


@api.route(f'{ADDGROUP_EP}', methods=['POST'])
@api.expect(new_group_field)
@api.response(HTTPStatus.OK, 'Success')
@api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
class AddGroup(Resource):
    """
    This class posts group to the user profile.
    """
    def post(self):
        """
        posts a new group data to create a new group
        """
        id = request.json.get(pf.MOCK_ID, None)
        # groups = request.json.get(pf.GROUPS, None)
        group = request.json.get(pf.GROUP, None)
        try:
            id = pf.add_group(id, group)
            # if id is None:
            #     raise wz.ServiceUnavailable('Error')
            return {
                MESSAGE_RESP: 'YOU HAVE SUCCESSFULLY ADDED GROUP TO PROFILE'
            }
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')
# @api.route(f'{DELETEGROUP_EP}', methods=['POST'])
# class DeleteGroup(Resource):
#     """
#     This class deletes group of the user profile.
#     """
#     def post(self):
#         data = request.get_json()
#         print(data['username'])
#         return {
#             GROUP_RESP: TEST_TASK,
#             USERNAME_RESP: data[USERNAME_RESP]
#         }

# like_task_field = api.model('LikeTask', {
#     tasks.ID: fields.String,
#     tasks.USER_ID: fields.String,
# })


# @api.route(f'{LIKETASK_EP}', methods=['POST'])
# @api.expect(like_task_field)
# @api.response(HTTPStatus.OK, 'Success')
# @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
# class LikeTask(Resource):
#     """
#     This class likes the taks under user's task lists
#     """
#     def post(self):
#         """
#         post a user's id and task id to like a task
#         """
#         task_id = request.json[tasks.ID]
#         user_id = request.json[tasks.USER_ID]
#         try:
#             tasks.like_task(task_id, user_id)
#             return {
#                 MESSAGE_RESP: 'YOU HAVE SUCCESSFULLY LIKED THE TASK'
#             }
#         except ValueError as e:
#             raise wz.NotAcceptable(f'{str(e)}')


# @api.route(f'{UNLIKETASK_EP}', methods=['POST'])
# @api.expect(like_task_field)
# @api.response(HTTPStatus.OK, 'Success')
# @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
# class UnlikeTask(Resource):
#     """
#     This class likes the taks under user's task lists
#     """
#     def post(self):
#         """
#         post a user's id and task id to unlike a task
#         """
#         task_id = request.json[tasks.ID]
#         user_id = request.json[tasks.USER_ID]
#         try:
#             tasks.unlike_task(task_id, user_id)
#             return {
#                 MESSAGE_RESP: 'YOU HAVE SUCCESSFULLY UNLIKED THE TASK'
#             }
#         except ValueError as e:
#             raise wz.NotAcceptable(f'{str(e)}')

# @api.route(f'{PROFILEVALIDATION_EP}', methods=['GET'])
# class ProfileValidation(Resource):
#     """
#     This class validates the user profile
#     """
#     def get(self):
#         """
#         gets the validation of user profile
#         """
#         return {
#             PROFILE_VALID_RESP: True
#         }
