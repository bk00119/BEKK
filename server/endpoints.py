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
from collections import OrderedDict

app = Flask(__name__)
CORS(app)
api = Api(app)

# COMMON KEYWORDS
CREATE = 'create'
USER = 'user'
VIEW = 'view'
UPDATE = 'update'
DELETE = 'delete'
TASKS = 'tasks'
TASK = 'task'
GOALS = 'goals'
GOAL = 'goal'
PUBLIC = 'public'
LIKE = 'like'
UNLIKE = 'unlike'
COMMENTS = "comments"
COMMENT = "comment"
POST = "post"
POSTS = "posts"
DEVELOPER = "developer"

# Endpoints
# AUTH
REGENERATE_ACCESS_TOKEN_EP = f'/{auth.ACCESS_TOKEN}/regenerate'
LOGIN_EP = '/login'
LOGOUT_EP = '/logout'
SIGNUP_EP = '/signup'
# USER PROFILE
VIEWUSERPUBLIC_EP = f'/{VIEW}/{USER}/{PUBLIC}'
# TASKS
VIEWUSERTASKS_EP = f'/{VIEW}/{USER}/{TASKS}'
CREATETASK_EP = f'/{CREATE}/{TASK}'
UPDATETASK_EP = f'/{UPDATE}/{TASK}'
DELETETASK_EP = f'/{DELETE}/{TASK}'
# GOALS
VIEWUSERGOALS_EP = f'/{VIEW}/{USER}/{GOALS}'
CREATEUSERGOAL_EP = f'/{CREATE}/{USER}/{GOAL}'
DELETEGOAL_EP = f'/{DELETE}/{GOAL}'
# COMMENTS
VIEWUSERCOMMENTS_EP = f'/{VIEW}/{USER}/{COMMENTS}'
VIEWALLPOSTCOMMENTS_EP = f'/{VIEW}/{POST}/{COMMENTS}'
CREATECOMMENT_EP = f'/{COMMENT}/{CREATE}'
# POSTS
CREATEPOST_EP = f'/{CREATE}/{POST}'
VIEWPOSTS_EP = f'/{VIEW}/{POSTS}'
DELETEPOST_EP = f'/{DELETE}/{POST}'
LIKEPOST_EP = f'/{LIKE}/{POST}'
UNLIKEPOST_EP = f'/{UNLIKE}/{POST}'
VIEWALLPOSTLIKES_EP = f'/{VIEW}/{POST}/{LIKE}'
DELETEPOSTTASK_EP = f'/{DELETE}/{POST}/{TASK}'
DELETEPOSTGOAL_EP = f'/{DELETE}/{POST}/{GOAL}'
# DEVELOPER ENDPOINTS
ACCESSLOGS_EP = f'/{DEVELOPER}/access_logs'

# ARCHIVE?
LIKETASK_EP = f'/{LIKE}/{TASK}'
UNLIKETASK_EP = f'/{UNLIKE}/{TASK}'


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
GOAL_ID = 'Goal ID'
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
    users.LAST_NAME: fields.String,
    # users.IS_ADMIN: fields.Boolean
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
        goal = request.json[tasks.GOAL_ID]

        access_token = request.json[auth.ACCESS_TOKEN]
        refresh_token = request.json[auth.REFRESH_TOKEN]
        res = auth.verify(user_id, access_token, refresh_token)
        if res:
            # VERIFICATION ERROR
            return res

        # Create Task
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


updated_task_field = api.model('UpdateTask', {
    tasks.ID: fields.String,
    tasks.GOAL_ID: fields.String,
    tasks.USER_ID: fields.String,
    tasks.CONTENT: fields.String,
    tasks.IS_COMPLETED: fields.Boolean,
    auth.ACCESS_TOKEN: fields.String,
    auth.REFRESH_TOKEN: fields.String,
})


@api.route(f'{UPDATETASK_EP}', methods=['POST'])
@api.expect(updated_task_field)
@api.response(HTTPStatus.OK, 'Success')
@api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
class UpdateTask(Resource):
    """
    This class is for updating an existing task
    """
    def post(self):
        """
        Allows user to create a new task
        (session management in needed to prevent
        this ep from creating tasks for other users)
        """
        tools.log_access(UPDATETASK_EP, request)
        data = request.json
        task_id = data[tasks.ID]
        goal_id = data[tasks.GOAL_ID]
        user_id = data[tasks.USER_ID]
        access_token = data[auth.ACCESS_TOKEN]
        refresh_token = data[auth.REFRESH_TOKEN]

        content = None
        is_completed = None
        # CASE 1: CONTENT IS UPDATED
        if tasks.CONTENT in data:
            content = data[tasks.CONTENT]
        # CASE 2: IS_COMPLETED IS UPDATED
        if tasks.IS_COMPLETED in data:
            is_completed = data[tasks.IS_COMPLETED]

        # VERIFY THE IDENTITY
        res = auth.verify(user_id, access_token, refresh_token)
        if res:
            return res

        try:
            tasks.update_task(task_id, goal_id, content, is_completed)
            return {'message': 'Update task successful'}
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


