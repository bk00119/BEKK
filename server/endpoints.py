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
from db import comments as cmts
from db import auth as auth
from db import posts as psts
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
COMMENTS = "comments"
COMMENT = "comment"
POST = "post"

# Endpoints
LOGIN_EP = '/login'
LOGOUT_EP = '/logout'
SIGNUP_EP = '/signup'
VIEWUSERPUBLIC_EP = f'/{VIEW}/{USER}/{PUBLIC}'
VIEWUSERTASKS_EP = f'/{VIEW}/{USER}/{TASKS}'
VIEWTASKS_EP = f'/{VIEW}/{TASKS}'
CREATETASK_EP = f'/{CREATE}/{TASK}'
VIEWUSERGOALS_EP = f'/{VIEW}/{USER}/{GOALS}'
CREATEUSERGOAL_EP = f'/{CREATE}/{USER}/{GOAL}'
DELETEGOAL_EP = f'/{DELETE}/{GOAL}'
LIKETASK_EP = f'/{LIKE}/{TASK}'
UNLIKETASK_EP = f'/{UNLIKE}/{TASK}'
VIEWCOMMENTS_EP = f'/{VIEW}/{COMMENTS}'
CREATEPOST_EP = f'/{CREATE}/{POST}'
CREATECOMMENT_EP = f'/{COMMENT}/{CREATE}'

# these endpoints are subject to deletion
PROFILE_EP = '/profile'
VIEWPROFILE_EP = '/viewProfile'
CREATEPROFILE_EP = '/createProfile'
REMOVEPROFILE_EP = '/removeProfile'
VIEWPROFILEGROUPS_EP = '/viewProfileGroups'
PROFILEVALIDATION_EP = '/profilevalidation'
# LIKETASK_EP = '/likeTask'
# UNLIKETASK_EP = '/unlikeTask'

# Responses
TOKEN_RESP = 'token'  # REMOVE IT AFTER DEVELOPING SIGNUP()
REFRESH_TOKEN_RESP = 'refresh_token'
ACCESS_TOKEN_RESP = 'access_token'
USERNAME_RESP = 'username'
PASSWORD_RESP = 'password'
EMAIL_RESP = 'email'
FIRST_NAME_RESP = 'first_name'
LAST_NAME_RESP = 'last_name'
PROFILE_VALID_RESP = "profilevalidation"
TASK_RESP = 'task'
ID_RESP = '_id'
MESSAGE_RESP = 'message'
GOAL_RESP = 'goal'
GROUP_RESP = 'group'
LIKE_RESP = 'liked'
UNLIKE_RESP = 'unliked'
USER_RESP = 'user'


NAME = 'Name'
GOALS = 'Goals'
PRIVATE = "Private"
COMMENTS = 'comments'

