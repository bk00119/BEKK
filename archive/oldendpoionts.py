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
