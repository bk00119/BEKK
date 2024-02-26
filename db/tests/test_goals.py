import pytest
from bson.objectid import ObjectId
import db.db_connect as dbc
import db.goals as gls

@pytest.fixture(scope='function')
def temp_goal():
    goal = {}
    goal[gls.USER_ID] = "6575033f3b89d2b4f309d7af"
    goal[gls.CONTENT] = 'test goal content'
    goal[gls.IS_COMPLETED] = False
    ret = gls.set_goal(goal[gls.USER_ID], goal[gls.CONTENT], goal[gls.IS_COMPLETED])
    goal[gls.ID] = ret
    return goal

def test_set_goal():
    test_goal = gls.get_new_test_goals()
    ret = gls.set_goal(test_goal[gls.USER_ID], test_goal[gls.CONTENT], test_goal[gls.IS_COMPLETED])
    assert isinstance(ret, str)
    gls.delete_set_goal(ret)

def test_delete_goal(temp_goal):
    goal = temp_goal
    gls.delete_set_goal(ObjectId(goal[gls.ID]))
    assert not gls.id_exists(ObjectId(goal[gls.ID]))

def test_delete_goal_not_exist():
    id = dbc.gen_object_id()
    with pytest.raises(ValueError):
        gls.delete_set_goal(id)

def test_get_goal(temp_goal):
    goal = temp_goal
    ret = gls.get_set_goal(ObjectId(goal[gls.ID]))
    assert isinstance(ret, dict)
    assert ret[gls.USER_ID] == goal[gls.USER_ID]
    assert ret[gls.CONTENT] == goal[gls.CONTENT]
    assert ret[gls.IS_COMPLETED] == goal[gls.IS_COMPLETED]
    gls.delete_set_goal(ObjectId(goal[gls.ID]))

def test_get_goal_not_exist():
    id = dbc.gen_object_id()
    with pytest.raises(ValueError):
        gls.get_set_goal(id)

@pytest.mark.skip(reason="not implemented yet") 
def test_get_user_goals(temp_goal):
    goal = temp_goal