TASKS = 'Tasks'
TASK_ID = 'Task ID'
USER_ID = 'User ID'
COMMENT_ID = 'Comment ID'
PROFILE = {
    NAME: 'John Smith',
    GOALS: ['cs hw2', 'fin hw3'],
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


user_login_field = api.model("User Login", {
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


user_signup_field = api.model("User Signup", {
    users.EMAIL: fields.String,
    users.PASSWORD: fields.String,
    users.USERNAME: fields.String,
    users.FIRST_NAME: fields.String,
    users.LAST_NAME: fields.String
})


@api.route(f'{SIGNUP_EP}', methods=['POST'])
@api.expect(user_signup_field)
@api.response(HTTPStatus.OK, 'Success')
@api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
class Signup(Resource):
    """
    This class supports fetching a user data for signup
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def post(self):
        """
        posts the user data for signup
        """
        data = request.get_json()
        try:
            return users.signup(data)
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


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


user_task_field = api.model('UserTasks', {
    tasks.USER_ID: fields.String,
    auth.ACCESS_TOKEN: fields.String,
    auth.REFRESH_TOKEN: fields.String
})


@api.route(f'{VIEWUSERTASKS_EP}', methods=['POST'])
@api.expect(user_task_field)
@api.response(HTTPStatus.OK, 'Success')
@api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
class ViewUserTasks(Resource):
    """
    View a single User's Tasks
    """
    def post(self):
        """
        User can view all tasks belonging to themselves/others
        """
        user_id = request.json[tasks.USER_ID]
        access_token = request.json[auth.ACCESS_TOKEN]
        refresh_token = request.json[auth.REFRESH_TOKEN]

        if not access_token:
            return (
                {'error': 'Access token is missing.'},
                HTTPStatus.UNAUTHORIZED
            )

        if not refresh_token:
            return (
                {'error': 'Refresh token is missing.'},
                HTTPStatus.UNAUTHORIZED
            )

        token_user_id = auth.verify_auth_token(access_token, False)['user_id']
        if user_id != token_user_id:
            return (
                {'error': 'Unauthorized to view the user\'s tasks'},
                HTTPStatus.UNAUTHORIZED
            )

        if not auth.verify_auth_token(access_token):
            if not auth.verify_auth_token(refresh_token):
                # USER NEEDS TO RE-LOGIN
                return (
                    {'error': 'Invalid refresh token.'},
                    HTTPStatus.UNAUTHORIZED
                )

            # REGENERATE ACCESS TOKEN
            access_token = users.generate_access_token(user_id)

        try:
            return {
                TASKS: tasks.get_user_tasks(user_id),
                # INCLUDE ORGIGNAL OR REGENERATED TOKEN
                auth.ACCESS_TOKEN: access_token
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

# =====================Goal Endpoint START=====================
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


@api.route(f'{CREATEUSERGOAL_EP}', methods=['POST'])
@api.expect(new_goal_field)
@api.response(HTTPStatus.OK, 'Success')
@api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
class CreateUserGoal(Resource):
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


# =====================Goal Endpoint END=====================

# =====================Comment Endpoint START================


user_comments_field = api.model('UserComments', {
    cmts.USER_ID: fields.String,
    auth.ACCESS_TOKEN: fields.String,
    auth.REFRESH_TOKEN: fields.String
})


@api.route(f'{VIEWCOMMENTS_EP}', methods=['POST'])
@api.expect(user_comments_field)
@api.response(HTTPStatus.OK, 'Success')
@api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
class ViewComments(Resource):
    """
    This class shows user's comments based on user_id.
    """
    def post(self):
        """
        gets all the comments of a user based on user_id
        """
        user_id = request.json[cmts.USER_ID]
        access_token = request.json[auth.ACCESS_TOKEN]
        refresh_token = request.json[auth.REFRESH_TOKEN]

        if not access_token:
            return (
                {'error': 'Access token is missing.'},
                HTTPStatus.UNAUTHORIZED
            )

        if not refresh_token:
            return (
                {'error': 'Refresh token is missing.'},
                HTTPStatus.UNAUTHORIZED
            )

        token_user_id = auth.verify_auth_token(access_token, False)['user_id']
        if user_id != token_user_id:
            return (
                {'error': 'Unauthorized to view the user\'s tasks'},
                HTTPStatus.UNAUTHORIZED
            )

        if not auth.verify_auth_token(access_token):
            if not auth.verify_auth_token(refresh_token):
                # USER NEEDS TO RE-LOGIN
                return (
                    {'error': 'Invalid refresh token.'},
                    HTTPStatus.UNAUTHORIZED
                )

            # REGENERATE ACCESS TOKEN
            access_token = users.generate_access_token(user_id)

        try:
            return {
                COMMENTS: cmts.get_user_comments(user_id),
                auth.ACCESS_TOKEN: access_token
            }
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


added_comment_field = api.model('AddedComment', {
    cmts.USER_ID: fields.String,
    cmts.CONTENT: fields.String,
})


@api.route(f'{CREATECOMMENT_EP}', methods=['POST'])
@api.expect(added_comment_field)
@api.response(HTTPStatus.OK, 'Success')
@api.response(HTTPStatus.NOT_ACCEPTABLE, "Not Acceptable")
@api.response(HTTPStatus.NO_CONTENT, "No Content")
class CreateComment(Resource):
    """
    This class posts a user's comment to a post
    """
    def post(self):
        """
        posts a user's comment under a post and adds to the DB
        """
        user_id = request.json[cmts.USER_ID]
        content = request.json[cmts.CONTENT]
        try:
            new_id = cmts.add_comment(user_id, content)
            if new_id is None:
                raise wz.ServiceUnavailable('Failed to add comment')
            return {COMMENT_ID: new_id}
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


# =====================Comment Endpoint END ================

# ===================== POSTS Endpoint START=====================


new_post_fields = api.model('NewPost', {
        psts.USER_ID: fields.String,
        psts.IS_COMPLETED: fields.Boolean,
        psts.CONTENT: fields.String,
        psts.TASK_IDS: fields.List(fields.String),
        psts.GOAL_IDS: fields.List(fields.String),
    })


@api.route(f'{CREATEPOST_EP}', methods=["POST"])
class CreatePost(Resource):
    """
    Creates a post
    """
    @api.expect(new_post_fields)
    def post(self):
        user_id = request.json[psts.USER_ID]
        is_completed = request.json[psts.IS_COMPLETED]
        content = request.json[psts.CONTENT]
        task_ids = request.json[psts.TASK_IDS]
        goal_ids = request.json[psts.GOAL_IDS]
        like_ids = []
        comment_ids = []

        try:
            new_id = psts.add_post(
                        user_id,
                        is_completed,
                        content,
                        task_ids,
                        goal_ids,
                        like_ids,
                        comment_ids)
            if new_id is None:
                raise wz.ServiceUnavailable('We have a technical problem.')
            return {"POST ID": new_id}
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')
