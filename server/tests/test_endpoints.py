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
    task = { 
        tsks.USER_ID: "6575033f3b89d2b4f309d7af",
        tsks.CONTENT: "test content",
        tsks.IS_COMPLETED: False
    }
    ret = tsks.add_task(task[tsks.USER_ID], task[tsks.CONTENT], task[tsks.IS_COMPLETED])
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
    tsks.del_task(test_task_id)

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

@patch('db.tasks.add_task', side_effect=ValueError(), autospec=True)
def test_bad_postTask(mock_add, setup_task_fields):
    """
    Testing for posting a task with ValueError: PostTask.post()
    """
    # setup new task fields with auth token 
    resp = TEST_CLIENT.post(ep.CREATETASK_EP, json= setup_task_fields)
    assert resp.status_code == NOT_ACCEPTABLE
    
@patch('db.tasks.add_task', return_value=None)
def test_postTask_failure(mock_add, setup_task_fields):
    """
    Testing for posting a task with ValueError: PostTask.post()
    """
   
    # ping endpoint
    resp = TEST_CLIENT.post(ep.CREATETASK_EP, json=setup_task_fields)
    assert resp.status_code == SERVICE_UNAVAILABLE

@patch('db.tasks.add_task', return_value=tsks.MOCK_ID, autospec=True)
def test_postTask(mock_add, setup_task_fields):
    """
    Testing for posting a new task successfully: PostTask.post()
    """
    # ping endpoint
    resp = TEST_CLIENT.post(ep.CREATETASK_EP, json= setup_task_fields)
    assert resp.status_code == OK

# ADD IT ONCE KEVIN'S DONE
# @patch('db.tasks.update_task', return_value=tsks.MOCK_ID, autospec=True)
# def test_updateTask(mock_add, setup_task_fields):
#     """
#     Testing for updating task successfully: UpdateTask.post()
#     """
#     resp = TEST_CLIENT.post(ep.UPDATETASK_EP, json= setup_task_fields)
#     assert resp.status_code == OK
    
def test_delTask(setup_tasks):
    # CREATE TASK
    setup_task = setup_tasks
    test_task_id = setup_task[tsks.ID]

    # Setup Target Fields
    target_fields = {}
    target_fields[tsks.ID] = test_task_id
    target_fields[tsks.USER_ID] = setup_task[tsks.USER_ID]

    # Generate & Attach Access Tokens
    test_access_token = usrs.generate_access_token(test_task_id)
    target_fields[auth.ACCESS_TOKEN] = test_access_token
    target_fields[auth.REFRESH_TOKEN] = test_access_token

    # DEL TASK 
    resp = TEST_CLIENT.post(f'{ep.DELETETASK_EP}', json= target_fields)
    assert resp.status_code == OK

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
    print(resp_json)
    assert ep.GOALS in resp_json
    
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


@pytest.mark.skip(reason= "not using this endpoint") 
def test_deleteGoal():
    resp = TEST_CLIENT.post(ep.DELETEGOAL_EP, json=SAMPLE_USER)
    print(f'{resp=}')
    resp_json = resp.get_json()
    print(f'{resp_json=}')
    assert ep.GOAL_RESP in resp_json
    assert ep.USERNAME_RESP in resp_json

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

@patch('db.comments.add_comment', return_value=cmts.MOCK_ID, autospec=True)
def test_createComment(mock_add):
    """
    Testing fo adding a new comment successfully: AddComment.post()
    """
    resp = TEST_CLIENT.post(ep.CREATECOMMENT_EP, json=cmts.get_new_test_comments())
    assert resp.status_code == OK

@patch('db.comments.add_comment', side_effect=ValueError(), autospec=True)
def test_bad_createComment(mock_add):
    """
    Testing for adding a new comment failed: AddComment.post()
    """
    resp = TEST_CLIENT.post(ep.CREATECOMMENT_EP, json=cmts.get_new_test_comments())
    assert resp.status_code == NOT_ACCEPTABLE

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

def test_viewPosts():
    # create post with user_id
    post_fields = psts.get_test_post()
    post_id = psts.add_post(**post_fields)

     # view & validate all posts belonging to user
    user_id = post_fields[psts.USER_ID]
    posts = TEST_CLIENT.get(f'{ep.VIEWPOSTS_EP}/{user_id}')
    posts = posts.get_json()
    for post_id in posts:
        assert posts[post_id][psts.USER_ID] == user_id

    # view & validate all posts
    posts = TEST_CLIENT.get(f'{ep.VIEWPOSTS_EP}/all')
    posts = posts.get_json()
    assert isinstance(posts, dict)
    for post_id in posts:
        assert isinstance(post_id, str)
        assert isinstance(posts[post_id], dict)

    # delete created post 
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

    
    
