#import server as ep
from http.client import (
    OK,
    NOT_FOUND,
    SERVICE_UNAVAILABLE, 
    NOT_ACCEPTABLE, 
    FORBIDDEN, 
    BAD_REQUEST
    )
import sys
sys.path.append("..")
from server import endpoints as ep
from bson.objectid import ObjectId
from unittest.mock import patch

import db.tasks as tsks
import db.users  as usrs
import db.posts as psts
import db.db_connect as dbc
import db.goals as gls
import db.comments as cmts
import db.auth as auth

import pytest

TEST_CLIENT = ep.app.test_client()

SAMPLE_ID = "656e2bdc5168d371dc3916e9"

SAMPLE_USER = {
    usrs.USERNAME: 'user1234',
    usrs.PASSWORD: 'pw1234',
    usrs.FIRST_NAME: 'Firstname',
    usrs.LAST_NAME: 'Lastname',
    usrs.EMAIL: 'test@test.com',
    auth.ACCESS_TOKEN: usrs.generate_access_token(SAMPLE_ID),
    auth.REFRESH_TOKEN: usrs.generate_access_token(SAMPLE_ID)
}


SAMPLE_TASKS = {
    ep.TASKS: ['task1', 'task2', 'task3']
}

SAMPLE_TASK = {
    ep.TASK_NAME: "SWE",
    ep.TASK_DESCRIPTION: "design project commits",
    ep.LIKE: False
}

def test_regenerate_access_token():
    resp = TEST_CLIENT.post(ep.REGENERATE_ACCESS_TOKEN_EP, json=SAMPLE_USER)
    print(f'{resp=}')
    resp_json = resp.get_json()
    print(f'{resp_json=}')
    assert ep.ACCESS_TOKEN_RESP in resp_json

def test_signup():
    resp = TEST_CLIENT.post(ep.SIGNUP_EP, json=SAMPLE_USER)
    print(f'{resp=}')
    resp_json = resp.get_json()
    print(f'{resp_json=}')
    assert ep.MESSAGE_RESP in resp_json
    assert ep.ACCESS_TOKEN_RESP in resp_json
    assert ep.REFRESH_TOKEN_RESP in resp_json
    assert ep.EMAIL_RESP in resp_json
    assert ep.ID_RESP in resp_json
    assert ep.USERNAME_RESP in resp_json
    assert ep.FIRST_NAME_RESP in resp_json
    assert ep.LAST_NAME_RESP in resp_json
    usrs.remove(resp_json[usrs.ID])

def test_login():
    # CREATE A TEMP USER
    signup_resp = TEST_CLIENT.post(ep.SIGNUP_EP, json=SAMPLE_USER)
    signup_resp_json = signup_resp.get_json()
    user_id = signup_resp_json[usrs.ID]

    resp = TEST_CLIENT.post(ep.LOGIN_EP, json=SAMPLE_USER)
    print(f'{resp=}')
    resp_json = resp.get_json()
    print(f'{resp_json=}')
    assert ep.REFRESH_TOKEN_RESP in resp_json
    assert ep.ACCESS_TOKEN_RESP in resp_json
    
    # REMOVE THE USER
    usrs.remove(user_id)

 
@patch('db.users.get_users')
def test_get_users(mock_get_users):
    mock_get_users.return_value = SAMPLE_USER
    users = usrs.get_users()
    assert isinstance(users, dict)
    assert len(users) > 0


# ===================== TASKS TESTS START=====================

@pytest.fixture(scope="function")
def setup_tasks():
    goal = gls.get_new_test_goals()
    goal_id = gls.set_goal(goal[gls.USER_ID], goal[gls.CONTENT], goal[gls.IS_COMPLETED])
    task = { 
        tsks.USER_ID: "6575033f3b89d2b4f309d7af",
        tsks.GOAL_ID: goal_id,
        tsks.CONTENT: "test content",
        tsks.IS_COMPLETED: False
    }
    ret = tsks.add_task(task[tsks.USER_ID], task[tsks.GOAL_ID], task[tsks.CONTENT], task[tsks.IS_COMPLETED])
    task[tsks.ID] = str(ret)
    return task

