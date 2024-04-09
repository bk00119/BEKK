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

def test_add_post(generate_post_fields):
    """
    Tests that add_post returned post id
    """
    # CREATE POST
    post_id = psts.add_post(**generate_post_fields)
    assert post_id is not None  
    psts.del_post(post_id)
    

def test_fetch_by_user_id(generate_post_fields):
    """
    Tests user_id-based post fetching
    """
    user_id = generate_post_fields[psts.USER_ID]
    posts = psts.fetch_by_user_id(user_id) 
    for post_id in posts:
        post = posts[post_id]
        assert post[psts.USER_ID] == user_id

def test_fetch_by_post_id(generate_post_fields):
    post_id = psts.add_post(**generate_post_fields)
    post = psts.fetch_by_post_id(post_id)
    assert post is not None 
    psts.del_post(post_id)

def test_del_post(generate_post_fields):
    """
    Tests post deletion 
    """
    post_id = psts.add_post(**generate_post_fields)
    psts.del_post(post_id) 
    assert psts.fetch_by_post_id(post_id) is None
    



    