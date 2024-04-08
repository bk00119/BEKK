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
import db.profiles as pf
import db.posts as psts
import db.db_connect as dbc
import db.goals as gls
import db.comments as cmts
import db.auth as auth

import pytest

TEST_CLIENT = ep.app.test_client()

SAMPLE_USER = {
    usrs.USERNAME: 'user1234',
    usrs.PASSWORD: 'pw1234',
    usrs.FIRST_NAME: 'Firstname',
    usrs.LAST_NAME: 'Lastname',
    usrs.EMAIL: 'test@test.com'
}

SAMPLE_PROFILE = {
    ep.NAME: 'John Adams',
    ep.GOALS: ['cs hw2', 'fin hw3'],
    # ep.GROUPS: ['cs', 'fin'],
    ep.PRIVATE: False
}

SAMPLE_TASKS = {
    ep.TASKS: ['task1', 'task2', 'task3']
}

SAMPLE_TASK = {
    ep.TASK_NAME: "SWE",
    ep.TASK_DESCRIPTION: "design project commits",
    ep.LIKE: False
}

SAMPLE_ID = "656e2bdc5168d371dc3916e9" 

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

@pytest.fixture(scope="function")
def test_generate_valid_profile_id():
    """
    checks and generates profile id from profile collections in MongoDB
    """
    assert SAMPLE_ID is not None 
    return {ep.PROFILE_ID : SAMPLE_ID}

def test_get_profile(test_generate_valid_profile_id):
    resp = TEST_CLIENT.post(ep.PROFILE_EP, json=test_generate_valid_profile_id) 
    resp_json = resp.get_json() 
    assert isinstance(resp_json, dict)
    assert resp.status_code == OK 

@patch('db.profiles.add_profile', return_value=pf.MOCK_ID, autospec=True)
def test_create_profile(mock_add):
    resp = TEST_CLIENT.post(ep.CREATEPROFILE_EP, json=pf.get_test_profile()) 
    assert resp.status_code == OK

@patch('db.profiles.add_profile', side_effect=ValueError(), autospec=True)
def test_create_bad_profile(mock_add):
    resp = TEST_CLIENT.post(ep.CREATEPROFILE_EP, json=pf.get_test_profile())
    assert resp.status_code == NOT_ACCEPTABLE
 
@patch('db.users.get_users')
def test_get_users(mock_get_users):
    mock_get_users.return_value = SAMPLE_USER
    users = usrs.get_users()
    assert isinstance(users, dict)
    assert len(users) > 0


# ===================== TASKS TESTS START=====================

# @pytest.mark.skip(reason="this ep does not test server ep")
# @patch('db.tasks.get_tasks')
# def test_get_tasks(mock_get_tasks):
#     mock_get_tasks.return_value = SAMPLE_TASKS
#     tasks = tsks.get_tasks()
#     assert isinstance(tasks, dict)
#     assert len(tasks) > 0   

# add task to database and return the task details passing its own id as a string
@pytest.fixture(scope="function")
def setup_tasks():
    task = { 
        tsks.USER_ID: "6575033f3b89d2b4f309d7af",
        tsks.GOAL_ID: "65d2dd8abe686c2ec340e298", 
        tsks.CONTENT: "test content",
        tsks.IS_COMPLETED: False
    }
    ret = tsks.add_task(task[tsks.USER_ID], task[tsks.GOAL_ID], task[tsks.CONTENT], task[tsks.IS_COMPLETED])
    task[tsks.ID] = str(ret)
    return task

# check if view tasks 
def test_get_viewTasks():
    resp = TEST_CLIENT.get(ep.VIEWTASKS_EP)
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)
    assert ep.TASKS in resp_json
    tasks = resp_json[ep.TASKS]
    assert isinstance(tasks, dict)
    for task_id in tasks:
        assert isinstance(task_id, str)
        assert isinstance(tasks[task_id], dict)


@patch('db.tasks.add_task', return_value=tsks.MOCK_ID, autospec=True)
def test_postTask(mock_add):
    """
    Testing for posting a new task successfully: PostTask.post()
    """
    resp = TEST_CLIENT.post(ep.CREATETASK_EP, json=tsks.get_new_test_task())
    assert resp.status_code == OK
    
@patch('db.tasks.add_task', side_effect=ValueError(), autospec=True)
def test_bad_postTask(mock_add):
    """
    Testing for posting a task with ValueError: PostTask.post()
    """
    resp = TEST_CLIENT.post(ep.CREATETASK_EP, json=tsks.get_new_test_task())
    assert resp.status_code == NOT_ACCEPTABLE
    
@patch('db.tasks.add_task', return_value=None)
def test_postTask_failure(mock_add):
    """
    Testing for posting a task with ValueError: PostTask.post()
    """
    resp = TEST_CLIENT.post(ep.CREATETASK_EP, json=tsks.get_new_test_task())
    assert resp.status_code == SERVICE_UNAVAILABLE