# UPDATE ONCE KEVIN IS DONE
# @pytest.fixture(scope="function")
# def update_tasks():
#     task = {
#         tsks.ID: "",
#         tsks.USER_ID: "6575033f3b89d2b4f309d7af",
#         tsks.GOAL_ID: "65d2dd8abe686c2ec340e298", 
#         tsks.CONTENT: "test content",
#         tsks.IS_COMPLETED: False
#     }
#     ret = tsks.add_task(task[tsks.USER_ID], task[tsks.GOAL_ID], task[tsks.CONTENT], task[tsks.IS_COMPLETED])
#     task[tsks.ID] = str(ret)
#     return task

def test_viewUserTask(setup_tasks):
    # CREATE TASK 
    setup = setup_tasks
    test_task_id = setup[tsks.ID]

    # CALL ENDPOINT
    test_user_id = setup[tsks.USER_ID] # user id of the created task 
    test_access_token = usrs.generate_access_token(test_user_id) 
    resp = TEST_CLIENT.post(ep.VIEWUSERTASKS_EP, json={ 
        tsks.USER_ID: test_user_id,
        auth.ACCESS_TOKEN: test_access_token,
        auth.REFRESH_TOKEN: test_access_token
    })

    # TEST RESP 
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)
    assert ep.TASKS in resp_json

    # CLEANUP 
    tsks.del_task(test_task_id, setup[tsks.GOAL_ID])
    gls.delete_set_goal(setup[tsks.GOAL_ID])

@pytest.fixture(scope="function")
def setup_task_fields():
    new_task = tsks.get_new_test_task()
    new_task_user_id = new_task[tsks.USER_ID]
    test_access_token = usrs.generate_access_token(new_task_user_id) 
    new_task[auth.ACCESS_TOKEN] = test_access_token
    new_task[auth.REFRESH_TOKEN] = test_access_token
    return new_task

@patch('db.tasks.add_task', return_value=tsks.MOCK_ID, autospec=True)
def test_postTask(mock_add, setup_task_fields):
    """
    Testing for posting a new task successfully: PostTask.post()
    """
    resp = TEST_CLIENT.post(ep.CREATETASK_EP, json= setup_task_fields)
    assert resp.status_code == OK
    gls.delete_set_goal(setup_task_fields[tsks.GOAL_ID])

@patch('db.tasks.add_task', side_effect=ValueError(), autospec=True)
def test_bad_postTask(mock_add, setup_task_fields):
    """
    Testing for posting a task with ValueError: PostTask.post()
    """
    # setup new task fields with auth token 
    resp = TEST_CLIENT.post(ep.CREATETASK_EP, json= setup_task_fields)
    assert resp.status_code == NOT_ACCEPTABLE
    gls.delete_set_goal(setup_task_fields[tsks.GOAL_ID])
    
@patch('db.tasks.add_task', return_value=None)
def test_postTask_failure(mock_add, setup_task_fields):
    """
    Testing for posting a task with ValueError: PostTask.post()
    """
   
    # ping endpoint
    resp = TEST_CLIENT.post(ep.CREATETASK_EP, json=setup_task_fields)
    assert resp.status_code == SERVICE_UNAVAILABLE
    gls.delete_set_goal(setup_task_fields[tsks.GOAL_ID])

@patch('db.tasks.add_task', return_value=tsks.MOCK_ID, autospec=True)
def test_postTask(mock_add, setup_task_fields):
    """
    Testing for posting a new task successfully: PostTask.post()
    """
    # ping endpoint
    resp = TEST_CLIENT.post(ep.CREATETASK_EP, json= setup_task_fields)
    assert resp.status_code == OK
    gls.delete_set_goal(setup_task_fields[tsks.GOAL_ID])

# @patch('db.tasks.update_task', return_value=tsks.MOCK_ID, autospec=True)
# def test_updateTask(mock_add, setup_task_fields):
#     """
#     Testing for updating task successfully: UpdateTask.post()
#     """
#     # 1) Create a new task first
#     resp = TEST_CLIENT.post(ep.CREATETASK_EP, json= setup_task_fields)
#     assert resp.status_code == OK
#     assert ep.TASK_ID in resp
#     task_id = resp[ep.TASK_ID]
#     # 2) Update the task
#     field = {
#         tsks.ID: task_id,
#         tsks.USER_ID: 
#     }
#     tasks.ID: fields.String,
#     tasks.USER_ID: fields.String,
#     tasks.CONTENT: fields.String,
#     tasks.IS_COMPLETED: fields.Boolean,
#     auth.ACCESS_TOKEN: fields.String,
#     auth.REFRESH_TOKEN: fields.String,

