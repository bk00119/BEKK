import pytest
import db.posts as psts

@pytest.fixture()
def generate_post_fields():
    return {
        psts.USER_ID: '6575033f3b89d2b4f309d7af', 
        psts.IS_COMPLETED: False, 
        psts.CONTENT: "Test Entry", 
        psts.TASK_IDS: [], 
        psts.GOAL_IDS: [], 
        psts.LIKE_IDS: [],
        psts.COMMENT_IDS: [], 
    }   

@pytest.mark.skip(reason="collection overload")
def test_add_post(generate_post_fields):
    """
    Tests that add_post returned post id
    """
    post_id = psts.add_post(**generate_post_fields)
    assert post_id is not None  


def test_fetch_by_user_id(generate_post_fields):
    user_id = generate_post_fields[psts.USER_ID]
    posts = psts.fetch_by_user_id(user_id) 
    for post_id in posts:
        post = posts[post_id]
        assert post[psts.USER_ID] == user_id
    