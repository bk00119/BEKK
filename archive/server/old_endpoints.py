PROFILE_EP = '/profile'
VIEWPROFILE_EP = '/viewProfile'
CREATEPROFILE_EP = '/createProfile'
REMOVEPROFILE_EP = '/removeProfile'
VIEWPROFILEGROUPS_EP = '/viewProfileGroups'
PROFILEVALIDATION_EP = '/profilevalidation'
LIKETASK_EP = '/likeTask'
UNLIKETASK_EP = '/unlikeTask'
PROFILE_VALID_RESP = "profilevalidation"
PROFILE = {
    NAME: 'John Smith',
    GOALS: ['cs hw2', 'fin hw3'],
    PRIVATE: False
}
PROFILE_ID = "Profile ID"
TEST_PROFILE = {
    NAME: 'John Smith',
    GOALS: ['cs hw2', 'fin hw3'],
    PRIVATE: False
}
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
        """
        post a user's id and task id to like a task
        """
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
        """
        post a user's id and task id to unlike a task
        """
        task_id = request.json[tasks.ID]
        user_id = request.json[tasks.USER_ID]
        try:
            tasks.unlike_task(task_id, user_id)
            return {
                MESSAGE_RESP: 'YOU HAVE SUCCESSFULLY UNLIKED THE TASK'
            }
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')

@api.route(f'{PROFILEVALIDATION_EP}', methods=['GET'])
class ProfileValidation(Resource):
    """
    This class validates the user profile
    """
    def get(self):
        """
        gets the validation of user profile
        """
        return {
            PROFILE_VALID_RESP: True
        }


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