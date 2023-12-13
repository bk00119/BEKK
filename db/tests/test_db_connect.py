import pytest

import db.db_connect as dbc

TEST_DB = dbc.DB
TEST_COLLECT = 'tasks'

TEST_TITLE = 'title'
TEST_USER = 'test_user'

# @pytest.mark.skip(reason="using local MongoDB") 
@pytest.fixture(scope='function')
def temp_rec():
    dbc.connect_db()
    # testing insert_one()
    dbc.client[TEST_DB][TEST_COLLECT].insert_one({TEST_TITLE: TEST_TITLE})
    # yield to our test function
    yield
    # testing delete_one()
    dbc.client[TEST_DB][TEST_COLLECT].delete_one({TEST_TITLE: TEST_TITLE})

# @pytest.mark.skip(reason="using local MongoDB") 
def test_fetch_all_as_dict(temp_rec):
    dbc.connect_db()
    ret = dbc.fetch_all_as_dict(TEST_DB, TEST_COLLECT)
    assert ret is not None

def test_fetch_one(temp_rec):
    ret = dbc.fetch_one(TEST_COLLECT, {TEST_TITLE: TEST_TITLE})
    assert ret is not None
    
def test_fetch_one_not_exist(temp_rec):
    ret = dbc.fetch_one(TEST_COLLECT, {TEST_TITLE: 'not a field value in db!'})
    assert ret is None

def test_update_one(temp_rec):
    dbc.update_one(TEST_COLLECT, {TEST_TITLE: TEST_TITLE}, {"$addToSet": {"likes": TEST_USER}})
