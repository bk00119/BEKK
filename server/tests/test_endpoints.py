#import server.endpoints as ep
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

from unittest.mock import patch

import db.tasks as tsks
import db.users  as usrs
import db.profiles as pf
import db.db_connect as dbc

import pytest

TEST_CLIENT = ep.app.test_client()

SAMPLE_USER = {
    'username': 'user1234',
    'password': 'pw1234'
}

SAMPLE_PROFILE = {
    ep.NAME: 'John Adams',
    ep.GOALS: ['cs hw2', 'fin hw3'],
    ep.GROUPS: ['cs', 'fin'],
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

def test_login():
    resp = TEST_CLIENT.post(ep.LOGIN_EP, json=SAMPLE_USER)
    print(f'{resp=}')
    resp_json = resp.get_json()
    print(f'{resp_json=}')
    assert ep.TOKEN_RESP in resp_json
    
def test_logout():
    resp = TEST_CLIENT.post(ep.LOGOUT_EP, json=SAMPLE_USER)
    print(f'{resp=}')
    resp_json = resp.get_json()
    print(f'{resp_json=}')
    assert ep.MESSAGE_RESP in resp_json

def test_signup():
    resp = TEST_CLIENT.post(ep.SIGNUP_EP, json=SAMPLE_USER)
    print(f'{resp=}')
    resp_json = resp.get_json()
    print(f'{resp_json=}')
    assert ep.TOKEN_RESP in resp_json
    assert ep.USERNAME_RESP in resp_json    

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

# @pytest.mark.skip(reason= "endpoint does not exist yet") 
@patch('db.tasks.get_tasks')
def test_get_tasks(mock_get_tasks):
    mock_get_tasks.return_value = SAMPLE_TASKS
    tasks = tsks.get_tasks()
    assert isinstance(tasks, dict)
    assert len(tasks) > 0

@pytest.fixture()
def setup_tasks():
    tsks.create_task(SAMPLE_TASK[ep.TASK_NAME], SAMPLE_TASK[ep.TASK_DESCRIPTION], SAMPLE_TASK[ep.LIKE])
    tsks.add_tasks(SAMPLE_TASKS[ep.TASKS])

# @pytest.mark.skip(reason="request causes internal server error, please fix this- kevin ng ") 
def test_viewTasks():
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
    resp = TEST_CLIENT.post(ep.POSTTASK_EP, json=tsks.get_new_test_task())
    assert resp.status_code == OK
    
@patch('db.tasks.add_task', side_effect=ValueError(), autospec=True)
def test_bad_postTask(mock_add):
    """
    Testing for posting a task with ValueError: PostTask.post()
    """
    resp = TEST_CLIENT.post(ep.POSTTASK_EP, json=tsks.get_new_test_task())
    assert resp.status_code == NOT_ACCEPTABLE
    
@patch('db.tasks.add_task', return_value=None)
def test_postTask_failure(mock_add):
    """
    Testing for posting a task with ValueError: PostTask.post()
    """
    resp = TEST_CLIENT.post(ep.POSTTASK_EP, json=tsks.get_new_test_task())
    assert resp.status_code == SERVICE_UNAVAILABLE

@pytest.fixture()
def setup_viewGoals():
    usrs.create_user(SAMPLE_USER[ep.USERNAME_RESP], SAMPLE_USER[ep.PASSWORD_RESP])
#     usrs.create_profile(SAMPLE_USER[ep.USERNAME_RESP], SAMPLE_PROFILE[ep.NAME], SAMPLE_PROFILE[ep.GOALS], SAMPLE_PROFILE[ep.GROUPS], SAMPLE_PROFILE[ep.PRIVATE])

def test_viewGoals():
    resp = TEST_CLIENT.get(ep.VIEWGOALS_EP)
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)
    assert ep.GOALS in resp_json
    goals = resp_json[ep.GOALS]
    assert isinstance(goals, dict)
    for goal_id in goals:
        assert isinstance(goal_id, str)
        assert isinstance(goals[goal_id], dict)
    
def test_postGoal():
    resp = TEST_CLIENT.post(ep.POSTGOAL_EP, json=pf.get_new_test_goal())
    assert resp.status_code == OK


def test_deleteGoal():
    resp = TEST_CLIENT.post(ep.DELETEGOAL_EP, json=SAMPLE_USER)
    print(f'{resp=}')
    resp_json = resp.get_json()
    print(f'{resp_json=}')
    assert ep.GOAL_RESP in resp_json
    assert ep.USERNAME_RESP in resp_json