#     resp = TEST_CLIENT.post(ep.UPDATETASK_EP, json= setup_task_fields)
#     assert resp.status_code == OK
    
def test_delTask(setup_tasks):
    # CREATE TASK
    setup_task = setup_tasks
    test_task_id = setup_task[tsks.ID]

    # Setup Target Fields
    target_fields = {}
    target_fields[tsks.ID] = test_task_id
    target_fields[tsks.GOAL_ID] = setup_task[tsks.GOAL_ID]
    target_fields[tsks.USER_ID] = setup_task[tsks.USER_ID]

    # Generate & Attach Access Tokens
    test_access_token = usrs.generate_access_token(setup_task[tsks.USER_ID])
    target_fields[auth.ACCESS_TOKEN] = test_access_token
    target_fields[auth.REFRESH_TOKEN] = test_access_token

    # ADD TASK TO GOAL FIRST
    gls.add_task_to_goal(target_fields[tsks.GOAL_ID], target_fields[tsks.ID])
    # DEL TASK 
    resp = TEST_CLIENT.post(f'{ep.DELETETASK_EP}', json= target_fields)
    assert resp.status_code == OK

    # DEL GOAL
    gls.delete_set_goal(setup_task[tsks.GOAL_ID])

    # TEST DELETION WAS SUCCESSFUL
    assert tsks.id_exists(test_task_id) == None
    


# ===================== TASKS TESTS END =====================

# ===================== GOALS TESTS START =====================
@pytest.fixture()
def setup_viewGoals():
    usrs.create_user(SAMPLE_USER[ep.USERNAME_RESP], SAMPLE_USER[ep.PASSWORD_RESP])

def test_viewUserGoals():
    new_goal = gls.get_new_test_goals()
    test_goal_id = str(gls.set_goal(new_goal[gls.USER_ID],new_goal[gls.CONTENT], new_goal[gls.IS_COMPLETED]))
    test_user_id = str(new_goal[gls.USER_ID])
    test_access_token = usrs.generate_access_token(test_user_id)
    resp = TEST_CLIENT.post(ep.VIEWUSERGOALS_EP, json={
        gls.USER_ID: test_user_id,
        auth.ACCESS_TOKEN: test_access_token,
        auth.REFRESH_TOKEN: test_access_token
        })
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)
    # assert ep.GOALS in resp_json
    if ep.GOALS in resp_json:
        goals = resp_json[ep.GOALS]
        assert isinstance(goals, dict)
        for goal_id in goals:
            assert isinstance(goal_id, str)
            assert isinstance(goals[goal_id], dict)
        gls.delete_set_goal(test_goal_id)

@pytest.mark.skip(reason= "endpoint not complete")     #TODO
def test_setUserGoal():
    resp = TEST_CLIENT.post(ep.CREATEUSERGOAL_EP, json=gls.USER_ID)
    assert resp.status_code == OK


# @pytest.mark.skip(reason= "not using this endpoint") 
def test_deleteGoal():
    new_goal = gls.get_new_test_goals()
    test_goal_id = str(gls.set_goal(new_goal[gls.USER_ID],new_goal[gls.CONTENT], new_goal[gls.IS_COMPLETED]))
    test_user_id = str(new_goal[gls.USER_ID])
    test_access_token = usrs.generate_access_token(test_user_id)
    test_task_id = str(tsks.add_task(test_user_id, test_goal_id, "test task", False))
    # CHECK IF THE TASK IS ATTACHED TO THE GOAL
    goal_data = gls.get_set_goal(test_goal_id)
    assert gls.TASK_IDS in goal_data
    assert test_task_id in goal_data[gls.TASK_IDS]
    resp = TEST_CLIENT.post(ep.DELETEGOAL_EP, json={
        gls.USER_ID: test_user_id,
        gls.ID: test_goal_id,
        auth.ACCESS_TOKEN: test_access_token,
        auth.REFRESH_TOKEN: test_access_token
        })
    # CHECK IF THE GOAL/TASK IS DELETED
    assert not gls.id_exists(test_goal_id)
    assert not tsks.id_exists(test_task_id)

# ===================== GOALS TESTS END =====================

# ===================== COMMENTS TESTS START =====================