target_task_field = api.model('TargetTask', {
    tasks.ID: fields.String,
    tasks.GOAL_ID: fields.String,
    tasks.USER_ID: fields.String,
    auth.ACCESS_TOKEN: fields.String,
    auth.REFRESH_TOKEN: fields.String
})


@api.expect(target_task_field)
@api.route(f'{DELETETASK_EP}', methods=['POST'])
class DeleteTask(Resource):
    """
    Delete Specific Post
    """
    @api.response(HTTPStatus.OK, 'Success')
    def post(self):
        # Auth
        user_id = request.json[tasks.USER_ID]
        access_token = request.json[auth.ACCESS_TOKEN]
        refresh_token = request.json[auth.REFRESH_TOKEN]
        res = auth.verify(user_id, access_token, refresh_token)
        if res:
            # VERIFICATION ERROR
            return res

        # Delete Task
        task_id = request.json[tasks.ID]
        goal_id = request.json[tasks.GOAL_ID]
        tasks.del_task(task_id, goal_id)


# =====================Task Endpoint END=====================

# =====================Goal Endpoint START=====================


user_goals_field = api.model('UserGoals', {
    gls.USER_ID: fields.String,
    # gls.ID: fields.String,
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
        # goal_id = request.json[gls.ID]
        access_token = request.json[auth.ACCESS_TOKEN]
        refresh_token = request.json[auth.REFRESH_TOKEN]

        res = auth.verify(user_id, access_token, refresh_token)
        if res:
            return res

        try:
            # gls.get_set_goal()
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
    gls.IS_COMPLETED: fields.Boolean,
    auth.ACCESS_TOKEN: fields.String,
    auth.REFRESH_TOKEN: fields.String
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
        access_token = request.json[auth.ACCESS_TOKEN]
        refresh_token = request.json[auth.REFRESH_TOKEN]
        res = auth.verify(user_id, access_token, refresh_token)
        if res:
            # VERIFICATION ERROR
            return res
        is_completed = request.json[gls.IS_COMPLETED]
        try:
            setGoal = gls.set_goal(user_id, content, is_completed)
            if setGoal is False:
                raise wz.ServiceUnavailable('Error')
            return {GOALS: setGoal}
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


delete_goal_field = api.model('DeleteGoal', {
    gls.USER_ID: fields.String,
    gls.ID: fields.String,
    auth.ACCESS_TOKEN: fields.String,
    auth.REFRESH_TOKEN: fields.String
})


@api.route(f'{DELETEGOAL_EP}', methods=['POST'])
@api.expect(delete_goal_field)
@api.response(HTTPStatus.OK, 'Success')
@api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
class DeleteUserGoal(Resource):
    """
    This class deletes a goal.
    """
    def post(self):
        """
        posts a goal data to delete the  goal
        """
        tools.log_access(CREATEUSERGOAL_EP, request)
        user_id = request.json[gls.USER_ID]
        goal_id = request.json[gls.ID]
        access_token = request.json[auth.ACCESS_TOKEN]
        refresh_token = request.json[auth.REFRESH_TOKEN]
        res = auth.verify(user_id, access_token, refresh_token)
        if res:
            # VERIFICATION ERROR
            return res
        try:
            # 1) FIND TASK_IDS FROM THE GOAL
            goal = gls.get_set_goal(goal_id)
            task_ids = []
            if gls.TASK_IDS in goal and len(goal[gls.TASK_IDS]) > 0:
                task_ids = goal[gls.TASK_IDS]

            # 2) DELETE THE GOAL
            gls.delete_set_goal(goal_id)

            # 3) DELETE THE TASKS
            for task_id in task_ids:
                tasks.del_task(task_id)
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')

# =====================Goal Endpoint END=====================

# =====================Comment Endpoint START================


all_post_comments_field = api.model('AllPostComments', {
    psts.ID: fields.String,
})


@api.route(f'{VIEWALLPOSTCOMMENTS_EP}', methods=['POST'])
@api.expect(all_post_comments_field)
@api.response(HTTPStatus.OK, 'Success')
@api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
class ViewAllPostComments(Resource):
    """
    This class shows all comments under a post including usernames
    """
    def post(self):
        """
        gets all the comments under a post
        """
        post = request.json[psts.ID]
        try:
            return cmts.get_post_comments(post)
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


user_comments_field = api.model('UserComments', {
    cmts.USER_ID: fields.String,
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

        try:
            return cmts.get_user_comments(user_id)
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


added_comment_field = api.model('AddedComment', {
    cmts.USER_ID: fields.String,
    cmts.POST_ID: fields.String,
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
        post_id = request.json[cmts.POST_ID]
        content = request.json[cmts.CONTENT]
        try:
            comment_id = cmts.add_comment(user_id, content)
            if comment_id is None:
                raise wz.ServiceUnavailable('Failed to add comment')

            # NEED TO ADD COMMENT ID INTO THE POST'S COMMENT_IDS
            # ADD POST_ID TO THE FIELD
            psts.add_comment(post_id, comment_id)
            return {COMMENT_ID: comment_id}
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


# =====================Comment Endpoint END ================

# ===================== POSTS Endpoint START=====================


new_post_fields = api.model('NewPost', {
        psts.USER_ID: fields.String,
        psts.CONTENT: fields.String,
        psts.TASK_IDS: fields.List(fields.String),
        psts.GOAL_IDS: fields.List(fields.String),
        auth.ACCESS_TOKEN: fields.String,
        auth.REFRESH_TOKEN: fields.String
    })


@api.expect(new_post_fields)
@api.route(f'{CREATEPOST_EP}', methods=["POST"])
class CreatePost(Resource):
    """
    Creates a post
    """
    def post(self):
        # Logging
        tools.log_access(CREATEPOST_EP, request)

        # AUTH
        user_id = request.json[psts.USER_ID]
        access_token = request.json[auth.ACCESS_TOKEN]
        refresh_token = request.json[auth.REFRESH_TOKEN]
        res = auth.verify(user_id, access_token, refresh_token)
        if res:
            return res

        # Request Fields
        content = request.json[psts.CONTENT]
        task_ids = request.json[psts.TASK_IDS]
        goal_ids = request.json[psts.GOAL_IDS]
        like_ids = []
        comment_ids = []

        for goal_id in goal_ids:
            if not gls.id_exists(goal_id):
                raise ValueError(
                    f'Goal ID: {goal_id} does not exist in database'
                )
        for task_id in task_ids:
            if not tasks.id_exists(task_id):
                raise ValueError(
                    f'Task ID: {task_id} does not exist in database'
                )
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

        # Initialize return object
        posts = None

        # Fetch all posts
        if user_id == 'all':
            posts = psts.fetch_all()
        # USER-BASED FETCH FOR POSTS
        else:
            posts = psts.fetch_by_user_id(user_id)

        # Append contents (goals, tasks, comments)
        for post_id in posts:
            # convert goal_ids to goal_obj
            goals_obj = []
            for goal_id in posts[post_id][psts.GOAL_IDS]:
                if gls.id_exists(goal_id):
                    goal = gls.get_set_goal(goal_id)
                    goals_obj.append(goal)
            posts[post_id][GOALS] = goals_obj

            # Convert task_ids to task_obj
            tasks_obj = []
            for task_id in posts[post_id][psts.TASK_IDS]:
                if tasks.id_exists(task_id):
                    task = tasks.get_task(task_id)
                    tasks_obj.append(task)
            posts[post_id][TASKS] = tasks_obj

            # Convert comment ids to comment_obj
            if posts[post_id][psts.COMMENT_IDS]:
                latest_comment_id = posts[post_id][psts.COMMENT_IDS][0]
                comment = cmts.get_comment(latest_comment_id)
                comment_user_id = comment[cmts.USER_ID]
                comment_user = users.get_user_public(comment_user_id)
                comment_user_username = None
                if users.USERNAME in comment_user:
                    comment_user_username = comment_user[users.USERNAME]
                posts[post_id][COMMENTS] = comment
                posts[post_id][COMMENTS][users.USERNAME] \
                    = comment_user_username

        if posts:
            sorted_posts = OrderedDict(sorted(posts.items(),
                                              key=lambda x: x[1]['timestamp'],
                                              reverse=True))
            return sorted_posts
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


delete_post_task_field = api.model('DeletePostTask', {
    psts.ID: fields.String,
    psts.USER_ID: fields.String,
    auth.ACCESS_TOKEN: fields.String,
    auth.REFRESH_TOKEN: fields.String,
    TASK_ID: fields.String
})


@api.route(f'{DELETEPOSTTASK_EP}', methods=['POST'])
@api.expect(delete_post_task_field)
@api.response(HTTPStatus.OK, 'Success')
@api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
class DeletePostTask(Resource):
    """
    This class removes a task from post
    """
    def post(self):
        # AUTH
        user_id = request.json[psts.USER_ID]
        access_token = request.json[auth.ACCESS_TOKEN]
        refresh_token = request.json[auth.REFRESH_TOKEN]
        res = auth.verify(user_id, access_token, refresh_token)
        if res:
            # VERIFICATION ERROR
            return res

        # Get parameters
        post_id = request.json[psts.ID]
        task_id = request.json[TASK_ID]

        # Log
        tools.log_access(DeletePostTask, request)

        try:
            if tasks.id_exists(task_id):
                psts.remove_task(post_id, task_id)
            return {
                MESSAGE_RESP: 'YOU HAVE SUCCESSFULLY DELETED A POST\'S TASK'
            }
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


delete_post_goal_field = api.model('DeletePostGoal', {
    psts.ID: fields.String,
    psts.USER_ID: fields.String,
    auth.ACCESS_TOKEN: fields.String,
    auth.REFRESH_TOKEN: fields.String,
    GOAL_ID: fields.String
})


@api.route(f'{DELETEPOSTGOAL_EP}', methods=['POST'])
@api.expect(delete_post_goal_field)
@api.response(HTTPStatus.OK, 'Success')
@api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
class DeletePostGoal(Resource):
    """
    This class removes a goal from post
    """
    def post(self):
        # AUTH
        user_id = request.json[psts.USER_ID]
        access_token = request.json[auth.ACCESS_TOKEN]
        refresh_token = request.json[auth.REFRESH_TOKEN]
        res = auth.verify(user_id, access_token, refresh_token)
        if res:
            # VERIFICATION ERROR
            return res

        # Get parameters
        post_id = request.json[psts.ID]
        goal_id = request.json[GOAL_ID]

        # Log
        tools.log_access(DeletePostGoal, request)

        try:
            if gls.id_exists(goal_id):
                psts.remove_goal(post_id, goal_id)
            return {
                MESSAGE_RESP: 'YOU HAVE SUCCESSFULLY DELETED A POST\'S GOAL'
            }
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


like_post_field = api.model('LikePost', {
    psts.ID: fields.String,
    psts.USER_ID: fields.String,
})


@api.route(f'{LIKEPOST_EP}', methods=['POST'])
@api.expect(like_post_field)
@api.response(HTTPStatus.OK, 'Success')
@api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
class LikePost(Resource):
    """
    This class likes the taks under user's task lists
    """
    def post(self):
        """
        post a user's id and task id to like a task
        """
        post_id = request.json[psts.ID]
        user_id = request.json[psts.USER_ID]
        try:
            psts.like_post(post_id, user_id)
            return {
                MESSAGE_RESP: 'YOU HAVE SUCCESSFULLY LIKED THE TASK'
            }
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


@api.route(f'{UNLIKEPOST_EP}', methods=['POST'])
@api.expect(like_post_field)
@api.response(HTTPStatus.OK, 'Success')
@api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
class UnlikePost(Resource):
    """
    This class likes the taks under user's task lists
    """
    def post(self):
        """
        post a user's id and task id to unlike a task
        """
        post_id = request.json[psts.ID]
        user_id = request.json[psts.USER_ID]
        try:
            psts.unlike_post(post_id, user_id)
            return {
                MESSAGE_RESP: 'YOU HAVE SUCCESSFULLY UNLIKED THE TASK'
            }
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


all_post_likes_field = api.model('AllPostLikes', {
    psts.ID: fields.String,
})


@api.route(f'{VIEWALLPOSTLIKES_EP}', methods=['POST'])
@api.expect(all_post_likes_field)
@api.response(HTTPStatus.OK, 'Success')
@api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
class ViewAllPostLikes(Resource):
    """
    This class shows all likes under a post including usernames
    """
    def post(self):
        """
        gets all the liked usernames under a post
        """
        post = request.json[psts.ID]
        try:
            return psts.get_post_likes(post)
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')

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
