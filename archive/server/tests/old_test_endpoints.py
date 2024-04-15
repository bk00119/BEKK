import db.posts as psts 


SAMPLE_PROFILE = {
    ep.NAME: 'John Adams',
    ep.GOALS: ['cs hw2', 'fin hw3'],
    ep.PRIVATE: False
}


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
    
@pytest.fixture()
def setup_viewProfileGroups():
    usrs.create_user(SAMPLE_USER[ep.USERNAME_RESP], SAMPLE_USER[ep.PASSWORD_RESP])
    usrs.create_profile(SAMPLE_USER[ep.USERNAME_RESP], SAMPLE_PROFILE[ep.NAME], SAMPLE_PROFILE[ep.GOALS], SAMPLE_PROFILE[ep.GROUPS], SAMPLE_PROFILE[ep.PRIVATE])  


def test_viewProfileGroups():
    resp = TEST_CLIENT.get(ep.VIEWPROFILEGROUPS_EP)
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)
    assert ep.GROUPS in resp_json

@pytest.fixture()
def setup_deleteGroup():
    usrs.delete_group(SAMPLE_USER[ep.USERNAME_RESP], SAMPLE_PROFILE[ep.NAME], SAMPLE_PROFILE[ep.GOALS])

@pytest.mark.skip(reason= "not using this endpoint") 
def test_deleteGroup():
    resp = TEST_CLIENT.post(ep.DELETEGROUP_EP, json=SAMPLE_USER)
    print(f'{resp=}')
    resp_json = resp.get_json()
    print(f'{resp_json=}')
    assert ep.GROUP_RESP in resp_json
    assert ep.USERNAME_RESP in resp_json

@patch('db.profiles.add_group', return_value=pf.MOCK_ID, autospec=True)
def test_addGroup(mock_add):
    """
    Testing for posting a new task successfully: PostTask.post()
    """
    resp = TEST_CLIENT.post(ep.ADDGROUP_EP, json=pf.get_new_test_group())
    assert resp.status_code == OK


def test_likeTask():
    new_task = tsks.get_new_test_task()
    test_task_id = str(tsks.add_task(new_task[tsks.USER_ID], new_task[tsks.GOAL_ID], new_task[tsks.CONTENT], new_task[tsks.IS_COMPLETED]))
    test_user_id = str(dbc.gen_object_id())
    resp = TEST_CLIENT.post(ep.LIKETASK_EP, json={tsks.ID: test_task_id, tsks.USER_ID: test_user_id})
    assert resp.status_code == OK
    tsks.del_task(test_task_id)

def test_unlikeTask():
    new_task = tsks.get_new_test_task()
    test_task_id = str(tsks.add_task(new_task[tsks.USER_ID], new_task[tsks.GOAL_ID], new_task[tsks.CONTENT], new_task[tsks.IS_COMPLETED]))
    test_user_id = str(dbc.gen_object_id())
    tsks.like_task(test_task_id, test_user_id)
    resp = TEST_CLIENT.post(ep.UNLIKETASK_EP, json={tsks.ID: test_task_id, tsks.USER_ID: test_user_id})
    assert resp.status_code == OK
    tsks.del_task(test_task_id)


def test_removeProfile():
    new_profile = pf.get_test_profile()
    test_profile_id = str(pf.add_profile(new_profile[pf.NAME], new_profile[pf.GOALS], new_profile[pf.TASKS], new_profile[pf.POSTS], new_profile[pf.PRIVATE] ))
    resp = TEST_CLIENT.post(ep.REMOVEPROFILE_EP, json={pf.MOCK_ID: test_profile_id})
    assert resp.status_code == OK
    pf.del_profile(test_profile_id)

@pytest.fixture()
def setup_likeTask():
    tsks.like_task(SAMPLE_USER[ep.USERNAME_RESP], SAMPLE_TASK[ep.TASK_NAME], SAMPLE_TASK[ep.TASK_DESCRIPTION], SAMPLE_TASK[ep.LIKE])  

@pytest.fixture()
def setup_unlikeTask():
    tsks.unlike_task(SAMPLE_USER[ep.USERNAME_RESP], SAMPLE_TASK[ep.TASK_NAME], SAMPLE_TASK[ep.TASK_DESCRIPTION], SAMPLE_TASK[ep.LIKE])