def test_viewUserComments():
    new_comment = cmts.get_new_test_comments()
    test_comment_id = str(cmts.add_comment(new_comment[cmts.USER_ID],new_comment[cmts.CONTENT]))
    
    test_user_id = str(new_comment[cmts.USER_ID])
    # test_access_token = usrs.generate_access_token(test_user_id)
    resp = TEST_CLIENT.post(ep.VIEWUSERCOMMENTS_EP, json={
        cmts.USER_ID: test_user_id,
        # auth.ACCESS_TOKEN: test_access_token,
        # auth.REFRESH_TOKEN: test_access_token
        })
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)
    assert cmts.USERNAME in resp_json
    assert cmts.COMMENTS_COLLECT in resp_json
    # assert ep.COMMENTS in resp_json
    # comments = resp_json[ep.COMMENTS]
    # assert isinstance(comments, dict)
    # for comment_id in comments:
    #     assert isinstance(comment_id, str)
    #     assert isinstance(comments[comment_id], dict)
    cmts.delete_comment(test_comment_id)
    psts.del_post(new_comment[cmts.POST_ID])

@patch('db.comments.add_comment', return_value=cmts.MOCK_ID, autospec=True)
def test_createComment(mock_add):
    """
    Testing fo adding a new comment successfully: AddComment.post()
    """
    comment_data = cmts.get_new_test_comments()
    resp = TEST_CLIENT.post(ep.CREATECOMMENT_EP, json=comment_data)
    assert resp.status_code == OK
    psts.del_post(comment_data[cmts.POST_ID])

@patch('db.comments.add_comment', side_effect=ValueError(), autospec=True)
def test_bad_createComment(mock_add):
    """
    Testing for adding a new comment failed: AddComment.post()
    """
    comment_data = cmts.get_new_test_comments()
    resp = TEST_CLIENT.post(ep.CREATECOMMENT_EP, json=comment_data)
    assert resp.status_code == NOT_ACCEPTABLE
    psts.del_post(comment_data[cmts.POST_ID])

# ===================== COMMENTS TESTS END =====================

@pytest.fixture(scope="function")
def generate_post_fields():
    new_post_fields = psts.get_test_post()
    new_post_id = new_post_fields[psts.USER_ID]
    test_access_token = usrs.generate_access_token(new_post_id) 
    new_post_fields[auth.ACCESS_TOKEN] = test_access_token
    new_post_fields[auth.REFRESH_TOKEN] = test_access_token
    return new_post_fields


@patch('db.posts.add_post', return_value=psts.MOCK_ID, autospec=True)
def test_createPost(mock_add, generate_post_fields):
    # CREATE POST 
    resp = TEST_CLIENT.post(ep.CREATEPOST_EP, json=generate_post_fields)
    assert resp.status_code == OK    

# @pytest.mark.skip(reason= "ACTION REQUIRED: THIS ENDPOINT REPLACES THE ACTUAL DATA TO THE TEST DATA") 
def test_viewPosts():
    # create post with user_id
    post_fields = psts.get_test_post()
    post_id = psts.add_post(**post_fields)
    # print(post_id)

     # view & validate all posts belonging to user
    user_id = post_fields[psts.USER_ID]
    posts = TEST_CLIENT.get(f'{ep.VIEWPOSTS_EP}/{user_id}')
    posts = posts.get_json()
    for each_post_id in posts:
        assert posts[each_post_id][psts.USER_ID] == user_id

    # view & validate all posts
    posts = TEST_CLIENT.get(f'{ep.VIEWPOSTS_EP}/all')
    posts = posts.get_json()
    assert isinstance(posts, dict)
    for each_post_id in posts:
        assert isinstance(each_post_id, str)
        assert isinstance(posts[each_post_id], dict)

    # delete created post -> ERROR CAUSED FROM THIS LINE
    psts.del_post(post_id)


def test_deletePost():
    # CREATE post
    post_fields = psts.get_test_post()
    post_id = psts.add_post(**post_fields)

    # Prep deletion required fields
    target_post = {}
    target_post[psts.ID] = post_id
    user_id = post_fields[psts.USER_ID]
    target_post[psts.USER_ID] = user_id

    # generate & attach AUTH fields
    test_access_token = usrs.generate_access_token(user_id) 
    target_post[auth.ACCESS_TOKEN] = test_access_token
    target_post[auth.REFRESH_TOKEN] = test_access_token

    # DELETE post
    resp = TEST_CLIENT.post(f'{ep.DELETEPOST_EP}', json= target_post)
    assert resp.status_code == OK

    # Check if the post is actually deleted
    deleted_post = psts.fetch_by_post_id(post_id)  # Assuming you have a function to get a post by its id
    assert deleted_post is None  # Assert that the post doesn't exist anymore