@patch('db.tasks.add_task', return_value=tsks.MOCK_ID, autospec=True)
def test_postTask(mock_add):
    """
    Testing for posting a new task successfully: PostTask.post()
    """
    resp = TEST_CLIENT.post(ep.CREATETASK_EP, json=tsks.get_new_test_task())
    assert resp.status_code == OK


def test_viewUserTask():
    # CREATE TASK 
    new_task = tsks.get_new_test_task()
    test_task_id = str(tsks.add_task(new_task[tsks.USER_ID], new_task[tsks.GOAL_ID], new_task[tsks.CONTENT], new_task[tsks.IS_COMPLETED]))
    
    # CALL EP
    test_user_id = str(new_task[tsks.USER_ID])
    test_access_token = usrs.generate_access_token(test_user_id)
    resp = TEST_CLIENT.post(ep.VIEWUSERTASKS_EP, json={
        tsks.USER_ID: test_user_id,
        auth.ACCESS_TOKEN: test_access_token,
        auth.REFRESH_TOKEN: test_access_token
    })
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)
    assert ep.TASKS in resp_json

    # CLEANUP 
    tsks.del_task(test_task_id)

# ===================== TASKS TESTS END =====================

# ===================== GOALS TESTS START =====================
@pytest.fixture()
def setup_viewGoals():
    usrs.create_user(SAMPLE_USER[ep.USERNAME_RESP], SAMPLE_USER[ep.PASSWORD_RESP])
#     usrs.create_profile(SAMPLE_USER[ep.USERNAME_RESP], SAMPLE_PROFILE[ep.NAME], SAMPLE_PROFILE[ep.GOALS], SAMPLE_PROFILE[ep.GROUPS], SAMPLE_PROFILE[ep.PRIVATE])

def test_viewUserGoals():
    new_goal = gls.get_new_test_goals()
    test_goal_id = str(gls.set_goal(new_goal[gls.USER_ID],new_goal[gls.CONTENT], new_goal[gls.IS_COMPLETED]))
    test_user_id = str(new_goal[gls.USER_ID])
    resp = TEST_CLIENT.post(ep.VIEWUSERGOALS_EP, json={gls.USER_ID: test_user_id})
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)
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
    resp = TEST_CLIENT.post(ep.VIEWCOMMENTS_EP, json={cmts.USER_ID: test_user_id})
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)
    assert ep.COMMENTS in resp_json
    comments = resp_json[ep.COMMENTS]
    assert isinstance(comments, dict)
    for comment_id in comments:
        assert isinstance(comment_id, str)
        assert isinstance(comments[comment_id], dict)
    cmts.delete_comment(test_comment_id)

@patch('db.comments.add_comment', return_value=cmts.MOCK_ID, autospec=True)
def test_addComment(mock_add):
    """
    Testing fo adding a new comment successfully: AddComment.post()
    """
    resp = TEST_CLIENT.post(ep.ADDCOMMENT_EP, json=cmts.get_new_test_comments())
    assert resp.status_code == OK

@patch('db.comments.add_comment', side_effect=ValueError(), autospec=True)
def test_bad_addComment(mock_add):
    """
    Testing for adding a new comment failed: AddComment.post()
    """
    resp = TEST_CLIENT.post(ep.ADDCOMMENT_EP, json=cmts.get_new_test_comments())
    assert resp.status_code == NOT_ACCEPTABLE

# ===================== COMMENTS TESTS END =====================

def test_removeProfile():
    new_profile = pf.get_test_profile()
    test_profile_id = str(pf.add_profile(new_profile[pf.NAME], new_profile[pf.GOALS], new_profile[pf.TASKS], new_profile[pf.POSTS], new_profile[pf.PRIVATE] ))
    resp = TEST_CLIENT.post(ep.REMOVEPROFILE_EP, json={pf.MOCK_ID: test_profile_id})
    assert resp.status_code == OK
    pf.del_profile(test_profile_id)

@pytest.fixture()
def generate_post_fields():
    return {
        psts.USER_ID: '6575033f3b89d2b4f309d7af', 
        psts.IS_COMPLETED: False, 
        psts.CONTENT: "Test Entry", 
        psts.TASK_IDS: [], 
        psts.GOAL_IDS: [], 
        psts.LIKE_IDS: [],
        psts.COMMENT_IDS: [], 
    }   


@patch('db.posts.add_post', return_value=psts.MOCK_ID, autospec=True)
def test_createPost(mock_add):
    # CREATE POST 
    test_post = psts.get_test_post()
    resp = TEST_CLIENT.post(ep.CREATEPOST_EP, json=test_post)
    assert resp.status_code == OK
    
def test_viewPosts(generate_post_fields):
    # create post with user_id 
    # post_id = psts.add_post(**generate_post_fields) # pausing this to prevent overloading database

    # touch endpoint
    user_id = generate_post_fields[psts.USER_ID]
    posts = TEST_CLIENT.get(f'{ep.VIEWPOSTS_EP}/{user_id}')
    posts = posts.get_json()
    
    # validate post created is in retrieved 
    for post_id in posts:
        assert posts[post_id][psts.USER_ID] == user_id

    # delete post (tbd)
    