from flask_restx import Namespace, Resource, Api, fields
from flask import request
from db import posts as psts
import werkzeug.exceptions as wz

CREATEPOST_EP = '/createPost'

api = Namespace("posts", description="Post Related Operations")

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