@pytest.fixture()
def setup_viewGroups():
    usrs.create_user(SAMPLE_USER[ep.USERNAME_RESP], SAMPLE_USER[ep.PASSWORD_RESP])
    usrs.create_profile(SAMPLE_USER[ep.USERNAME_RESP], SAMPLE_PROFILE[ep.NAME], SAMPLE_PROFILE[ep.GOALS], SAMPLE_PROFILE[ep.GROUPS], SAMPLE_PROFILE[ep.PRIVATE])  

def test_viewGroups():
    resp = TEST_CLIENT.get(ep.VIEWGROUPS_EP)
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)
    groups = resp_json[ep.GROUPS]
    assert isinstance(groups, list)
    for group in groups:
        assert isinstance(group, list)

@pytest.fixture()
def setup_deleteGroup():
    usrs.delete_group(SAMPLE_USER[ep.USERNAME_RESP], SAMPLE_PROFILE[ep.NAME], SAMPLE_PROFILE[ep.GOALS])

def test_deleteGroup():
    resp = TEST_CLIENT.post(ep.DELETEGROUP_EP, json=SAMPLE_USER)
    print(f'{resp=}')
    resp_json = resp.get_json()
    print(f'{resp_json=}')
    assert ep.GROUP_RESP in resp_json
    assert ep.USERNAME_RESP in resp_json

@patch('db.profiles.add_group', return_value=pf.MOCK_ID, autospec=True)
def test_postGroup(mock_add):
    """
    Testing for posting a new task successfully: PostTask.post()
    """
    resp = TEST_CLIENT.post(ep.POSTGROUP_EP, json=pf.get_goals())
    assert resp.status_code == OK
# def test_postGroup():
#     resp = TEST_CLIENT.post(ep.POSTGROUP_EP, json=SAMPLE_USER)
#     print(f'{resp=}')
#     resp_json = resp.get_json()
#     print(f'{resp_json=}')
#     # assert ep.GROUP_RESP in resp_json
#     assert ep.USERNAME_RESP in resp_json

# REMOVE THIS
@patch('db.tasks.add_task', return_value=tsks.MOCK_ID, autospec=True)
def test_postTask(mock_add):
    """
    Testing for posting a new task successfully: PostTask.post()
    """
    resp = TEST_CLIENT.post(ep.POSTTASK_EP, json=tsks.get_new_test_task())
    assert resp.status_code == OK

def test_likeTask():
    new_task = tsks.get_new_test_task()
    test_task_id = str(tsks.add_task(new_task[tsks.USER_ID], new_task[tsks.TITLE], new_task[tsks.CONTENT]))
    test_user_id = str(dbc.gen_object_id())
    resp = TEST_CLIENT.post(ep.LIKETASK_EP, json={tsks.ID: test_task_id, tsks.USER_ID: test_user_id})
    assert resp.status_code == OK
    tsks.del_task(test_task_id)

def test_unlikeTask():
    new_task = tsks.get_new_test_task()
    test_task_id = str(tsks.add_task(new_task[tsks.USER_ID], new_task[tsks.TITLE], new_task[tsks.CONTENT]))
    test_user_id = str(dbc.gen_object_id())
    tsks.like_task(test_task_id, test_user_id)
    resp = TEST_CLIENT.post(ep.UNLIKETASK_EP, json={tsks.ID: test_task_id, tsks.USER_ID: test_user_id})
    assert resp.status_code == OK
    tsks.del_task(test_task_id)

def test_removeProfile():
    new_profile = pf.get_test_profile()
    test_profile_id = str(pf.add_profile(new_profile[pf.NAME], new_profile[pf.GOALS], new_profile[pf.PRIVATE], new_profile[pf.GROUPS]))
    resp = TEST_CLIENT.post(ep.REMOVEPROFILE_EP, json={pf.MOCK_ID: test_profile_id})
    assert resp.status_code == OK
    pf.del_profile(test_profile_id)


# @pytest.fixture()
# def setup_likeTask():
#     tsks.like_task(SAMPLE_USER[ep.USERNAME_RESP], SAMPLE_TASK[ep.TASK_NAME], SAMPLE_TASK[ep.TASK_DESCRIPTION], SAMPLE_TASK[ep.LIKE])  

# @pytest.fixture()
# def setup_unlikeTask():
#     tsks.unlike_task(SAMPLE_USER[ep.USERNAME_RESP], SAMPLE_TASK[ep.TASK_NAME], SAMPLE_TASK[ep.TASK_DESCRIPTION], SAMPLE_TASK[ep.LIKE])
