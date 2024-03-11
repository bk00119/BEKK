import pytest
from bson.objectid import ObjectId
import db.db_connect as dbc
import db.comments as cmt

@pytest.fixture(scope='function')
def temp_comment():
    comment = {}
    comment[cmt.USER_ID] = "6575033f3b89d2b4f309d7af"
    comment[cmt.CONTENT] = 'test comment content'
    ret = cmt.add_comment(comment[cmt.USER_ID], comment[cmt.CONTENT])
    comment[cmt.ID] = ret
    return comment

def test_add_comment():
    test_comment = cmt.get_new_test_comments()
    ret = cmt.add_comment(test_comment[cmt.USER_ID], test_comment[cmt.CONTENT])
    assert isinstance(ret, str)
    cmt.delete_comment(ret)

def test_delete_comment(temp_comment):
    comment = temp_comment
    cmt.delete_comment(ObjectId(comment[cmt.ID]))
    assert not cmt.id_exists(ObjectId(comment[cmt.ID]))

def test_delete_comment_not_exist():
    id = dbc.gen_object_id()
    with pytest.raises(ValueError):
        cmt.delete_comment(id)

def test_get_comment(temp_comment):
    comment = temp_comment
    ret = cmt.get_comment(ObjectId(comment[cmt.ID]))
    assert isinstance(ret, dict)
    assert ret[cmt.USER_ID] == comment[cmt.USER_ID]
    assert ret[cmt.CONTENT] == comment[cmt.CONTENT]
    cmt.delete_comment(ObjectId(comment[cmt.ID]))

def test_get_comment_not_exist():
    id = dbc.gen_object_id()
    with pytest.raises(ValueError):
        cmt.get_comment(id)

@pytest.mark.skip(reason="not implemented yet") 
def test_get_user_comments(temp_comment):
    comment = temp_comment
