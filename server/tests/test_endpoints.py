
import server.endpoints as ep

TEST_CLIENT = ep.app.test_client()

SAMPLE_USER = {
    'username': 'user1234',
    'password': 'pw1234'
}

def test_login():
    resp = TEST_CLIENT.post(ep.LOGIN_EP, json=SAMPLE_USER)
    print(f'{resp=}')
    resp_json = resp.get_json()
    print(f'{resp_json=}')
    assert ep.TOKEN_RESP in resp_json

def test_signup():
    resp = TEST_CLIENT.post(ep.SIGNUP_EP, json=SAMPLE_USER)
    print(f'{resp=}')
    resp_json = resp.get_json()
    print(f'{resp_json=}')
    assert ep.TOKEN_RESP in resp_json
    assert ep.USERNAME_RESP in resp_json

# check if data exists
def test_profile():
    resp = TEST_CLIENT.get(ep.PROFILE_EP) 
    resp_json = resp.get_json() 
    assert isinstance(resp_json, dict)
    assert ep.NAME in resp_json 
    assert ep.GROUPS in resp_json 
    assert ep.GOALS in resp_json
    groups = resp_json[ep.GROUPS] 
    goals = resp_json[ep.GOALS] 
    assert isinstance(groups, list) 
    assert isinstance(goals, list)
    for group_name in groups:
        assert isinstance(group_name, str) 
    for goal_title in goals:
        assert isinstance(goal_title, str) 

def test_viewTasks():
    resp = TEST_CLIENT.get(ep.VIEWTASKS_EP)
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)
    assert ep.TASKS in resp_json
    tasks = resp_json[ep.TASKS]
    assert isinstance(tasks, list)
    for task in tasks:
        assert isinstance(task, str)