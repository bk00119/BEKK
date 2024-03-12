import pytest
import db.posts as psts

@pytest.fixture()
def generate_post_fields():
    return {
        psts.USER_ID: None, 
        psts.IS_COMPLETED: False, 
        psts.CONTENT: "Test Entry", 
        psts.TASK_IDS: [], 
        psts.GOAL_IDS: [], 
        psts.LIKE_IDS: [],
        psts.COMMENT_IDS: [], 
    }

def test_add_post(generate_post_fields):
    """
    Tests that add_post returned post id 
    """
    post_id = psts.add_post(**generate_post_fields)
    assert post_id is not None  

