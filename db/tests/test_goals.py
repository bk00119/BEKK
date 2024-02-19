import pytest
from bson.objectid import ObjectId
import db.db_connect as dbc
import db.tasks as tsks
import db.goals as gls

@pytest.fixture(scope='function')
def temp_goal():
    goal = {}
    goal[gls.USER_ID] = "abc123"
    goal[gls.IS_COMPLETED] = True
    goal[gls.CONTENT] = 'test goal content'
    return goal
