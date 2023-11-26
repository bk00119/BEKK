import pytest

import db.db_connect as dbc

TEST_DB = dbc.DB
TEST_COLLECT = 'tasks'

# @pytest.mark.skip(reason="using local MongoDB") 
@pytest.fixture(scope='function')
def temp_rec():
    dbc.connect_db()

# @pytest.mark.skip(reason="using local MongoDB") 
def test_fetch_all_as_dict(temp_rec):
    dbc.connect_db()
    ret = dbc.fetch_all_as_dict(TEST_DB, TEST_COLLECT)
    assert ret is not None