def test_likePost():
    new_post = psts.get_test_post()
    test_post_id = str(psts.add_post(new_post[psts.USER_ID], new_post[psts.GOAL_IDS], new_post[psts.CONTENT],
                                     new_post[psts.TASK_IDS], new_post[psts.LIKE_IDS], new_post[psts.COMMENT_IDS]))
    test_user_id = str(dbc.gen_object_id())
    resp = TEST_CLIENT.post(ep.LIKEPOST_EP, json={psts.ID: test_post_id, psts.USER_ID: test_user_id})
    assert resp.status_code == OK
    psts.del_post(test_post_id)

def test_unlikePost():
    new_post = psts.get_test_post()
    test_post_id = str(psts.add_post(new_post[psts.USER_ID], new_post[psts.GOAL_IDS], new_post[psts.CONTENT],
                                     new_post[psts.TASK_IDS], new_post[psts.LIKE_IDS], new_post[psts.COMMENT_IDS]))
    test_user_id = str(dbc.gen_object_id())
    psts.like_post(test_post_id, test_user_id)
    resp = TEST_CLIENT.post(ep.UNLIKEPOST_EP, json={psts.ID: test_post_id, psts.USER_ID: test_user_id})
    assert resp.status_code == OK
    psts.del_post(test_post_id)


def test_delete_post_task():
    # create task, goal, and post 
    post_fields = psts.get_test_post()
    user_id = post_fields[psts.USER_ID]
    test_goal_id = gls.set_goal(user_id, "Test Goal", False)
    test_task_id = tsks.add_task(user_id, test_goal_id, "Test Task", False)
    post_fields[psts.TASK_IDS].append(test_task_id) # attach task to post
    post_id = psts.add_post(**post_fields)

    # check that attachment was made 
    with_task_post = psts.fetch_by_post_id(post_id)
    assert test_task_id in with_task_post[psts.TASK_IDS]

    # remove that task_id from the field 
    fields = {}
    fields[psts.ID] = post_id
    fields[psts.USER_ID] = user_id
    test_access_token = usrs.generate_access_token(user_id) 
    fields[auth.ACCESS_TOKEN] = test_access_token
    fields[auth.REFRESH_TOKEN] = test_access_token
    fields[ep.TASK_ID] = test_task_id
    resp = TEST_CLIENT.post(ep.DELETEPOSTTASK_EP, json=fields)

    # retrieve and check task_id is not there 
    without_task_post = psts.fetch_by_post_id(post_id)
    assert test_task_id not in without_task_post[psts.TASK_IDS]

    # cleanup 
    tsks.del_task(test_task_id, test_goal_id)
    gls.delete_set_goal(test_goal_id)
    psts.del_post(post_id)

def test_delete_post_task():
    # create task, goal, and post 
    post_fields = psts.get_test_post()
    user_id = post_fields[psts.USER_ID]
    test_goal_id = gls.set_goal(user_id, "Test Goal", False)
    post_fields[psts.GOAL_IDS].append(test_goal_id)
    post_id = psts.add_post(**post_fields)

    # check that attachment was made 
    with_goal_post = psts.fetch_by_post_id(post_id)
    assert test_goal_id in with_goal_post[psts.GOAL_IDS]

    # remove that task_id from the field 
    fields = {}
    fields[psts.ID] = post_id
    fields[psts.USER_ID] = user_id
    test_access_token = usrs.generate_access_token(user_id) 
    fields[auth.ACCESS_TOKEN] = test_access_token
    fields[auth.REFRESH_TOKEN] = test_access_token
    fields[ep.GOAL_ID] = test_goal_id
    resp = TEST_CLIENT.post(ep.DELETEPOSTGOAL_EP, json=fields)

    # retrieve and check task_id is not there 
    without_goal_post = psts.fetch_by_post_id(post_id)
    assert test_goal_id not in without_goal_post[psts.GOAL_IDS]

    # cleanup 
    gls.delete_set_goal(test_goal_id)
    psts.del_post(post_id)
    