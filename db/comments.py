"""
This module interfaces to our comments data.
"""

# from pymongo import MongoClient
import random
from bson.objectid import ObjectId
import db.db_connect as dbc
import db.users as usrs
import db.posts as psts
from datetime import datetime

# COMMENTS COLLECTION:
# _id: ObjectID
# user_id: str(ObjectID)
# content: str

COMMENTS_COLLECT = 'comments'
POSTS_COLLECT = "posts"
ID = '_id'
USER_ID = 'user_id'
CONTENT = 'content'
USERNAME = 'username'
TIMESTAMP = 'timestamp'
POST_ID = 'post_id'

ID_LEN = 24
BIG_NUM = 100_000_000_000_000_000_000
MOCK_ID = MOCK_ID = '0' * ID_LEN


def get_comments():
    dbc.connect_db()
    return dbc.fetch_all_as_dict(dbc.DB, COMMENTS_COLLECT, None)


def get_test_comment():
    return {
        "user_id": 'user123',
        'content': 'good job!'
    }


def get_new_test_comments():
    '''
    sample task for testing add_comment()
    '''
    add_comment = {}
    _id = random.randint(0, BIG_NUM)
    _id = str(_id)
    _id = _id.rjust(ID_LEN, '0')
    add_comment[USER_ID] = '6575033f3b89d2b4f309d7af'
    # add_comment[POST_ID] = ''  # NEED TO WORK ON THIS
    add_comment[POST_ID] = psts.add_post('6575033f3b89d2b4f309d7af',
                                         "test post", [], [], [], [])
    add_comment[CONTENT] = 'great work!'
    return add_comment


def id_exists(id: str) -> bool:
    dbc.connect_db()
    return dbc.fetch_one(COMMENTS_COLLECT, {ID: ObjectId(id)})


def add_comment(user_id: str, content: str):
    '''
    user adds a comment to a post, which is added to the Comments DB
    '''
    comment = {}
    comment[USER_ID] = user_id
    comment[CONTENT] = content
    comment[TIMESTAMP] = str(datetime.now())
    dbc.connect_db()
    _id = dbc.insert_one(COMMENTS_COLLECT, comment)
    return _id


def delete_comment(comment_id: str):
    if id_exists(comment_id):
        return dbc.del_one(COMMENTS_COLLECT, {ID: ObjectId(comment_id)})
    else:
        raise ValueError(f'Delete Comment Failed: {comment_id} not in DB.')


def get_comment(comment_id: str):
    # gets a singular comment
    if id_exists(comment_id):
        return dbc.fetch_one(COMMENTS_COLLECT, {ID: ObjectId(comment_id)})
    else:
        raise ValueError(f'Get Comment Failed: {comment_id} not in DB.')


def get_user_comments(user_id: str):
    # gets all comments under an user
    if usrs.id_exists(user_id):
        comments = dbc.fetch_all_as_dict(dbc.DB, COMMENTS_COLLECT,
                                         {USER_ID: user_id})

        username = usrs.get_user_public(user_id).get(USERNAME)
        all_comments = []
        for comment_id in comments:
            all_comments.append(get_comment(comment_id).get(CONTENT))

        return {
            USERNAME: username,
            COMMENTS_COLLECT: all_comments
        }
    else:
        raise ValueError(f'Get User Comments Failed: {user_id} not in DB.')


def get_post_comments(post_id: str):
    # gets all the comments under a post
    try:
        post = psts.fetch_by_post_id(post_id)

        if post:
            users_comments = []
            for comment_id in post['comment_ids']:
                comment_data = get_comment(comment_id)
                user_data = usrs.get_user_public(comment_data['user_id'])
                user_comment = {
                    'username': user_data.get(USERNAME),
                    'comment': comment_data.get(CONTENT)
                }
                users_comments.append(user_comment)
            return users_comments
        else:
            print(f"Post with ID {post_id} not found.")
    except Exception as e:
        print(f"Error getting post comments: {e}")
