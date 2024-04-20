"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""
from http import HTTPStatus
from flask import Flask, request
from flask_restx import Resource, Api, fields
from db import tasks as tasks
from db import users as users
from db import goals as gls
from db import comments as cmts
from db import auth as auth
from db import posts as psts
import werkzeug.exceptions as wz
# from bson.objectid import ObjectId
# import db.db as db
from flask_cors import CORS
# from apis import api
import utils.tools as tools

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
POSTS = "posts"
DEVELOPER = "developer"

# Endpoints
REGENERATE_ACCESS_TOKEN_EP = f'/{auth.ACCESS_TOKEN}/regenerate'
LOGIN_EP = '/login'
LOGOUT_EP = '/logout'
SIGNUP_EP = '/signup'
VIEWUSERPUBLIC_EP = f'/{VIEW}/{USER}/{PUBLIC}'
VIEWUSERTASKS_EP = f'/{VIEW}/{USER}/{TASKS}'
VIEWTASKS_EP = f'/{VIEW}/{TASKS}'
CREATETASK_EP = f'/{CREATE}/{TASK}'
DELETETASK_EP = f'/{DELETE}/{TASK}'
VIEWUSERGOALS_EP = f'/{VIEW}/{USER}/{GOALS}'
CREATEUSERGOAL_EP = f'/{CREATE}/{USER}/{GOAL}'
DELETEGOAL_EP = f'/{DELETE}/{GOAL}'
LIKETASK_EP = f'/{LIKE}/{TASK}'
UNLIKETASK_EP = f'/{UNLIKE}/{TASK}'
VIEWUSERCOMMENTS_EP = f'/{VIEW}/{USER}/{COMMENTS}'
CREATEPOST_EP = f'/{CREATE}/{POST}'
VIEWPOSTS_EP = f'/{VIEW}/{POSTS}'
CREATECOMMENT_EP = f'/{COMMENT}/{CREATE}'
DELETEPOST_EP = f'/{DELETE}/{POST}'

# DEVELOPER ENDPOINTS
ACCESSLOGS_EP = f'/{DEVELOPER}/access_logs'


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
TASK_NAME = 'task name'
TASK_DESCRIPTION = 'task description'
LIKE = False


# User Example Data
TEST_USER_TOKEN = 'ABC123'


# Task Example Data
TEST_TASK = {
    TASK_NAME: "SWE",
    TASK_DESCRIPTION: "BEKK final project",
    LIKE: True
}


token_field = api.model("Tokens", {
    auth.ACCESS_TOKEN: fields.String,
    auth.REFRESH_TOKEN: fields.String
})


@api.route(f'{REGENERATE_ACCESS_TOKEN_EP}', methods=['POST'])
@api.expect(token_field)
@api.response(HTTPStatus.OK, 'Success')
@api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
class RegenerateAccessToken(Resource):
    """
    This class supports fetching a user data for login
    """
    def post(self):
        """
        posts the user data for login
        """
        access_token = request.json[auth.ACCESS_TOKEN]
        refresh_token = request.json[auth.REFRESH_TOKEN]
        new_access_token = auth.regenerate_access_token(access_token,
                                                        refresh_token)

        try:
            return {
                # REGENERATED TOKEN
                auth.ACCESS_TOKEN: new_access_token
            }
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


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
        tools.log_access(VIEWUSERPUBLIC_EP, request)
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
        tools.log_access(LOGIN_EP, request)
        data = request.get_json()
        try:
            return users.login(data)
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


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
        tools.log_access(SIGNUP_EP, request)
        data = request.get_json()
        try:
            return users.signup(data)
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


# =====================Task Endpoint START=====================


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
        tools.log_access(VIEWUSERTASKS_EP, request)
        # Auth
        user_id = request.json[tasks.USER_ID]
        access_token = request.json[auth.ACCESS_TOKEN]
        refresh_token = request.json[auth.REFRESH_TOKEN]
        res = auth.verify(user_id, access_token, refresh_token)
        if res:
            # VERIFICATION ERROR
            return res

        # Get User Tasks
        try:
            return {
                TASKS: tasks.get_user_tasks(user_id),
                # INCLUDE THE REGENERATED TOKEN
                auth.ACCESS_TOKEN: access_token
            }
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


