#import server.endpoints as ep
import sys
sys.path.append("..")
from server import endpoints as ep

from unittest.mock import patch

import db.users as usrs
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
    
    

def test_profile():
    resp = TEST_CLIENT.get(ep.PROFILE_EP) 
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

def test_create_profile():
    resp = TEST_CLIENT.post(ep.CREATEPROFILE_EP, json=SAMPLE_PROFILE) 
    print(f'{resp=}')
    resp_json = resp.get_json()
    assert ep.PROFILE_VALID_RESP in resp_json
    assert resp_json[ep.PROFILE_VALID_RESP] == 200
    
@pytest.mark.skip("modify profile endpoint does not exist yet")
def test_modify_profile():
    pass

def test_viewTasks():
    resp = TEST_CLIENT.get(ep.VIEWTASKS_EP)
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)
    assert ep.TASKS in resp_json
    tasks = resp_json[ep.TASKS]
    assert isinstance(tasks, list)
    for task in tasks:
        assert isinstance(task, str)

def test_postTask():
    resp = TEST_CLIENT.post(ep.POSTTASK_EP, json=SAMPLE_USER)
    print(f'{resp=}')
    resp_json = resp.get_json()
    print(f'{resp_json=}')
    assert ep.TASK_RESP in resp_json
    assert ep.USERNAME_RESP in resp_json

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
