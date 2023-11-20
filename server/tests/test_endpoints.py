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

import pytest

TEST_CLIENT = ep.app.test_client()

SAMPLE_USER = {
    'username': 'user1234',
    'password': 'pw1234'
}

SAMPLE_PROFILE = {
    ep.NAME: 'John Smith',
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
    this profile id has to always be part of the profiles database
    """
    return "123" 

def test_get_profile(test_generate_valid_profile_id):
    resp = TEST_CLIENT.get(ep.PROFILE_EP, query_string={ep.PROFILE_ID:f'{test_generate_valid_profile_id}'}) 
    resp_json = resp.get_json() 
    assert isinstance(resp_json, dict)
    assert ep.NAME in resp_json 
    assert ep.GROUPS in resp_json 
    assert ep.GOALS in resp_json
    assert ep.PRIVATE in resp_json
    groups = resp_json[ep.GROUPS] 
    goals = resp_json[ep.GOALS] 
    assert isinstance(resp_json[ep.NAME], str)
    assert isinstance(resp_json[ep.PRIVATE], bool)
    assert isinstance(groups, list) 
    assert isinstance(goals, list)
    for group_name in groups:
        assert isinstance(group_name, str) 
    for goal_title in goals:
        assert isinstance(goal_title, str)

@patch('db.profiles.add_profile', return_value=pf.MOCK_ID, autospec=True)
def test_create_profile(mock_add):
    resp = TEST_CLIENT.post(ep.CREATEPROFILE_EP, json=pf.get_test_profile()) 
    assert resp.status_code == OK

@patch('db.profiles.add_profile', side_effect=ValueError(), autospec=True)
def test_create_bad_profile(mock_add):
    resp = TEST_CLIENT.post(ep.CREATEPROFILE_EP, json=pf.get_test_profile())
    assert resp.status_code == NOT_ACCEPTABLE
    
@pytest.mark.skip("endpoint does not exist yet")
def test_modify_profile():
    TEST_CLIENT.post(ep.MODIFYPROFILE_EP, json=pf.get_mod_profile()) 
    assert resp.status_code == OK 
 
@patch('db.users.get_users')
def test_get_users(mock_get_users):
    mock_get_users.return_value = SAMPLE_USER
    users = usrs.get_users()
    assert isinstance(users, dict)
    assert len(users) > 0

@pytest.mark.skip(reason= "endpoint does not exist yet") 
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

@pytest.mark.skip(reason="endpoint does not exist yet") 
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

def test_postTask():
    resp = TEST_CLIENT.post(ep.POSTTASK_EP, json=SAMPLE_USER)
    print(f'{resp=}')
    resp_json = resp.get_json()
    print(f'{resp_json=}')
    assert ep.TASK_RESP in resp_json
    assert ep.USERNAME_RESP in resp_json

@pytest.fixture()
def setup_viewGoals():
    usrs.create_user(SAMPLE_USER[ep.USERNAME_RESP], SAMPLE_USER[ep.PASSWORD_RESP])
    usrs.create_profile(SAMPLE_USER[ep.USERNAME_RESP], SAMPLE_PROFILE[ep.NAME], SAMPLE_PROFILE[ep.GOALS], SAMPLE_PROFILE[ep.GROUPS], SAMPLE_PROFILE[ep.PRIVATE])


def test_viewGoals():
    resp = TEST_CLIENT.get(ep.VIEWGOALS_EP)
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)
    assert ep.GOALS in resp_json
    goals = resp_json[ep.GOALS]
    assert isinstance(goals, list)
    for goal in goals:
        assert isinstance(goal, str)

def test_postGoal():
    resp = TEST_CLIENT.post(ep.POSTGOAL_EP, json=SAMPLE_USER)
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
    assert ep.GROUPS in resp_json
    groups = resp_json[ep.GROUPS]
    assert isinstance(groups, list)
    for group in groups:
        assert isinstance(group, str)



def test_postGroup():
    resp = TEST_CLIENT.post(ep.POSTGROUP_EP, json=SAMPLE_USER)
    print(f'{resp=}')
    resp_json = resp.get_json()
    print(f'{resp_json=}')
    assert ep.GROUP_RESP in resp_json
    assert ep.USERNAME_RESP in resp_json

def test_likeTask():
    resp = TEST_CLIENT.post(ep.LIKETASK_EP, json=SAMPLE_USER)
    print(f'{resp=}')
    resp_json = resp.get_json()
    print(f'{resp_json=}') 
    assert ep.LIKE_RESP in resp.json
    assert ep.USERNAME_RESP in resp_json

def test_unlikeTask():
    resp = TEST_CLIENT.post(ep.UNLIKETASK_EP, json=SAMPLE_USER)
    print(f'{resp=}')
    resp_json = resp.get_json()
    print(f'{resp_json=}') 
    assert ep.UNLIKE_RESP in resp.json
    assert ep.USERNAME_RESP in resp_json

@pytest.fixture()
def setup_likeTask():
    tsks.like_task(SAMPLE_USER[ep.USERNAME_RESP], SAMPLE_TASK[ep.TASK_NAME], SAMPLE_TASK[ep.TASK_DESCRIPTION], SAMPLE_TASK[ep.LIKE])  