new_task_field = api.model('NewTask', {
    tasks.USER_ID: fields.String,
    tasks.GOAL_ID: fields.String,
    tasks.IS_COMPLETED: fields.Boolean,
    tasks.CONTENT: fields.String,
    auth.ACCESS_TOKEN: fields.String,
    auth.REFRESH_TOKEN: fields.String
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
        tools.log_access(CREATETASK_EP, request)
        # Auth
        user_id = request.json[tasks.USER_ID]
        access_token = request.json[auth.ACCESS_TOKEN]
        refresh_token = request.json[auth.REFRESH_TOKEN]
        res = auth.verify(user_id, access_token, refresh_token)
        if res:
            # VERIFICATION ERROR
            return res

        # Create Task
        goal = request.json[tasks.GOAL_ID]
        is_completed = request.json[tasks.IS_COMPLETED]
        content = request.json[tasks.CONTENT]
        try:
            # TASK: user_id, content, is_complete
            new_id = tasks.add_task(user_id, goal, content, is_completed)
            # GOAL: add task_id to tasks[]
            if new_id is None:
                raise wz.ServiceUnavailable('Error')
            return {
                TASK_ID: new_id,
                # INCLUDE THE REGENERATED TOKEN
                auth.ACCESS_TOKEN: access_token
            }
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


token_field = api.model('TargetTask', {
    tasks.ID: fields.String,
    tasks.USER_ID: fields.String,
    auth.ACCESS_TOKEN: fields.String,
    auth.REFRESH_TOKEN: fields.String
})


@api.route(f'{DELETETASK_EP}', methods=['POST'])
class DeleteTask(Resource):
    """
    Delete Specific Post
    """
    @api.response(HTTPStatus.OK, 'Success')
    def post(self):
        # Auth
        user_id = request.json[tasks.ID]
        access_token = request.json[auth.ACCESS_TOKEN]
        refresh_token = request.json[auth.REFRESH_TOKEN]
        res = auth.verify(user_id, access_token, refresh_token)
        if res:
            # VERIFICATION ERROR
            return res

        # Delete Task
        task_id = request.json[tasks.ID]
        tasks.del_task(task_id)


# =====================Task Endpoint END=====================

# =====================Goal Endpoint START=====================


user_goals_field = api.model('UserGoals', {
    gls.USER_ID: fields.String,
    auth.ACCESS_TOKEN: fields.String,
    auth.REFRESH_TOKEN: fields.String
})


@api.route(f'{VIEWUSERGOALS_EP}', methods=['POST'])
@api.expect(user_goals_field)
@api.response(HTTPStatus.OK, 'Success')
@api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
class ViewUserGoals(Resource):
    """
    This class shows a single user's goals
    """
    def post(self):
        """
        gets all the goals of a user based on user_id
        """
        tools.log_access(VIEWUSERGOALS_EP, request)
        user_id = request.json[gls.USER_ID]
        access_token = request.json[auth.ACCESS_TOKEN]
        refresh_token = request.json[auth.REFRESH_TOKEN]

        res = auth.verify(user_id, access_token, refresh_token)
        if res:
            return res

        access_token = auth.regenerate_access_token(access_token,
                                                    refresh_token)

        try:
            data = {
                GOALS: gls.get_user_goals(user_id),
                auth.ACCESS_TOKEN: access_token
            }
            return data
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
        tools.log_access(CREATEUSERGOAL_EP, request)
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


@api.route(f'{VIEWUSERCOMMENTS_EP}', methods=['POST'])
@api.expect(user_comments_field)
@api.response(HTTPStatus.OK, 'Success')
@api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
class ViewUserComments(Resource):
    """
    This class shows user's comments based on user_id.
    """
    def post(self):
        """
        gets all the comments of a user based on user_id
        """
        tools.log_access(VIEWUSERCOMMENTS_EP, request)
        user_id = request.json[cmts.USER_ID]
        access_token = request.json[auth.ACCESS_TOKEN]
        refresh_token = request.json[auth.REFRESH_TOKEN]

        res = auth.verify(user_id, access_token, refresh_token)
        if res:
            return res

        # REGENERATE AN ACCESS TOKEN IF THE TOKEN IS EXPIRED
        # OTHERWISE RETURN THE ORIGINAL ACCESS TOKEN
        access_token = auth.regenerate_access_token(access_token,
                                                    refresh_token)

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
        tools.log_access(CREATECOMMENT_EP, request)
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
        tools.log_access(CREATEPOST_EP, request)
        user_id = request.json[psts.USER_ID]
        content = request.json[psts.CONTENT]
        task_ids = request.json[psts.TASK_IDS]
        goal_ids = request.json[psts.GOAL_IDS]
        like_ids = []
        comment_ids = []

        try:
            new_id = psts.add_post(
                        user_id,
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


@api.route(f'{VIEWPOSTS_EP}/<user_id>', methods=["GET"])
class ViewPosts(Resource):
    """
    View posts by 'all' or users
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Data Not Found')
    def get(self, user_id):
        # GLOBAL FETCH FOR POSTS
        tools.log_access(VIEWPOSTS_EP, request)
        
        # if not user_id:
        if user_id == 'all':
            return psts.fetch_all()

        # USER-BASED FETCH FOR POSTS
        posts = psts.fetch_by_user_id(user_id)
        if posts:
            return posts
        else:
            raise wz.NotFound(f'No posts found with {user_id=}')


post_token_field = api.model('TargetPost', {
    psts.ID: fields.String,
    psts.USER_ID: fields.String,
    auth.ACCESS_TOKEN: fields.String,
    auth.REFRESH_TOKEN: fields.String
})


@api.route(f'{DELETEPOST_EP}', methods=['POST'])
class DeletePost(Resource):
    """
    Delete Specific Post
    """
    @api.response(HTTPStatus.OK, 'Success')
    def post(self):
        # AUTH
        user_id = request.json[psts.USER_ID]
        access_token = request.json[auth.ACCESS_TOKEN]
        refresh_token = request.json[auth.REFRESH_TOKEN]
        res = auth.verify(user_id, access_token, refresh_token)
        if res:
            # VERIFICATION ERROR
            return res

        # Delete Post
        post_id = request.json[psts.ID]
        tools.log_access(DeletePost, request)
        psts.del_post(post_id)

# ===================== POSTS Endpoint END=====================
# ===================== DEVELOPER Endpoint START=====================


developer_data = api.model('DeveloperData', {
    users.EMAIL: fields.String,
    users.PASSWORD: fields.String,
})


@api.route(f'{ACCESSLOGS_EP}', methods=['POST'])
@api.expect(developer_data)
@api.response(HTTPStatus.OK, 'Success')
@api.response(HTTPStatus.NOT_ACCEPTABLE, "Not Acceptable")
@api.response(HTTPStatus.NO_CONTENT, "No Content")
class Get_Access_Logs(Resource):
    """
    Get Access Logs of Endpoints
    """
    @api.response(HTTPStatus.OK, 'Success')
    def post(self):
        tools.log_access(LOGIN_EP, request, True)
        data = request.get_json()

        try:
            if tools.verify_identity(data):
                return tools.get_access_logs()
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')

# ===================== DEVELOPER Endpoint END=====================
